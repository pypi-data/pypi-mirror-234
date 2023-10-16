#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

import psutil
from de.p1st.monitor import datetime_util

from de.p1st.monitor.logger import Logger
from de.p1st.monitor.warn import WarnMessage, WarnLevel
from de.p1st.monitor.warn_data import WarnData


class SwapLogger(Logger):
    def __init__(self,
                 warn_if_above: float = 1.0,
                 warn_threshold: int = 1,
                 warn_data_range: int = 1,
                 ):
        # The space between swap is at `self.warn_if_above` and swap is full at `1.0`.
        buffer = 1 - warn_if_above
        critical_if_above = warn_if_above + 0.5 * buffer
        super().__init__(warn_threshold,
                         warn_data_range,
                         warn_if_above,
                         critical_if_above)
        self.warn_if_above = warn_if_above

    def get_warn_data(self, data: list[any]) -> WarnData | WarnMessage:
        used_mb = data[1]
        total_mb = data[2]
        message = f'Swap usage ist at {used_mb} MB of {total_mb} MB'

        if used_mb == 0 and total_mb == 0:
            return WarnMessage(WarnLevel.HIGH, data[0], 'Swap is not enabled')

        usage = used_mb / total_mb
        return WarnData(data[0], usage, message)

    def read_data(self) -> list[any]:
        used_mb, total_mb = self.get_swap()
        return [
            datetime_util.now(),
            used_mb,
            total_mb,
        ]

    def data_schema(self) -> list[str]:
        return ['datetime#Date', 'int#Used swap in MB', 'int#Total swap in MB']

    def get_log_file(self) -> Path:
        return self.get_log_dir() / f'swap.csv'

    #
    # HELPERS
    #

    @classmethod
    def get_swap(cls) -> (int, int):
        """
        :return: Tuple[used swap in MB, total swap in MB].
        """
        mb = 1024 * 1024
        mem = psutil.swap_memory()

        return int(mem.used / mb), int(mem.total / mb)
