
# SuperFastPython.com
# load many files concurrently with processes and threads in batch
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
import threading
from cffi import FFI
from tqdm import tqdm
import time
from threading import Thread
from SharedData.Logger import Logger

# USAGE EXAMPLE:
# io_bound(thread_func, iterator, args)
# thread_func:define the task function to run parallel. Ie: read_files,days_trading_from_to
# iteration: single iteration items of parallel task
# args: commom task variables

# thread_func EXAMPLES

# IO BOUND EXAMPLE
# def read_files(iteration, args):
#     fileid = iteration[0]
#     file_list = args[0]
#     fpath = file_list[fileid]
#     df = pd.read_csv(fpath)
#     return [df]

# CPU BOUND EXAMPLE
# def days_trading_from_to(iteration, args):
#     cal = iteration[0]
#     start = iteration[1]
#     end = iteration[2]
#     calendars = args[0]
#     idx = (calendars[cal]>=start) & ((calendars[cal]<=end))
#     return [np.count_nonzero(idx)]

############## MULTI PROCESS MULTI THREAD ORDERED ##############


def io_bound(thread_func, iterator, args, maxproc=None, maxthreads=4):
    results = []
    # determine chunksize
    niterator = len(iterator)
    if niterator > 0:
        n_workers = multiprocessing.cpu_count() - 2
        n_workers = min(n_workers, niterator)
        if not maxproc is None:
            n_workers = min(n_workers, maxproc)
        chunksize = round(niterator / n_workers)
        # create the process pool
        with ProcessPoolExecutor(n_workers) as executor:
            futures = list()
            # split the load operations into chunks
            for i in range(0, niterator, chunksize):
                # select a chunk of filenames
                proc_iterator = iterator[i:(i + chunksize)]
                # submit the task
                future = executor.submit(io_bound_process,
                                         thread_func, proc_iterator, args, maxthreads)
                futures.append(future)
            # process all results
            for future in futures:
                # open the file and load the data
                res = future.result()
                results = [*results, *res]
    return results


def io_bound_process(thread_func, proc_iterator, args, maxthreads):
    results = []
    # create a thread pool
    nthreads = len(proc_iterator)
    nthreads = min(nthreads, maxthreads)
    if nthreads > 0:
        with ThreadPoolExecutor(nthreads) as exe:
            # load files
            futures = [exe.submit(thread_func, iteration, args)
                       for iteration in proc_iterator]
            # collect data
            for future in futures:
                res = future.result()
                results = [*results, *res]

    return results

############## MULTI PROCESS MULTI THREAD UNORDERED ##############


def io_bound_unordered(thread_func, iterator, args, maxproc=None, maxthreads=4):
    results = []
    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()
    niterator = len(iterator)
    nworkers = multiprocessing.cpu_count() - 2
    if not maxproc is None:
        nworkers = min(nworkers, maxproc)
    if (niterator <= nworkers) \
            | (niterator <= int(nworkers*maxthreads)):
        maxthreads = 1
        nworkers = niterator

    workers = [multiprocessing.Process(target=multi_thread_worker_process,
                                       args=(thread_func, input_queue, output_queue, args, maxthreads))
               for _ in range(nworkers)]

    for w in workers:
        w.start()

    for i in range(niterator):
        input_queue.put(iterator.iloc[i])

    desc = '%s(%i proc,%i threads)' % (thread_func.__name__,nworkers,maxthreads)
    for i in tqdm(range(niterator), desc=desc):
        results.extend(output_queue.get())

    # Signal processes to terminate
    for _ in range(nworkers):
        input_queue.put(None)

    for w in workers:
        w.join()

    if not input_queue.empty():
        raise Exception('Input queue not totally consumed!')
    
    if not output_queue.empty():
        raise Exception('Output queue not totally consumed!')

    return results


def multi_thread_worker_process(thread_func, input_queue, output_queue, args, nthreads):
    threads = [threading.Thread(target=worker_thread,
                                args=(thread_func, input_queue, output_queue, args))
               for _ in range(nthreads)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()


def worker_thread(thread_func, input_queue, output_queue, args):
    while True:
        iteration = input_queue.get()
        if iteration is None:
            break
        try:
            result = thread_func(iteration, args)
        except Exception as e:
            Logger.log.error('Error in worker %s : %s ,%s\n' \
                             % thread_func.__name__, str(iteration),str(e))
        output_queue.put(result)

################# MULTI PROCESS ORDERED #################


def cpu_bound(thread_func, iterator, args, maxproc=None):
    results = []
    # determine chunksize
    niterator = len(iterator)
    if niterator > 0:
        n_workers = multiprocessing.cpu_count() - 2
        n_workers = min(n_workers, niterator)
        if not maxproc is None:
            n_workers = min(n_workers, maxproc)
        chunksize = round(niterator / n_workers)
        # create the process pool
        with ProcessPoolExecutor(n_workers) as executor:
            futures = list()
            # split the load operations into chunks
            for i in range(0, niterator, chunksize):
                # select a chunk of filenames
                proc_iterator = iterator[i:(i + chunksize)]
                # submit the task
                future = executor.submit(
                    cpu_bound_process, thread_func, proc_iterator, args)
                futures.append(future)
            # process all results
            for future in futures:
                # open the file and load the data
                res = future.result()
                results = [*results, *res]
    return results


def cpu_bound_process(thread_func, proc_iterator, args):
    results = []
    for iteration in proc_iterator:
        res = thread_func(iteration, args)
        results = [*results, *res]
    return results

############## MULTI PROCESS UNORDERED ##############


def cpu_bound_unordered(thread_func, iterator, args, maxproc=None):
    results = []
    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()
    niterator = len(iterator)
    nworkers = multiprocessing.cpu_count() - 2
    nworkers = min(nworkers, niterator)
    if not maxproc is None:
        nworkers = min(nworkers, maxproc)

    workers = [multiprocessing.Process(target=single_thread_worker_process,
                                       args=(thread_func, input_queue, output_queue, args))
               for _ in range(nworkers)]

    for w in workers:
        w.start()

    for i in range(niterator):
        input_queue.put(iterator[i])

    for i in tqdm(range(niterator), desc='cpu_bound_unordered:'):
        results.extend(output_queue.get())

    # Signal processes to terminate
    for _ in range(niterator):
        input_queue.put(None)

    for w in workers:
        w.join()

    return results


def single_thread_worker_process(thread_func, input_queue, output_queue, args):
    while True:
        iteration = input_queue.get()
        if iteration is None:
            break
        result = thread_func(iteration, args)
        output_queue.put(result)
