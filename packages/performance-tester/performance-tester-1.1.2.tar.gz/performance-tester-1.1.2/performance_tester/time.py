import time
import statistics
from functools import wraps


def measure_execution_time(num_exec: int = 5):
    def measure_execution_time_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed_time_lst = []
            for _ in range(num_exec):
                start_time = time.perf_counter()
                result = func(*args, **kwargs)
                end_time = time.perf_counter()
                elapsed_time = end_time - start_time
                elapsed_time_lst.append(elapsed_time)
            print(f"{num_exec} loops:")
            print(f"mean: {statistics.mean(elapsed_time_lst)} sec.")
            print(f"std : {statistics.stdev(elapsed_time_lst)} sec.")
            print(f"max : {max(elapsed_time_lst)} sec.")
            print(f"min : {min(elapsed_time_lst)} sec.")
            return result
        return wrapper
    return measure_execution_time_wrapper
