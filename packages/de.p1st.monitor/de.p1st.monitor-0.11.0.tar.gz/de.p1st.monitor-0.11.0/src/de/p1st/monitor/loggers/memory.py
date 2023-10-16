#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

import psutil
from de.p1st.monitor import datetime_util

from de.p1st.monitor.logger import Logger
from de.p1st.monitor.warn_data import WarnData


class MemoryLogger(Logger):
    def __init__(self,
                 warn_if_above: float = 1.0,
                 warn_threshold: int = 1,
                 warn_data_range: int = 1,
                 ):
        # The space between memory is at `self.warn_if_above` and memory is full at `1.0`.
        buffer = 1 - warn_if_above
        critical_if_above = warn_if_above + 0.5 * buffer
        super().__init__(warn_threshold,
                         warn_data_range,
                         warn_if_above,
                         critical_if_above)
        self.warn_if_above = warn_if_above

    def get_warn_data(self, data: list[any]) -> WarnData:
        used_mb = data[1]
        total_available_mb = data[3]
        used = used_mb / total_available_mb
        message = f'Memory usage ist at {used_mb} MB of {total_available_mb} MB ({round(used*100,2)}%)'
        return WarnData(data[0], used, message)

    def read_data(self) -> list[any]:
        used_mb, free_mb, available_mb, total_mb = self.get_memory()
        used_and_cached_mb = total_mb - free_mb
        total_available_mb = used_mb + available_mb
        return [
            datetime_util.now(),
            used_mb,
            used_and_cached_mb,
            total_available_mb,
        ]

    def data_schema(self) -> list[str]:
        return ['datetime#Date', 'int#Used memory in MB', 'int#Used and cached in MB',
                'int#Total available memory in MB']

    def get_log_file(self) -> Path:
        return self.get_log_dir() / f'memory.csv'

    #
    # HELPERS
    #

    @classmethod
    def get_memory(cls) -> tuple[int, int, int, int]:
        """
        :return: Tuple[used memory in MB, free memory in MB, total memory in MB]. This does not include swap.
        """
        mb = 1024 * 1024
        mem = psutil.virtual_memory()

        # mem.available:
        #   The memory that can be given instantly to processes,
        #   excluding swap.
        # mem.total:
        #   Total physical memory (exclusive swap).
        # mem.used + mem.available != mem.total
        return int(mem.used / mb), int(mem.free / mb), int(mem.available / mb), int(mem.total / mb)
