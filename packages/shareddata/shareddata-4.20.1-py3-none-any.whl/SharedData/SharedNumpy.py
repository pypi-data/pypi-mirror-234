import pandas as pd
import numpy as np
import time
from datetime import datetime
from tqdm import tqdm

from SharedData.Logger import Logger
from SharedData.TableIndexJit import get_symbol_loc, get_portfolio_loc


class SharedNumpy(np.ndarray):

    def __new__(cls, type, *args, **kwargs):
        if type == 'MEMORY':
            obj = np.ndarray.__new__(cls, *args, **kwargs)
            obj.table = None
            return obj
        elif type == 'DISK':            
            memmap = args[0]
            obj = memmap.view(cls)
            obj.memmap = memmap
            obj.table = None
            return obj
        else:
            raise Exception('Unknown type %s!' % (type))

    def subscribe(self, host, port):
        self.table.subscribe(host, port)

    def preallocate(self):
        # TODO: REVISE PREALLOCATE NOT CONSUMING MEMORY
        arr = super().__getitem__(slice(0, self.size))
        sizeb = self.size*self.itemsize
        sizemb = sizeb / 10**6
        if sizemb > 500:
            blocksize = int(1000*10**6/self.itemsize)
            descr = 'Preallocating:%iMB %s' % (sizemb, self.table.relpath)
            with tqdm(total=sizeb, unit='B', unit_scale=True, desc=descr) as pbar:
                allocated = 0
                while allocated < self.size:
                    # write in chunks of max 100 MB size
                    chunk_size = min(blocksize, self.size-allocated)
                    arr['mtime'][allocated:chunk_size] = np.datetime64('NaT')
                    allocated += chunk_size
                    pbar.update(chunk_size*self.itemsize)
        else:
            arr['mtime'][:] = np.datetime64('NaT')

    def free(self):
        self.table.free()

    def write(self):
        if self.count > 0:
            self.table.write()

    ############################## KEYLESS OPERATIONS ########################################

    def insert(self, new_records, acquire=True):        
        errmsg = ''
        try:
            if acquire:
                self.table.acquire()
                    
            nrec = new_records.size
            _count = self.count
            if (_count + nrec <= self.size):
                # convert new_records
                if (self.dtype != new_records.dtype):
                    new_records = self.convert(new_records)
                # fill mtime
                nidx = np.isnat(new_records['mtime'])
                if nidx.any():
                    new_records['mtime'][nidx] = time.time_ns()

                arr = super().__getitem__(slice(0, self.size))
                arr[_count:_count+nrec] = new_records
                self.count = _count + nrec
                self.mtime = datetime.now().timestamp()
            else:
                errmsg = 'Table max size reached!'
                Logger.log.error(errmsg)
        except Exception as e:
            errmsg = 'Error inserting %s!\n%s' % (self.table.relpath, str(e))
            Logger.log.error(errmsg)
        finally:
            if acquire:
                self.table.release()
            if errmsg:
                raise Exception(errmsg)

    ############################## PRIMARY KEY OPERATIONS ########################################
    def upsert(self, new_records):

        if new_records.size > 0:

            # convert to same dtype record
            if isinstance(new_records, pd.DataFrame):
                new_records = self.table.df2records(new_records)
            elif (self.dtype != new_records.dtype):
                new_records = self.convert(new_records)

            # fill mtime
            nidx = np.isnat(new_records['mtime'])
            if nidx.any():
                new_records['mtime'][nidx] = time.time_ns()

            # single record to array
            if new_records.shape == ():
                new_records = np.array([new_records])

            try:
                success = True
                self.table.acquire()
                # upsert
                minchgid = self.count
                arr = super().__getitem__(slice(0, self.size))
                if 'date_portfolio_symbol' in self.table.index.pkeystr:
                    self.count, minchgid = self.index.upsert_func(
                        arr, self.count, new_records, self.pkey,
                        self.index.dateiniidx, self.index.dateendidx, self.index.dateunit,
                        self.index.portlastidx, self.index.portprevidx,
                        self.index.symbollastidx, self.index.symbolprevidx)                    
                elif 'date_symbol' == self.table.index.pkeystr:
                    self.count, minchgid = self.index.upsert_func(
                        arr, self.count, new_records, self.pkey,
                        self.index.dateiniidx, self.index.dateendidx,
                        self.index.symbollastidx, self.index.symbolprevidx,
                        self.index.dateunit)
                elif 'date_portfolio' == self.table.index.pkeystr:
                    self.count, minchgid = self.index.upsert_func(
                        arr, self.count, new_records, self.pkey,
                        self.index.dateiniidx, self.index.dateendidx,
                        self.index.portlastidx, self.index.portprevidx,
                        self.index.dateunit)
                else:
                    self.count, minchgid = self.index.upsert_func(
                        arr, self.count, new_records, self.pkey,
                        self.index.dateiniidx, self.index.dateendidx, self.index.dateunit)

                minchgid = int(minchgid)
                self.minchgid = minchgid
                self.mtime = datetime.now().timestamp()

            except Exception as e:
                Logger.log.error('Error upserting %s!\n%s' %
                                 (self.table.relpath, str(e)))
                success = False
            finally:
                self.table.release()
                # table full
                if self.count == self.size:                    
                    Logger.log.warning('Table %s is full!' %
                                     (self.table.relpath))                    
                if not success:
                    raise Exception('Error upserting %s!' %
                                 (self.table.relpath))

            return minchgid
        return self.count

    def sort_index(self, start=0):
        self.index.sort_index(self, start)

    def get_loc(self, keys):
        success = False
        try:
            self.table.acquire()
            loc = self.index.get_loc_func(self[:], self.pkey, keys).astype(int)
            success = True
        except Exception as e:
            Logger.log.error('Error getting loc for %s!\n%s' %
                             (self.table.relpath, str(e)))
            loc = np.array([])
        finally:
            self.table.release()
            if not success:
                raise Exception('Error getting loc for %s!' % (self.table.relpath))
        return loc

    def get_date_loc(self, date):
        success = False
        try:
            self.table.acquire()
            if isinstance(date, np.datetime64):
                date = pd.Timestamp(date)
            dtint = int(date.value/24/60/60/10**9)
            dtiniid = self.index.dateiniidx[dtint]
            dtendid = self.index.dateendidx[dtint]
            success = True
        except Exception as e:
            Logger.log.error('Error getting date_loc for %s!\n%s' %
                             (self.table.relpath, str(e)))
        finally:
            self.table.release()
            if not success:
                raise Exception('Error getting date_loc for %s!' % (self.table.relpath))
        return [dtiniid, dtendid+1]

    def get_symbol_loc(self, symbol, maxids=0):
        success = False
        try:
            self.table.acquire()
            if not isinstance(symbol, bytes):
                symbol = symbol.encode('utf-8')
            symbolhash = hash(symbol)
            loc = get_symbol_loc(self[:], self.index.symbollastidx,
                                 self.index.symbolprevidx, symbol, symbolhash, maxids)
            success = True
        except Exception as e:
            Logger.log.error('Error getting symbol_loc for %s!\n%s' %
                             (self.table.relpath, str(e)))
        finally:
            self.table.release()
            if not success:
                raise Exception('Error getting symbol_loc for %s!' %
                                (self.table.relpath))
        return loc

    def get_portfolio_loc(self, portfolio, maxids=0):
        success = False
        try:
            self.table.acquire()
            if not isinstance(portfolio, bytes):
                portfolio = portfolio.encode('utf-8')
            portfoliohash = hash(portfolio)
            loc = get_portfolio_loc(
                self[:], self.index.portlastidx, self.index.portprevidx, portfolio, portfoliohash, maxids)
            success = True
        except Exception as e:
            Logger.log.error('Error getting portfolio_loc for %s!\n%s' %
                             (self.table.relpath, str(e)))
        finally:
            self.table.release()
            if not success:
                raise Exception('Error getting portfolio_loc for %s!' % 
                                (self.table.relpath))
        return loc
    

    ############################## CONVERSION ##############################

    def records2df(self, records):
        return self.table.records2df(records)

    def df2records(self, df):
        return self.table.df2records(df)

    def convert(self, new_records):
        rec = np.full((new_records.size,), fill_value=np.nan, dtype=self.dtype)
        for col in self.dtype.names:
            if col in new_records.dtype.names:
                try:
                    rec[col] = new_records[col].astype(self.dtype[col])
                except:
                    Logger.log.error('Could not convert %s!' % (col))
        return rec

    ############################## GETTERS / SETTERS ##############################

    def __getitem__(self, key):
        if hasattr(self, 'table'):
            arr = super().__getitem__(slice(0, self.count))  # slice arr
            if self.count > 0:
                return arr.__getitem__(key)
            else:
                return arr
        else:
            return super().__getitem__(key)

    @property
    def count(self):
        return self.table.hdr['count']

    @count.setter
    def count(self, value):
        self.table.hdr['count'] = value

    @property
    def mtime(self):
        return self.table.hdr['mtime']

    @mtime.setter
    def mtime(self, value):
        self.table.hdr['mtime'] = value

    @property
    def minchgid(self):
        return self.table.hdr['minchgid']

    @minchgid.setter
    def minchgid(self, value):
        value = min(value, self.table.hdr['minchgid'])
        self.table.hdr['minchgid'] = value

    @property
    def index(self):
        return self.table.index

    @index.setter
    def index(self, value):
        self.table.index = value

    @property
    def pkey(self):
        return self.table.index.pkey

    @pkey.setter
    def pkey(self, value):
        self.table.index.pkey = value
