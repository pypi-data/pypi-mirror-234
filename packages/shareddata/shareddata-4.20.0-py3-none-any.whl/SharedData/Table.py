import os
import threading
import time
import pandas as pd
import numpy as np
from pathlib import Path
from multiprocessing import shared_memory
import gzip
import io
import hashlib
from datetime import datetime
from tqdm import tqdm
import threading
import psutil
import traceback

from SharedData.Logger import Logger
from SharedData.AWSS3 import S3Upload, S3Download, UpdateModTime, S3ListFolder
from SharedData.TableIndex import TableIndex
from SharedData.SharedNumpy import SharedNumpy
from SharedData.RealTime import RealTime

from SharedData.Utils import cpp


class Table:
    
    # TODO: create partitioning option yearly, monthly, daily

    def __init__(self, shareddata, database, period, source, tablename,
                 records=None, names=None, formats=None, size=None,
                 overwrite=False, user='master', tabletype='DISK', partitioning=None):
        self.type = tabletype

        self.shareddata = shareddata
        self.user = user
        self.database = database
        self.period = period
        self.source = source
        self.tablename = tablename
        self.subscription_thread = None

        self.names = names
        self.formats = formats
        self.size = size
        self.overwrite = overwrite
        self.partitioning = partitioning
        # header
        self.hdr = None
        # records
        self.recnames = []
        self.recformats = []
        self.recdtype = None
        self.records = np.ndarray([])

        # index
        self.index = TableIndex(self)

        self.init_headers()

        self.init_paths()

        self.isloaded = self.create_mutex()

        errmsg = ''
        try:
            self.acquire()

            self.exists_local = self.filepath.is_file()
            self.exists_remote = self.exists_local
            if not self.exists_local:
                keys = S3ListFolder(self.shm_name.replace('\\', '/'))
                self.exists_remote = np.any(
                    [self.relpath+'/' in s for s in keys])
            self.exists = self.exists_local | self.exists_remote
            if self.type == 'MEMORY':
                self.exists = self.exists | self.isloaded

            if (not records is None):
                if isinstance(records, pd.DataFrame):
                    records = self.df2records(records)
                descr = records.__array_interface__['descr']
                self.names = [item[0] for item in descr]
                self.formats = [item[1] for item in descr]
                if self.size is None:
                    self.size = int(records.size)

            if (not self.exists) | (self.overwrite):
                if (not self.names is None) \
                    & (not self.formats is None)\
                        & (not self.size is None):
                    self.create_header()

                    self.create_file()
                    
                    self.malloc()
                elif not self.exists:
                    raise Exception(
                        '%s not found create first!' % (self.relpath))

                if not records is None:
                    self.records.insert(records, acquire=False)

            elif self.exists:

                if self.exists_local:
                    with open(self.filepath, 'rb') as io_obj:
                        self.read_header(io_obj)

                head_io = tail_io = None
                if (self.shareddata.s3read)\
                        & ((not self.isloaded) | (not self.exists_local)):
                    [head_io, tail_io] = self.download()

                if not head_io is None:
                    self.read_header(head_io)
                    self.hdr['isloaded'] == 0

                if not tail_io is None:
                    self.read_tailheader(tail_io)
                    self.hdr['isloaded'] == 0

                self.create_file()

                self.malloc()

                if (not head_io is None) | (not tail_io is None):
                    self.read_data(head_io, tail_io)

                if self.hdr['isloaded'] == 0:
                    self.hdr['isloaded'] = 1
                
                # set the modify time of the file
                mtime = max(self.hdr['mtime'],
                            self.hdr['mtimehead'], self.hdr['mtimetail'])
                self.hdr['mtime'] = mtime
                os.utime(self.filepath, (mtime, mtime))

                

            self.index.initialize()
        except Exception as e:
            tb = traceback.format_exc()
            errmsg = '%s error initializing\n %s\n%s!' % (
                self.relpath, str(tb), str(e))
            # errmsg = '%s error initalizing \n%s!' % (self.relpath,str(e))
            Logger.log.error(errmsg)
        finally:
            self.release()
            if errmsg != '':
                self.free()
                raise Exception(errmsg)

    def init_headers(self):
        self.header_changed = False
        # head header
        self._hdrnames = ['headersize', 'headerdescr', 'md5hashhead', 'md5hashtail',
                          'mtime', 'mtimehead', 'mtimetail',
                          'itemsize', 'recordssize', 'count',
                          'headsize', 'tailsize', 'minchgid',
                          'hastail', 'isloaded', 'isidxcreated',
                          'descr']
        self._hdrformats = ['<i8', '|S250', '|S16', '|S16',
                            '<f8', '<f8', '<f8',
                            '<i8', '<i8', '<i8',
                            '<i8', '<i8', '<i8',
                            '<u1', '<u1', '<u1',
                            '|SXXX']
        # tail header
        self._tailhdrnames = ['headersize', 'headerdescr',
                              'md5hash', 'mtime', 'tailsize']
        self._tailhdrformats = ['<i8', '|S80', '|S16', '<f8', '<i8']

    def init_paths(self):
        # path
        self.shm_name = self.user+'/'+self.database+'/' + \
            self.period+'/'+self.source+'/table/'+self.tablename
        self.relpath = str(self.shm_name)
        if os.name == 'posix':
            self.shm_name = self.shm_name.replace('/', '\\')
        self.path = Path(os.environ['DATABASE_FOLDER'])
        self.path = self.path / self.shm_name
        self.path = Path(str(self.path).replace('\\', '/'))
        if self.shareddata.save_local:
            os.makedirs(self.path, exist_ok=True)
        self.filepath = self.path / 'data.bin'
        self.headpath = self.path / 'head.bin'
        self.tailpath = self.path / 'tail.bin'

    ############### CREATE ###############
    def create_mutex(self):
        self.pid = os.getpid()

        [self.shm_mutex, isloaded] = self.shareddata.malloc(
            self.shm_name+'#mutex')
        if not isloaded:
            [self.shm_mutex, ismalloc] = self.shareddata.malloc(
                self.shm_name+'#mutex', create=True, size=8)
        dtype_mutex = np.dtype({'names': ['pid'], 'formats': ['<i8']})
        self.mutex = np.ndarray((1,), dtype=dtype_mutex,
                                buffer=self.shm_mutex.buf)[0]

        return isloaded

    def create_header(self):

        check_pkey = True
        npkeys = len(self.index.pkeycolumns)
        for k in range(npkeys):
            check_pkey = (check_pkey) & (
                self.names[k] == self.index.pkeycolumns[k])
        if not check_pkey:
            raise Exception('First columns must be %s!' %
                            (self.index.pkeycolumns))
        else:
            if not 'mtime' in self.names:
                self.names.insert(npkeys, 'mtime')
                self.formats.insert(npkeys, '<M8[ns]')

            # malloc recarray
            self.recnames = self.names
            self.rectypes = self.formats
            self.recdtype = np.dtype(
                {'names': self.recnames, 'formats': self.rectypes})
            descr_str = ','.join(self.recnames)+';'+','.join(self.rectypes)
            descr_str_b = str.encode(
                descr_str, encoding='UTF-8', errors='ignore')
            len_descr = len(descr_str_b)

            # build header
            self.hdrnames = self._hdrnames
            hdrformats = self._hdrformats.copy()
            hdrformats[-1] = hdrformats[-1].replace('XXX', str(len_descr))
            self.hdrformats = hdrformats
            hdrnames = ','.join(self.hdrnames)
            hdrdtypes = ','.join(self.hdrformats)
            hdrdescr_str = hdrnames+';'+hdrdtypes
            hdrdescr_str_b = str.encode(
                hdrdescr_str, encoding='UTF-8', errors='ignore')

            self.hdrdtype = np.dtype(
                {'names': self.hdrnames, 'formats': self.hdrformats})
            self.hdr = np.recarray(shape=(1,), dtype=self.hdrdtype)[0]
            self.hdr['headersize'] = 250
            self.hdr['headerdescr'] = hdrdescr_str_b
            self.hdr['mtime'] = datetime.now().timestamp()
            self.hdr['mtimehead'] = self.hdr['mtime']
            self.hdr['mtimetail'] = self.hdr['mtime']
            self.hdr['count'] = 0
            self.hdr['minchgid'] = self.hdr['count']
            self.hdr['itemsize'] = int(self.recdtype.itemsize)
            self.hdr['recordssize'] = int(self.size)
            self.hdr['headsize'] = 0
            self.hdr['descr'] = descr_str_b
            self.hdr['isloaded'] = 0
            self.hdr['isidxcreated'] = 0
    
    def create_file(self):
        totalbytes = int(self.hdrdtype.itemsize
                         + self.recdtype.itemsize*self.size)        
        if not self.exists_local:
            with open(self.filepath, 'wb') as f:
                # Seek to the end of the file
                f.seek(totalbytes-1)
                # Write a single null byte to the end of the file
                f.write(b'\x00')
                if os.name == 'posix':
                    os.posix_fallocate(f.fileno(), 0, totalbytes)
                elif os.name == 'nt':
                    pass #TODO: implement preallocation for windows in pyd
        elif (Path(self.filepath).stat().st_size < totalbytes):
            with open(self.filepath, 'ab') as f:
                # Seek to the end of the file
                f.seek(totalbytes-1)
                # Write a single null byte to the end of the file
                f.write(b'\x00')
                if os.name == 'posix':
                    os.posix_fallocate(f.fileno(), 0, totalbytes)
                elif os.name == 'nt':
                    pass #TODO: implement preallocation for windows in pyd
       
    def copy_file(self):
        """
        Copies the file to a temporary file, writes a new header, and extends the file if needed.
        Then, it renames the temporary file to the original file name and deletes the original file.
        """        
        if self.size is None:
            self.size = self.hdr['recordssize']
        totalbytes = int(self.hdrdtype.itemsize
                            + self.recdtype.itemsize*self.size)

        orig_size = int(self.orig_hdr.dtype.itemsize
                        +self.orig_hdr['recordssize']*self.orig_hdr['itemsize'])
        
        self.filepathtmp = str(self.filepath)+'.tmp'
        with open(self.filepath, 'rb') as f:
            with open(self.filepathtmp, 'wb') as ftmp:
                # write new header
                ftmp.seek(0)
                ftmp.write(self.hdr.tobytes())
                # copy data
                f.seek(self.orig_hdr.dtype.itemsize)
                bwritten = self.orig_hdr.dtype.itemsize
                message = 'Copying file :%iMB %s' % (
                    orig_size / (1024*1024), self.relpath)
                buffersize = int(1024**2*250)
                with tqdm(total=orig_size, unit='B', unit_scale=True, desc=message) as pbar:                    
                    while bwritten < orig_size:
                        nwrite = int(min(buffersize, orig_size-bwritten))
                        ftmp.write(f.read(nwrite))
                        pbar.update(nwrite)
                        bwritten += nwrite
                    # extend file if needed
                    if totalbytes>orig_size:
                        ftmp.write(b'\x00'*(totalbytes-orig_size))
                    ftmp.flush()
        
        #rename file
        os.remove(self.filepath)
        os.rename(self.filepathtmp,self.filepath)

    ############### DOWNLOAD ###############
    def download(self):
        head_io = None
        tail_io = None
        download_tail = False
        mtimetail = None

        tini = time.time()
        remote_path = str(self.headpath)+'.gzip'
        if not self.hdr is None:
            download_tail = self.hdr['hastail'] == 1
            mtimetail = self.hdr['mtimetail']
            [head_io_gzip, head_local_mtime, head_remote_mtime] = \
                S3Download(remote_path, local_mtime=self.hdr['mtimehead'])
        else:
            [head_io_gzip, head_local_mtime, head_remote_mtime] = \
                S3Download(remote_path)

        if not head_io_gzip is None:
            # remote file is newer than local
            # unzip head and read
            te = time.time()-tini+0.000001
            datasize = head_io_gzip.getbuffer().nbytes/1000000
            Logger.log.debug('download head %s %.2fMB in %.2fs %.2fMBps ' %
                             (self.relpath, datasize, te, datasize/te))
            head_io_gzip.seek(0)
            head_io = gzip.GzipFile(fileobj=head_io_gzip, mode='rb')
            self.read_header(head_io)
            download_tail = self.hdr['hastail'] == 1
            mtimetail = self.hdr['mtimetail'] - 1  # force tail download

        if download_tail:
            remote_path = str(self.tailpath)+'.gzip'
            [tail_io_gzip, tail_local_mtime, tail_remote_mtime] = \
                S3Download(remote_path, local_mtime=mtimetail)
            if not tail_io_gzip is None:
                tail_io_gzip.seek(0)
                tail_io = gzip.GzipFile(fileobj=tail_io_gzip, mode='rb')

        return [head_io, tail_io]

    ############### READ ###############
    def read_header(self, io_obj):
        io_obj.seek(0)
        # load header dtype
        nbhdrdescr = int.from_bytes(io_obj.read(8), byteorder='little')
        hdrdescr_b = io_obj.read(nbhdrdescr)
        hdrdescr = hdrdescr_b.decode(encoding='UTF-8', errors='ignore')
        hdrdescr = hdrdescr.replace('\x00', '')
        self.hdrnames = hdrdescr.split(';')[0].split(',')
        self.hdrformats = hdrdescr.split(';')[1].split(',')
        self.hdrdtype = np.dtype(
            {'names': self.hdrnames, 'formats': self.hdrformats})
        # read header
        io_obj.seek(0)
        self.hdr = np.ndarray((1,), dtype=self.hdrdtype,
                              buffer=io_obj.read(self.hdrdtype.itemsize))[0]
        # load data dtype
        descr = self.hdr['descr'].decode(encoding='UTF-8', errors='ignore')
        self.recnames = descr.split(';')[0].split(',')
        self.recformats = descr.split(';')[1].split(',')
        self.recdtype = np.dtype(
            {'names': self.recnames, 'formats': self.recformats})
                        
        if self.size is None:
            self.size = self.hdr['recordssize']

        if self.hdrnames == self._hdrnames:
            self.orig_hdr = self.hdr
        else:
            # convert header
            self.header_changed = True
            self.orig_hdr = self.hdr.copy()

            self.hdrnames = self._hdrnames
            len_descr = len(self.hdr['descr'])
            hdrformats = self._hdrformats.copy()
            hdrformats[-1] = hdrformats[-1].replace('XXX', str(len_descr))
            self.hdrformats = hdrformats
            hdrnames = ','.join(self.hdrnames)
            hdrdtypes = ','.join(self.hdrformats)
            hdrdescr_str = hdrnames+';'+hdrdtypes
            hdrdescr_str_b = str.encode(
                hdrdescr_str, encoding='UTF-8', errors='ignore')
            self.hdrdtype = np.dtype(
                {'names': self.hdrnames, 'formats': self.hdrformats})
            self.hdr = np.ndarray((1,), dtype=self.hdrdtype)[0]
            for name in self.orig_hdr.dtype.names:
                if name in self.hdr.dtype.names:
                    self.hdr[name] = self.orig_hdr[name]
            self.hdr['headerdescr'] = hdrdescr_str_b
            if not 'mtimehead' in self.orig_hdr.dtype.names:
                self.hdr['mtimehead'] = self.hdr['mtime']
            if not 'mtimetail' in self.orig_hdr.dtype.names:
                self.hdr['mtimetail'] = self.hdr['mtime']                
            self.hdr['isloaded'] = 0
            self.hdr['isidxcreated'] = 0

            if self.exists_local:
                self.copy_file()
     
    def read_tailheader(self, tail_io):
        tail_io.seek(0)
        tailnbhdrdescr = int.from_bytes(tail_io.read(8), byteorder='little')
        tailhdrdescr_b = tail_io.read(tailnbhdrdescr)
        tailhdrdescr = tailhdrdescr_b.decode(encoding='UTF-8', errors='ignore')
        tailhdrdescr = tailhdrdescr.replace('\x00', '')
        self.tailhdrnames = tailhdrdescr.split(';')[0].split(',')
        self.tailhdrformats = tailhdrdescr.split(';')[1].split(',')
        self.tailhdrdtype = np.dtype(
            {'names': self.tailhdrnames, 'formats': self.tailhdrformats})

        nbtailhdr = self.tailhdrdtype.itemsize
        tail_io.seek(0)
        tailheader_buf = tail_io.read(nbtailhdr)
        self.tailhdr = np.ndarray((1,),
                                  dtype=self.tailhdrdtype, buffer=tailheader_buf)[0]
        self.tailhdr = self.tailhdr.copy()
        self.tailhdr['headersize'] = tailnbhdrdescr
        # update header
        self.hdr['md5hashtail'] = self.tailhdr['md5hash']
        self.hdr['mtimetail'] = self.tailhdr['mtime']
        self.hdr['tailsize'] = self.tailhdr['tailsize']
        self.hdr['count'] = self.hdr['headsize']+self.tailhdr['tailsize']

    def read_data(self, head_io, tail_io):
        if not head_io is None:
            self.read_head(head_io)

        if not tail_io is None:
            self.read_tail(tail_io)

    def read_head(self, head_io):
        buffer_size = 250 * 1024 * 1024  # 250 MB buffer size
        head_io.seek(0)
        with open(self.filepath, 'rb+') as f:
            # write header
            f.seek(0)
            f.write(self.hdr.tobytes())
            # seek start of head data
            head_io.seek(self.orig_hdr.dtype.itemsize)
            # read head data
            nb_head = (self.hdr['headsize']*self.hdr['itemsize'])
            message = 'Unzipping:%iMB %s' % (
                nb_head / (1024*1024), self.relpath)
            with tqdm(total=nb_head, unit='B', unit_scale=True, desc=message) as pbar:
                while True:
                    buffer = head_io.read(buffer_size)
                    if not buffer:
                        break
                    f.write(buffer)
                    pbar.update(len(buffer))
            f.flush()

    def read_tail(self, tail_io):
        tail_io.seek(0)
        nbhdr = self.hdr.dtype.itemsize
        nbhead = self.hdr['headsize']*self.hdr['itemsize']
        with open(self.filepath, 'rb+') as f:
            f.seek(nbhdr+nbhead)
            tail_io.seek(self.tailhdr.dtype.itemsize)
            f.write(tail_io.read())
            f.flush()

    def compare_hash(self, h1, h2):
        l1 = len(h1)
        l2 = len(h2)
        l = min(l1, l2)
        return h1[:l] == h2[:l]

    ############### WRITE ###############
    def write(self):
        errmsg = ''
        try:
            self.acquire()

            tini = time.time()
            # create header
            mtime = self.hdr['mtime']
            write_head = False
            if self.shareddata.s3write:
                write_head = self.fill_header()

            thread_s3 = threading.Thread(
                target=self.upload, args=(write_head, mtime))
            thread_s3.start()

            thread_flush = threading.Thread(target=self.write_file)
            thread_flush.start()

            # join threads
            thread_s3.join()
            thread_flush.join()

            te = time.time() - tini
            datasize = self.hdr['count'] * self.hdr['itemsize'] / 1000000
            Logger.log.debug('write %s %.2fMB in %.2fs %.2fMBps ' %
                             (self.relpath, datasize, te, datasize / te))
        except Exception as e:
            errmsg = 'Could not write %s\n%s!' % (self.relpath, e)
            Logger.log.error(errmsg)
        finally:
            self.release()
            if errmsg != '':
                raise Exception(errmsg)

    def fill_header(self):

        # partition data by current year
        partdate = pd.Timestamp(datetime(datetime.now().year, 1, 1))
        idx = self.records['date'] >= partdate
        if np.any(idx):  # there is data for the current year
            if np.all(idx):  # all data for the current year
                headsize = self.hdr['count']
                tailsize = 0
                self.hdr['hastail'] = 0
            else:  # some data for the current year
                partid = np.where(idx)[0][0]
                headsize = partid
                tailsize = self.hdr['count'] - partid
                self.hdr['hastail'] = 1
        else:  # there is not data for the current year
            tailsize = 0
            headsize = self.hdr['count']
            self.hdr['hastail'] = 0

        headsize_chg = (headsize != self.hdr['headsize'])
        self.hdr['headsize'] = headsize
        self.hdr['mtimehead'] = self.hdr['mtime']
        self.hdr['mtimetail'] = self.hdr['mtime']
        self.hdr['headsize'] = headsize
        self.hdr['tailsize'] = tailsize
        self.hdr['minchgid'] = self.hdr['count']

        head_modified = (self.hdr['minchgid'] <= self.hdr['headsize'])
        write_head = (head_modified) | (headsize_chg)

        nb_header = int(self.hdrdtype.itemsize)
        nb_head = int(self.hdr['headsize']*self.hdr['itemsize'])
        nb_tail = int(tailsize*self.hdr['itemsize'])

        self.tailhdrdtype = np.dtype(
            {'names': self._tailhdrnames, 'formats': self._tailhdrformats})
        self.tailhdr = np.recarray(shape=(1,), dtype=self.tailhdrdtype)[0]
        self.tailhdr['headersize'] = 80
        _headerdescr = ','.join(self._tailhdrnames) + \
            ';'+','.join(self._tailhdrformats)
        _headerdescr_b = str.encode(
            _headerdescr, encoding='UTF-8', errors='ignore')
        self.tailhdr['headerdescr'] = _headerdescr_b
        self.tailhdr['mtime'] = self.hdr['mtime']
        self.tailhdr['tailsize'] = tailsize

        if write_head:
            self.hdr['md5hashhead'] = 0  # reset the hash value
            nb_records_mb = (nb_header+nb_head)/(1024*1024)
            if nb_records_mb <= 100:
                m = hashlib.md5(self.records[0:self.hdr['headsize']].tobytes())
            else:
                message = 'Creating md5 hash:%iMB %s' % (
                    nb_records_mb, self.relpath)
                block_size = 100 * 1024 * 1024  # or any other block size that you prefer
                chunklines = int(block_size/self.hdr['itemsize'])
                total_lines = self.hdr['headsize']
                read_lines = 0
                nb_total = self.hdr['headsize']*self.hdr['itemsize']
                m = hashlib.md5()
                # Use a with block to manage the progress bar
                with tqdm(total=nb_total, unit='B', unit_scale=True, desc=message) as pbar:
                    # Loop until we have read all the data
                    while read_lines < total_lines:
                        # Read a block of data
                        chunk_size = min(chunklines, total_lines-read_lines)
                        # Update the shared memory buffer with the newly read data
                        m.update(
                            self.records[read_lines:read_lines+chunk_size].tobytes())
                        read_lines += chunk_size  # update the total number of bytes read so far
                        # Update the progress bar
                        pbar.update(chunk_size*self.hdr['itemsize'])
            self.hdr['md5hashhead'] = m.digest()

        if self.hdr['hastail'] == 1:
            self.tailhdr['md5hash'] = 0  # reset the hash value
            self.hdr['md5hashtail'] = 0  # reset the hash value
            nb_records_mb = (nb_tail)/(1024*1024)
            startbyte = nb_header+nb_head
            if nb_records_mb <= 100:
                m = hashlib.md5(
                    self.records[self.hdr['headsize']:self.hdr['count']].tobytes())
            else:
                message = 'Creating md5 hash:%iMB %s' % (
                    nb_records_mb, self.relpath)
                block_size = 100 * 1024 * 1024  # or any other block size that you prefer
                chunklines = int(block_size/self.hdr['itemsize'])
                total_lines = self.tailhdr['tailsize']
                read_lines = 0
                tailstart = self.hdr['headsize']
                nb_total = self.tailhdr['tailsize']*self.hdr['itemsize']
                m = hashlib.md5()
                # Use a with block to manage the progress bar
                with tqdm(total=nb_total, unit='B', unit_scale=True, desc=message) as pbar:
                    # Loop until we have read all the data
                    while read_lines < total_lines:
                        # Read a block of data
                        chunk_size = min(chunklines, total_lines-read_lines)
                        # Update the shared memory buffer with the newly read data
                        m.update(
                            self.records[tailstart+read_lines:tailstart+read_lines+chunk_size].tobytes())
                        read_lines += chunk_size  # update the total number of bytes read so far
                        # Update the progress bar
                        pbar.update(chunk_size*self.hdr['itemsize'])

            self.tailhdr['md5hash'] = m.digest()
            self.hdr['md5hashtail'] = self.tailhdr['md5hash']

        return write_head

    ############### UPLOAD ###############
    def upload(self, write_head, mtime):
        if self.shareddata.s3write:
            if write_head:
                self.upload_head(mtime)

            if self.hdr['hastail'] == 1:
                self.upload_tail(mtime)

    def upload_head(self, mtime):
        # zip head
        gzip_io = io.BytesIO()
        with gzip.GzipFile(fileobj=gzip_io, mode='wb', compresslevel=1) as gz:
            gz.write(self.hdr.tobytes())
            headsize_mb = (self.hdr['headsize'] *
                           self.hdr['itemsize']) / (1024*1024)
            blocksize = 1024*1024*100
            chunklines = int(blocksize/self.hdr['itemsize'])
            descr = 'Zipping:%iMB %s' % (headsize_mb, self.relpath)
            with tqdm(total=headsize_mb, unit='B', unit_scale=True, desc=descr) as pbar:
                written = 0
                while written < self.hdr['headsize']:
                    # write in chunks of max 100 MB size
                    chunk_size = min(chunklines, self.hdr['headsize']-written)
                    gz.write(
                        self.records[written:written+chunk_size].tobytes())
                    written += chunk_size
                    pbar.update(chunk_size*self.hdr['itemsize'])
        S3Upload(gzip_io, str(self.headpath)+'.gzip', mtime)

    def upload_tail(self, mtime):
        gzip_io = io.BytesIO()
        with gzip.GzipFile(fileobj=gzip_io, mode='wb', compresslevel=1) as gz:
            gz.write(self.tailhdr.tobytes())
            gz.write(self.records[self.hdr['headsize']:self.hdr['count']].tobytes())
        S3Upload(gzip_io, str(self.tailpath)+'.gzip', mtime)

    ############### CONVERT ###############
    def records2df(self, records):
        df = pd.DataFrame(records, copy=False)
        dtypes = df.dtypes.reset_index()
        dtypes.columns = ['tag', 'dtype']
        # convert object to string
        string_idx = ['|S' in str(dt) for dt in dtypes['dtype']]
        string_idx = (string_idx) | (dtypes['dtype'] == 'object')
        tags_obj = dtypes['tag'][string_idx].values
        for tag in tags_obj:
            try:
                df[tag] = df[tag].str.decode(encoding='utf-8', errors='ignore')
            except:
                pass
        df = df.set_index(self.index.pkeycolumns)
        return df

    def df2records(self, df):
        check_pkey = True
        if len(self.index.pkeycolumns) == len(df.index.names):
            for k in range(len(self.index.pkeycolumns)):
                check_pkey = (check_pkey) & (
                    df.index.names[k] == self.index.pkeycolumns[k])
        else:
            check_pkey = False
        if not check_pkey:
            raise Exception('First columns must be %s!' %
                            (self.index.pkeycolumns))
        else:
            if self.recdtype is None:
                df = df.reset_index()
                dtypes = df.dtypes.reset_index()
                dtypes.columns = ['tag', 'dtype']
                # convert object to string
                tags_obj = dtypes['tag'][dtypes['dtype'] == 'object'].values
                for tag in tags_obj:
                    try:
                        df[tag] = df[tag].str.encode(
                            encoding='utf-8', errors='ignore')
                    except:
                        Logger.log.error('Could not convert %s!' % (tag))
                    df[tag] = df[tag].astype('|S')
                return np.ascontiguousarray(df.to_records(index=False))
            else:
                df = df.reset_index()
                dtypes = self.recdtype
                rec = np.full((df.shape[0],), fill_value=np.nan, dtype=dtypes)
                for col in dtypes.names:
                    try:
                        if col in df.columns:
                            rec[col] = df[col].astype(dtypes[col])
                    except Exception as e:
                        Logger.log.error(
                            'Could not convert %s!\n%s' % (col, e))

                return rec

    ############### LOCK ###############
    def acquire(self):
        tini = time.time()
        # semaphore is process safe
        telapsed = 0
        hdrptr = self.mutex.__array_interface__['data'][0]
        semseek = 0
        firstcheck = True
        while cpp.long_compare_and_swap(hdrptr, semseek, 0, self.pid) == 0:
            # check if process that locked the mutex is still running
            telapsed = time.time() - tini
            if (telapsed > 15) | ((firstcheck) & (telapsed > 1)):
                lockingpid = self.mutex['pid']
                if not psutil.pid_exists(lockingpid):
                    if cpp.long_compare_and_swap(hdrptr, semseek, lockingpid, self.pid) != 0:
                        break
                if not firstcheck:
                    Logger.log.warning(
                        '%s Waiting for semaphore...' % (self.relpath))
                tini = time.time()
                firstcheck = False
            time.sleep(0.000001)

    def release(self):
        hdrptr = self.mutex.__array_interface__['data'][0]
        semseek = 0
        if cpp.long_compare_and_swap(hdrptr, semseek, self.pid, 0) != 1:
            Logger.log.error(
                '%s Tried to release semaphore without acquire!' % (self.relpath))
            raise Exception('Tried to release semaphore without acquire!')

    ############### SUBSCRIBE ###############

    def subscribe(self, host, port):
        if self.subscription_thread is None:
            self.subscription_thread = threading.Thread(
                target=RealTime.table_subscribe_thread,
                args=(self, host, port)
            )
            self.subscription_thread.start()
            Logger.log.debug('Subscription started!')
        else:
            Logger.log.error('Subscription already running!')
