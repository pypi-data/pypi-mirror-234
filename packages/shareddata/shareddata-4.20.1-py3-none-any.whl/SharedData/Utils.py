import os
from multiprocessing import resource_tracker

# TODO: CHANGE FIX REGISTER/UNREGISTER TO INCLUDE SEMAPHORES
def remove_shm_from_resource_tracker():
    """Monkey-patch multiprocessing.resource_tracker so SharedMemory won't be tracked

    More details at: https://bugs.python.org/issue38119
    """

    def fix_register(name, rtype):
        if rtype == "shared_memory":
            return
        return resource_tracker._resource_tracker.register(self, name, rtype)
    resource_tracker.register = fix_register

    def fix_unregister(name, rtype):
        if rtype == "shared_memory":
            return
        return resource_tracker._resource_tracker.unregister(self, name, rtype)
    resource_tracker.unregister = fix_unregister

    if "shared_memory" in resource_tracker._CLEANUP_FUNCS:
        del resource_tracker._CLEANUP_FUNCS["shared_memory"]


if os.name == 'posix':
    from cffi import FFI
    # atomic semaphore operation
    ffi = FFI()
    ffi.cdef("""    
    unsigned char long_compare_and_swap(long mem_addr, long seek, long oldvalue, long newvalue);
    """)
    cpp = ffi.verify("""    
    unsigned char long_compare_and_swap(long mem_addr, long seek, long oldvalue, long newvalue) {
        long * mem_ptr = (long *) mem_addr;
        mem_ptr += seek;
        return __sync_bool_compare_and_swap(mem_ptr, oldvalue, newvalue);
    };    
    """)

elif os.name == "nt": 
    import sys
    sys.path.append(os.path.dirname(__file__))   
    import sharedmutexwin as cpp
    


