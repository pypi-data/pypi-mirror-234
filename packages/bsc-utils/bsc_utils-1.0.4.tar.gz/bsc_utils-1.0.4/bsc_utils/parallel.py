from concurrent.futures import (
    Executor, ProcessPoolExecutor, ThreadPoolExecutor, as_completed
)

from tqdm import tqdm


def parallel(
    func, params_list, executor_type: Executor, max_workers: int = None
):

    num_iter = len(params_list)

    if isinstance(executor_type, ThreadPoolExecutor):
        if not max_workers:
            max_workers = 100
        if max_workers > num_iter:
            max_workers = num_iter

    elif isinstance(executor_type, ProcessPoolExecutor):
        pass  # concurrent.futures default is already max CPU number

    with executor_type(max_workers=max_workers) as executor:
        futures = [executor.submit(func, **p) for p in params_list]
        results = list(
            tqdm(
                [future.result() for future in as_completed(futures)],
                total=num_iter,
            )
        )
        return results
