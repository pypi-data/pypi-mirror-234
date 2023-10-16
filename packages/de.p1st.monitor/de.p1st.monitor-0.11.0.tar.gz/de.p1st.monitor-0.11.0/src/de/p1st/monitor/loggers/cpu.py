#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
from abc import abstractmethod
from typing import Literal

import psutil

from de.p1st.monitor import datetime_util

from de.p1st.monitor.logger import Logger
from de.p1st.monitor.warn_data import WarnData


class CPULogger(Logger):
    def __init__(self,
                 warn_if_above: float = None,
                 warn_threshold: int = 1,
                 warn_data_range: int = 1,
                 ):

        critical_if_above = warn_if_above * 1.5
        super().__init__(warn_threshold,
                         warn_data_range,
                         warn_if_above,
                         critical_if_above)
        self.warn_if_above = warn_if_above

    def get_warn_data(self, data: list[any]) -> WarnData:
        load_avg = data[1]
        message = f'CPU load avg of last {self.get_load_timespan()} minutes is at {load_avg}'
        return WarnData(data[0], load_avg, message)

    def read_data(self) -> list[any]:
        return [
            datetime_util.now(),
            self.get_load(self.get_load_timespan())
        ]

    def data_schema(self) -> list[str]:
        return [
            'datetime#Date',
            f'float#LoadAverage{self.get_load_timespan()}min'
        ]

    def get_log_file(self) -> Path:
        return self.get_log_dir() / f'cpu_{self.get_load_timespan()}min.csv'

    @abstractmethod
    def get_load_timespan(self) -> Literal[1, 5, 15]:
        raise ValueError('Subclasses must implement this')

    #
    # HELPERS
    #

    @staticmethod
    def get_load(minutes: Literal[1, 5, 15]) -> float:
        """
        :param minutes: avg of last 1/5/15 minutes
        :return: Average CPU load of last 1/5/15 minutes
        """
        idx_dict = {
            1: 0,
            5: 1,
            15: 2
        }
        idx = idx_dict[minutes]

        # Number of processes in the system run queue averaged over
        # the last 1, 5, and 15 minutes:
        # one, five, fifteen = psutil.getloadavg()

        # Load percentage during last 5 minutes.
        # This value has been tested to be correct on my AMD Ryzen 4800H CPU.
        return psutil.getloadavg()[idx] / psutil.cpu_count()


class CPULogger1(CPULogger):
    def get_load_timespan(self) -> Literal[1, 5, 15]:
        return 1


class CPULogger5(CPULogger):
    def get_load_timespan(self) -> Literal[1, 5, 15]:
        return 5


class CPULogger15(CPULogger):
    def get_load_timespan(self) -> Literal[1, 5, 15]:
        return 15
