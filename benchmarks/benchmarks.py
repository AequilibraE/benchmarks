import time
from contextlib import contextmanager

@contextmanager
def benchmark(results_dict, key):
    """
    A context manager for performance benchmarking.

    Args:
        results_dict: Dictionary to store the benchmark results
        key: Key under which to store the execution time

    Example:
        results = {}
        with benchmark(results, 'operation_1'):
            # code to benchmark
        print(results)  # {'operation_1': 0.123}
    """
    start_time = time.perf_counter()
    try:
        yield
    finally:
        end_time = time.perf_counter()
        results_dict[key] = end_time - start_time


