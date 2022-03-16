import multiprocessing
from typing import List


def get_hunksize_possible_vals() -> List[str]:
    return [str(2448 * i) for i in range(1, 20)]


def get_possible_nthreads() -> List[str]:
    return list(map(str, range(1, multiprocessing.cpu_count() + 1)))
