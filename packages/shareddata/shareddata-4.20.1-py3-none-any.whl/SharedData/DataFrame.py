# THIRD PARTY LIBS
import os
import sys
import pandas as pd
import numpy as np
import json
import time
import io
import gzip
import hashlib
import shutil
from threading import Thread

from pandas.tseries.offsets import BDay
from pathlib import Path
from multiprocessing import shared_memory
from datetime import datetime, timedelta


from SharedData.Logger import Logger
from SharedData.AWSS3 import S3Download, S3Upload, UpdateModTime


class SharedDataFrame:

    def __init__(self, sharedDataPeriod, tag, df=None):
        self.sharedDataPeriod = sharedDataPeriod
        self.tag = tag
        self.tagstr = self.tag.strftime('%Y%m%d%H%M')

        self.sharedDataFeeder = sharedDataPeriod.sharedDataFeeder
        self.feeder = sharedDataPeriod.sharedDataFeeder.feeder
        self.sharedData = sharedDataPeriod.sharedDataFeeder.sharedData
        self.database = self.sharedData.database

        self.period = sharedDataPeriod.period
        self.periodSeconds = sharedDataPeriod.periodSeconds

        self.init_time = time.time()

        # Time series dataframe
        self.data = pd.DataFrame()

        self.create_map = 'na'
        if df is None:  # Read dataset tag
            # allocate memory
            ismapped = self.Malloc()
            if not ismapped:
                # Read
                df = self.Read()
                if not df.empty:
                    self.Malloc(df)

        else:  # map existing dataframe
            # drop non number fields
            df = df._get_numeric_data().astype(np.float64)
            # allocate memory
            self.Malloc(df)

        self.init_time = time.time() - self.init_time

    # GETTERS AND SETTERS
    def getDataPath(self, iswrite=False):
        shm_name = self.sharedData.user
        shm_name = shm_name + '/' + self.sharedData.database
        shm_name = shm_name + '/' + self.sharedDataFeeder.feeder
        shm_name = shm_name + '/' + self.period + '/' + self.tagstr
        if os.name == 'posix':
            shm_name = shm_name.replace('/', '\\')

        path = Path(os.environ['DATABASE_FOLDER'])
        path = path / self.sharedData.user
        path = path / self.sharedData.database
        path = path / self.sharedDataFeeder.feeder
        path = path / self.period
        path = Path(str(path).replace('\\', '/'))
        if self.sharedData.save_local:
            if not os.path.isdir(path):
                os.makedirs(path)

        return path, shm_name

    # C R U D
    def Malloc(self, df=None):
        tini = time.time()
        if os.environ['LOG_LEVEL'] == 'DEBUG':
            Logger.log.debug('Malloc %s/%s/%s/%s ...%.2f%% ' %
                             (self.database, self.feeder, self.period, self.tagstr, 0.0))

        # Create write ndarray
        path, shm_name = self.getDataPath()
        if not df is None:
            # try create memory file
            try:
                r = len(df.index)
                c = len(df.columns)

                idx_b = str.encode(','.join(df.index.values),
                                   encoding='UTF-8', errors='ignore')
                colscsv_b = str.encode(','.join(df.columns.values),
                                       encoding='UTF-8', errors='ignore')
                nb_idx = len(idx_b)
                nb_cols = len(colscsv_b)
                nb_data = int(r*c*8)
                header_b = np.array([r, c, nb_idx, nb_cols, nb_data]).astype(
                    np.int64).tobytes()
                nb_header = len(header_b)

                nb_buf = nb_header+nb_idx+nb_cols+nb_data
                nb_offset = nb_header+nb_idx+nb_cols

                [self.shm, ismalloc] = self.sharedData.malloc(
                    shm_name, create=True, size=nb_buf)

                i = 0
                self.shm.buf[i:nb_header] = header_b
                i = i + nb_header
                self.shm.buf[i:i+nb_idx] = idx_b
                i = i + nb_idx
                self.shm.buf[i:i+nb_cols] = colscsv_b

                self.shmarr = np.ndarray((r, c),
                                         dtype=np.float64, buffer=self.shm.buf, offset=nb_offset)

                self.shmarr[:] = df.values.copy()

                self.data = pd.DataFrame(self.shmarr,
                                         index=df.index,
                                         columns=df.columns,
                                         copy=False)

                if os.environ['LOG_LEVEL'] == 'DEBUG':
                    Logger.log.debug('Malloc create %s ...%.2f%% %.2f sec! ' %
                                     (shm_name, 100, time.time()-tini))
                self.create_map = 'create'
                return True
            except Exception as e:
                return False
        else:  # df is None
            # try map dataframe
            try:
                [self.shm, ismalloc] = self.sharedData.malloc(shm_name)

                i = 0
                nb_header = 40
                header = np.frombuffer(
                    self.shm.buf[i:nb_header], dtype=np.int64)
                i = i + nb_header
                nb_idx = header[2]
                idx_b = bytes(self.shm.buf[i:i+nb_idx])
                index = idx_b.decode(
                    encoding='UTF-8', errors='ignore').split(',')
                i = i + nb_idx
                nb_cols = header[3]
                cols_b = bytes(self.shm.buf[i:i+nb_cols])
                columns = cols_b.decode(
                    encoding='UTF-8', errors='ignore').split(',')

                r = header[0]
                c = header[1]
                nb_data = header[4]
                nb_offset = nb_header+nb_idx+nb_cols

                self.shmarr = np.ndarray((r, c), dtype=np.float64,
                                         buffer=self.shm.buf, offset=nb_offset)

                self.data = pd.DataFrame(self.shmarr,
                                         index=index,
                                         columns=columns,
                                         copy=False)

                if not df is None:
                    iidx = df.index.intersection(self.data.index)
                    icol = df.columns.intersection(self.data.columns)
                    self.data.loc[iidx, icol] = df.loc[iidx, icol]

                self.create_map = 'map'
                return True
            except:
                pass

        return False

    # READ
    def Read(self):
        return self.ReadDataFrame()

    def ReadDataFrame(self):
        tini = time.time()
        path, shm_name = self.getDataPath()
        local_path = str(path/(self.tagstr+'.bin'))
        remote_path = local_path+'.gzip'
        df_io = None
        if self.sharedData.s3read:
            # Synchronize S3
            force_download = (not self.sharedData.save_local)
            [df_io_gzip, df_local_mtime, df_remote_mtime] = \
                S3Download(remote_path, local_path, force_download)
            if not df_io_gzip is None:
                df_io = io.BytesIO()
                df_io_gzip.seek(0)
                with gzip.GzipFile(fileobj=df_io_gzip, mode='rb') as gz:
                    shutil.copyfileobj(gz, df_io)
                if self.sharedData.save_local:
                    SharedDataFrame.write_file(
                        df_io, local_path, df_remote_mtime)
                    UpdateModTime(local_path, df_remote_mtime)

        if (df_io is None) & (self.sharedData.save_local):
            # read local
            if os.path.isfile(str(local_path)):
                df_io = open(str(local_path), 'rb')

        if not df_io is None:
            return SharedDataFrame.read_data(df_io, local_path)

        return pd.DataFrame([])

    def read_data(df_io, local_path):
        df_io.seek(0)
        _header = np.frombuffer(df_io.read(40), dtype=np.int64)
        _idx_b = df_io.read(int(_header[2]))
        _idxcsv = _idx_b.decode(encoding='UTF-8', errors='ignore')
        _idx = _idxcsv.split(',')
        _colscsv_b = df_io.read(int(_header[3]))
        _colscsv = _colscsv_b.decode(encoding='UTF-8', errors='ignore')
        _cols = _colscsv.split(',')
        _data = np.frombuffer(df_io.read(int(_header[4])), dtype=np.float64).reshape(
            (_header[0], _header[1]))
        # calculate hash
        _m = hashlib.md5(_idx_b)
        _m.update(_colscsv_b)
        _m.update(_data)
        _md5hash_b = _m.digest()
        __md5hash_b = df_io.read(16)
        if not _md5hash_b == __md5hash_b:
            raise Exception('DataFrame file corrupted!\n%s' % (local_path))
        df = pd.DataFrame(_data, index=_idx, columns=_cols)
        df_io.close()
        return df

    # WRITE
    def Write(self):
        path, shm_name = self.getDataPath(iswrite=True)
        local_path = str(path/(self.tagstr+'.bin'))
        remote_path = local_path+'.gzip'
        df_io = SharedDataFrame.create_dataframe_io(self.data)
        mtime = datetime.now().timestamp()
        threads = []
        if self.sharedData.s3write:
            df_io.seek(0)
            gzip_io = io.BytesIO()
            with gzip.GzipFile(fileobj=gzip_io, mode='wb', compresslevel=1) as gz:
                shutil.copyfileobj(df_io, gz)
            threads = [*threads,
                       Thread(target=S3Upload, args=(gzip_io, remote_path, mtime))]

        if self.sharedData.save_local:
            threads = [*threads,
                       Thread(target=SharedDataFrame.write_file, args=(df_io, local_path, mtime))]

        for i in range(len(threads)):
            threads[i].start()

        for i in range(len(threads)):
            threads[i].join()

    def create_dataframe_io(df):
        r, c = df.shape
        idx_b = str.encode(','.join(df.index.values),
                           encoding='UTF-8', errors='ignore')
        colscsv_b = str.encode(','.join(df.columns.values),
                               encoding='UTF-8', errors='ignore')
        nbidx = len(idx_b)
        nbcols = len(colscsv_b)
        data = np.ascontiguousarray(df.values.astype(np.float64))
        header = np.array([r, c, nbidx, nbcols, r*c*8]).astype(np.int64)
        # calculate hash
        m = hashlib.md5(idx_b)
        m.update(colscsv_b)
        m.update(data)
        md5hash_b = m.digest()
        # allocate memory
        io_obj = io.BytesIO()
        io_obj.write(header)
        io_obj.write(idx_b)
        io_obj.write(colscsv_b)
        io_obj.write(data)
        io_obj.write(md5hash_b)
        return io_obj

    def write_file(io_obj, path, mtime):
        with open(path, 'wb') as f:
            f.write(io_obj.getbuffer())
            f.flush()
        os.utime(path, (mtime, mtime))
