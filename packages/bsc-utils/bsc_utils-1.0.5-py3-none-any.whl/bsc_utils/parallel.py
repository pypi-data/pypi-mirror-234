import os
from concurrent.futures import (
    Executor, ProcessPoolExecutor, ThreadPoolExecutor, as_completed
)

from tqdm import tqdm


def parallel(func, params_list, executor_type: Executor):

    num_iter = len(params_list)

    if executor_type == ThreadPoolExecutor:
        max_workers = int(os.getenv('NUM_THREADS', 100))

        if max_workers > num_iter:
            max_workers = num_iter

    elif executor_type == ProcessPoolExecutor:
        max_workers = os.getenv(
            'NUM_PROCESSORS'
        )  # concurrent.futures default is already max CPU number
        if max_workers:
            max_workers = int(max_workers)

    with executor_type(max_workers=max_workers) as executor:
        futures = [executor.submit(func, **p) for p in params_list]
        results = []
        with tqdm(total=num_iter) as pbar:
            for future in as_completed(futures):
                results.append(future.result())
                pbar.update()

        return results
