import multiprocessing
from typing import List

from chdman_gui.utils import get_hd_templates


def get_hunksize_possible_vals() -> List[str]:
    return [str(2448 * i) for i in range(1, 20)]


def get_possible_nthreads() -> List[str]:
    return list(map(str, range(1, multiprocessing.cpu_count() + 1)))


def get_hd_templates_possible_vals() -> List[str]:
    data = get_hd_templates()
    return [
        f"{line['Manufacturer']} {line['Model']} - {line['Total Size'].replace(' ', '')}"
        for line in data
    ]
