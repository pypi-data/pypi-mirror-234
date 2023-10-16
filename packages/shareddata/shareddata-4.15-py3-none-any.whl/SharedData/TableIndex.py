import numpy as np
import os
import time
from multiprocessing import shared_memory


import SharedData.TableIndexJit as TableIndexJit
from SharedData.TableIndexJit import *
from SharedData.Logger import Logger


class TableIndex:

    def __init__(self, table):
        self.table = table
        self.shareddata = self.table.shareddata

        self.initialized = False

        # primary key hash table
        self.pkeycolumns = TableIndex.get_pkeycolumns(self.table.database)
        self.pkeystr = '_'.join(self.pkeycolumns)
        self.pkey = np.ndarray([])
        # date index
        self.dateiniidx = np.ndarray([])
        self.dateendidx = np.ndarray([])
        # symbol index
        self.symbollastidx = np.ndarray([])
        self.symbolprevidx = np.ndarray([])
        # portfolio index
        self.portlastidx = np.ndarray([])
        self.portprevidx = np.ndarray([])        

    def initialize(self):
        errmsg = ''
        try:
            self.get_functions()

            self.malloc()

            # check if index was created
            # count = np.sum(self.pkey != -1)
            # if self.table.hdr['count'] != count:
            if self.table.hdr['isidxcreated'] == 0:
                self.create_index()
                
            self.initialized = True
        except Exception as e:
            errmsg = 'Failed to intialize index for %s!\n%s' % (self.table.relpath, str(e))            
            self.initialized = False
        finally:            
            if not self.initialized:
                Logger.log.error(errmsg)
                raise Exception(errmsg)

    def get_functions(self):
        # primary key & index functions
        self.create_index_func = None
        self.upsert_func = None
        self.get_loc_func = None

        create_pkey_fname = 'create_pkey_' + self.pkeystr + '_jit'
        if hasattr(TableIndexJit, create_pkey_fname):
            self.create_index_func = getattr(TableIndexJit, create_pkey_fname)
        else:
            raise Exception('create_pkey function not found for database %s!'
                            % (self.table.database))

        upsert_fname = 'upsert_' + self.pkeystr + '_jit'
        if hasattr(TableIndexJit, upsert_fname):
            self.upsert_func = getattr(TableIndexJit, upsert_fname)
        else:
            raise Exception('upsert function not found for database %s!'
                            % (self.table.database))

        get_loc_fname = 'get_loc_' + self.pkeystr + '_jit'
        if hasattr(TableIndexJit, get_loc_fname):
            self.get_loc_func = getattr(TableIndexJit, get_loc_fname)
        else:
            raise Exception('get_loc function not found for database %s!'
                            % (self.table.database))        

    def malloc(self):
        shm_name = self.table.shm_name
        self.malloc_pkey(shm_name)
        if 'date' in self.pkeystr:
            self.malloc_dateidx(shm_name)
        if 'symbol' in self.pkeystr:
            self.malloc_symbolidx(shm_name)
        if 'portfolio' in self.pkeystr:
            self.malloc_portfolioidx(shm_name)        

    def malloc_pkey(self, shm_name):
        keysize = int(self.table.records.size*3)
        keysize_bytes = int(keysize * 8)
        
        iscreate = False        
        if self.table.type=='MEMORY':
            [self.pkeyshm, ismalloc] = self.shareddata.malloc(shm_name+'#pkey')
            if not ismalloc:
                [self.pkeyshm, ismalloc] = self.shareddata.malloc(shm_name+'#pkey',
                    create=True, size=keysize_bytes)
                iscreate = True
            self.pkey = np.ndarray((keysize,), dtype=np.int64,
                               buffer=self.pkeyshm.buf)
        elif self.table.type=='DISK':
            self.pkeypath = str(self.table.filepath)\
                .replace('data.bin', 'pkey.bin')
            
            resetfile = False            
            if (not os.path.exists(self.pkeypath)):
                resetfile = True                
            elif os.path.getsize(self.pkeypath) != keysize_bytes:
                resetfile = True

            if resetfile:
                self.create_file(self.pkeypath,keysize_bytes)
                iscreate = True

            if os.path.getmtime(self.table.filepath) > os.path.getmtime(self.pkeypath):
                iscreate = True

            self.pkey = self.shareddata.memmap(self.pkeypath, np.int64, 0, keysize)

        if iscreate:
            self.table.hdr['isidxcreated'] = 0
            self.pkey[:] = -1

    def malloc_dateidx(self, shm_name):
        # date index
        dtunit = str(self.table.records.dtype[0]).split('[')[-1].split(']')[0]
        if dtunit == 'ns':
            self.dateunit = 24*60*60*1000*1000*1000
        else:
            raise Exception('Only dates with ns precision are supported!')
        maxdate = np.datetime64('2070-01-01', 'D')
        dateidxsize = maxdate.astype(np.int64)
        dateidxsize_bytes = int(dateidxsize * 8)

        iscreate = False
        if self.table.type=='MEMORY':
            [self.dateidxshm, ismalloc] = self.shareddata.malloc(shm_name+'#dateidx')
            if not ismalloc:
                [self.dateidxshm, ismalloc] = self.shareddata.malloc(shm_name+'#dateidx',
                                                                    create=True, size=int(dateidxsize_bytes*2))
                iscreate = True

            self.dateiniidx = np.ndarray(
                (dateidxsize,), dtype=np.int64, buffer=self.dateidxshm.buf)
            self.dateendidx = np.ndarray((dateidxsize,), dtype=np.int64, buffer=self.dateidxshm.buf,
                                        offset=dateidxsize_bytes)
        elif self.table.type=='DISK':
            self.dateidxpath = str(self.table.filepath).replace('data.bin', 'dateidx.bin')
            if not os.path.exists(self.dateidxpath):
                self.create_file(self.dateidxpath,dateidxsize_bytes)
                iscreate = True                
            elif os.path.getmtime(self.table.filepath) > os.path.getmtime(self.dateidxpath):
                iscreate = True
            
            self.dateiniidx = self.shareddata.memmap(self.dateidxpath, np.int64, 0, dateidxsize)
            self.dateendidx = self.shareddata.memmap(self.dateidxpath, np.int64, dateidxsize_bytes, dateidxsize)

        if iscreate:
            self.table.hdr['isidxcreated'] = 0
            self.dateiniidx[:] = -1
            self.dateendidx[:] = -1

    def malloc_symbolidx(self, shm_name):
        hashtblsize = int(self.table.records.size*3)
        hashtblsize_bytes = int(hashtblsize * 8)
        listsize = self.table.records.size
        listsize_bytes = int(listsize * 8)
        size_bytes = int(hashtblsize_bytes+listsize_bytes)

        # symbol index
        iscreate = False
        if self.table.type=='MEMORY':
            [self.symbolidxshm, ismalloc] = self.shareddata.malloc(
                shm_name+'#symbolidx')
            if not ismalloc:
                [self.symbolidxshm, ismalloc] = self.shareddata.malloc(shm_name+'#symbolidx',
                    create=True, size=size_bytes)
                iscreate = True

            self.symbollastidx = np.ndarray(
                (hashtblsize,), dtype=np.int64, buffer=self.symbolidxshm.buf)
            self.symbolprevidx = np.ndarray((listsize,), dtype=np.int64, buffer=self.symbolidxshm.buf,
                                            offset=hashtblsize_bytes)
        elif self.table.type=='DISK':
            self.symbolidxpath = str(self.table.filepath).replace('data.bin', 'symbolidx.bin')            
            resetfile = False            
            if (not os.path.exists(self.symbolidxpath)):
                resetfile = True                
            elif os.path.getsize(self.symbolidxpath) != size_bytes:
                resetfile = True
            if resetfile:
                self.create_file(self.symbolidxpath,size_bytes)
                iscreate = True                        
            elif os.path.getmtime(self.table.filepath) > os.path.getmtime(self.symbolidxpath):
                iscreate = True

            self.symbollastidx = self.shareddata.memmap(self.symbolidxpath, np.int64, 0, hashtblsize)
            self.symbolprevidx = self.shareddata.memmap(self.symbolidxpath, np.int64, hashtblsize_bytes, listsize)

        if iscreate:
            self.table.hdr['isidxcreated'] = 0
            self.symbollastidx[:] = -1
            self.symbolprevidx[:] = -1

    def malloc_portfolioidx(self, shm_name):
        hashtblsize = int(self.table.records.size*3)
        hashtblsize_bytes = int(hashtblsize * 8)
        listsize = self.table.records.size
        listsize_bytes = int(listsize * 8)
        size_bytes = int(hashtblsize_bytes+listsize_bytes)

        # portfolio index
        iscreate = False
        if self.table.type=='MEMORY':
            [self.portidxshm, ismalloc] = self.shareddata.malloc(
                shm_name+'#portidx')
            if not ismalloc:
                [self.portidxshm, ismalloc] = self.shareddata.malloc(shm_name+'#portidx',
                    create=True, size=size_bytes)
                iscreate = True

            self.portlastidx = np.ndarray(
                (hashtblsize,), dtype=np.int64, buffer=self.portidxshm.buf)
            self.portprevidx = np.ndarray((listsize,), dtype=np.int64, buffer=self.portidxshm.buf,
                                        offset=hashtblsize_bytes)
        elif self.table.type=='DISK':
            self.portidxpath = str(self.table.filepath).replace('data.bin', 'portidx.bin')
            resetfile = False            
            if (not os.path.exists(self.portidxpath)):
                resetfile = True                
            elif os.path.getsize(self.portidxpath) != size_bytes:
                resetfile = True
            if resetfile:
                self.create_file(self.portidxpath,size_bytes)
                iscreate = True                        
            elif os.path.getmtime(self.table.filepath) > os.path.getmtime(self.portidxpath):
                iscreate = True

            self.portlastidx = self.shareddata.memmap(self.portidxpath, np.int64, 0, hashtblsize)
            self.portprevidx = self.shareddata.memmap(self.portidxpath, np.int64, hashtblsize_bytes, listsize)

        if iscreate:
            self.table.hdr['isidxcreated'] = 0
            self.portlastidx[:] = -1
            self.portprevidx[:] = -1    

    def create_index(self,start=0,update=False):
        ti = time.time()
        if self.table.records.count > 0:
            if not update:
                print('Creating index %s %i lines...' %
                    (self.table.relpath, self.table.records.count))                
            else:
                print('Updating index %s %i lines...' %
                    (self.table.relpath, self.table.records.count))
            time.sleep(0.001)
    
            self.table.hdr['isidxcreated'] = 0
            if self.table.type=='DISK':                
                self.table.shf_hdr.flush()

            # TODO: CREATE AN UPDATE METHOD
            start = 0
            self.pkey[:] = -1
            self.dateiniidx[:] = -1
            self.dateendidx[:] = -1
            arr = self.table.records
            if 'date_portfolio_symbol' in self.pkeystr:
                self.symbollastidx[:] = -1
                self.symbolprevidx[:] = -1
                self.portlastidx[:] = -1
                self.portprevidx[:] = -1
                success = self.create_index_func(arr, self.table.records.count, self.pkey,
                                                self.dateiniidx, self.dateendidx, self.dateunit, \
                                                self.portlastidx, self.portprevidx, \
                                                self.symbollastidx, self.symbolprevidx,  start)
            elif 'date_symbol' in self.pkeystr:
                self.symbollastidx[:] = -1
                self.symbolprevidx[:] = -1
                success = self.create_index_func(arr, self.table.records.count, self.pkey,
                                                 self.dateiniidx, self.dateendidx, self.dateunit, \
                                                self.symbollastidx, self.symbolprevidx, start)
            elif 'date_portfolio' in self.pkeystr:
                self.portlastidx[:] = -1
                self.portprevidx[:] = -1
                success = self.create_index_func(arr, self.table.records.count, self.pkey,
                                                self.dateiniidx, self.dateendidx, self.dateunit, \
                                                self.portlastidx, self.portprevidx, start)
            
            if not success:
                Logger.log.critical('Duplicated Index %s!!!' %
                                    self.table.relpath)
                raise Exception('Duplicated Index %s!!!' % self.table.relpath)
            
            self.table.hdr['isidxcreated'] = 1
            if self.table.type=='DISK':
                self.flush()                
                self.table.shf_hdr.flush()

            print('Creating index %s %i lines/s DONE!' %
                  (self.table.relpath, self.table.records.count/(time.time()-ti)))

    def update_index(self, start):                
        self.create_index(start,update=True)        

    def sort_index(self, shnumpy, start=0):
        
        try:
            self.table.acquire()
            
            keys = tuple(shnumpy[column][start:]
                         for column in self.pkeycolumns[::-1])
            idx = np.lexsort(keys)

            shift_idx = np.roll(idx, 1)
            if len(shift_idx) > 0:
                shift_idx[0] = -1
                idx_diff = idx - shift_idx
                unsortered_idx = np.where(idx_diff != 1)[0]
                if np.where(idx_diff != 1)[0].any():
                    _minchgid = np.min(unsortered_idx) + start
                    shnumpy.minchgid = _minchgid
                    shnumpy[start:] = shnumpy[start:][idx]                    
                    self.update_index(_minchgid)

        except Exception as e:
            Logger.log.error('Error sorting index!\n%s' % (e))
        finally:
            self.table.release()

    def create_file(self,fpath,size):
        with open(fpath, 'wb') as f:
            # Seek to the end of the file
            f.seek(size-1)
            # Write a single null byte to the end of the file
            f.write(b'\x00')
            if os.name == 'posix':
                os.posix_fallocate(f.fileno(), 0, size)
            elif os.name == 'nt':
                pass # TODO: implement windows file allocation

    def flush(self):
        mtime = self.table.hdr['mtime']
        self.pkey.flush()        
        os.utime(self.pkeypath, (mtime, mtime))
        if 'date' in self.pkeystr:
            self.dateiniidx.flush()
            self.dateendidx.flush()
            os.utime(self.dateidxpath, (mtime, mtime))
        if 'symbol' in self.pkeystr:
            self.symbollastidx.flush()
            self.symbolprevidx.flush()
            os.utime(self.symbolidxpath, (mtime, mtime))
        if 'portfolio' in self.pkeystr:
            self.portlastidx.flush()
            self.portprevidx.flush()
            os.utime(self.portidxpath, (mtime, mtime))
        
    def free(self):
        del self.pkey
        del self.dateiniidx
        del self.dateendidx
        if 'symbol' in self.pkeystr:
            del self.symbollastidx
            del self.symbolprevidx
        if 'portfolio' in self.pkeystr:
            del self.portlastidx
            del self.portprevidx

    @staticmethod
    def get_pkeycolumns(database):
        if database == 'MarketData':
            return ['date', 'symbol']

        elif database == 'Relationships':
            return ['date', 'symbol1', 'symbol2']

        elif database == 'Portfolios':
            return ['date', 'portfolio']

        elif database == 'Signals':
            return ['date', 'portfolio', 'symbol']

        elif database == 'Risk':
            return ['date', 'portfolio', 'symbol']

        elif database == 'Positions':
            return ['date', 'portfolio', 'symbol']

        elif database == 'Orders':
            return ['date', 'portfolio', 'symbol', 'clordid']

        elif database == 'Trades':
            return ['date', 'portfolio', 'symbol', 'tradeid']

        else:
            raise Exception('Database not implemented!')
