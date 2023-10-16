#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
from typing import Literal
from pathlib import Path

import psutil

from de.p1st.monitor import datetime_util
from de.p1st.monitor.logger import Logger
from de.p1st.monitor.logger_ex import LoggerReadEx
from de.p1st.monitor.warn_data import WarnData


class DriveTempLogger(Logger):
    def __init__(self,
                 type_: Literal['drivetemp', 'nvme'],
                 warn_if_above: int = None,
                 warn_threshold: int = 1,
                 warn_data_range: int = 1,
                 ):
        """
        :param type_: HDD -> drivetemp, NVMe -> nvme
        """

        critical_if_above = warn_if_above + 10
        super().__init__(warn_threshold,
                         warn_data_range,
                         warn_if_above,
                         critical_if_above
                         )

        self.type = type_

    def get_warn_data(self, data: list[any]) -> WarnData:
        min_temp = data[1]
        max_temp = data[2]
        message = f'Temperature of drive type {self.type} is in range {min_temp}:{max_temp}'
        return WarnData(data[0], max_temp, message)

    def read_data(self) -> list[any]:
        min_temp, max_temp = self.get_drive_temp()
        return [
            datetime_util.now(),
            min_temp,
            max_temp
        ]

    def data_schema(self) -> list[str]:
        return ['datetime#Date', 'float#MinTemperature', 'float#MaxTemperature']

    def get_log_file(self) -> Path:
        return self.get_log_dir() / f'drive-temp_{self.type}.csv'

    #
    # HELPERS
    #

    def get_drive_temp(self) -> (float, float):
        """
        Use `psutil` Python library to get HDD/SSD temperature.
        https://psutil.readthedocs.io/en/latest/index.html#psutil.sensors_temperatures

        Not sure if this changed the results:
        sudo modprobe drivetemp

        Example output:
        {
          'nvme': [
            shwtemp(label='Composite', current=37.85, high=81.85, critical=85.85)
          ],
          'pch_skylake': [...],
          'coretemp': [...],
          'drivetemp': [
            shwtemp(label='', current=23.0, high=65.0, critical=85.0),
            shwtemp(label='', current=25.0, high=55.0, critical=70.0),
            shwtemp(label='', current=24.0, high=60.0, critical=85.0),
            shwtemp(label='', current=22.0, high=60.0, critical=85.0)]
        }

        Problem: If one has multiple drives attached, they can't be distinguished.
        https://github.com/giampaolo/psutil/issues/1902

        Therefore, we currently accumulate the maximum and minimum values of all drives of the same type.
        """
        min_temp, max_temp = -math.inf, math.inf

        data = psutil.sensors_temperatures(fahrenheit=False)
        if self.type not in data:
            raise LoggerReadEx(f'Sensor {self.type} not found')
        if len(data[self.type]) == 0:
            raise LoggerReadEx(f'Sensor {self.type} has no entries')
        for i in data[self.type]:
            current = i.current
            min_temp = max(min_temp, current)
            max_temp = min(max_temp, current)

        return min_temp, max_temp
