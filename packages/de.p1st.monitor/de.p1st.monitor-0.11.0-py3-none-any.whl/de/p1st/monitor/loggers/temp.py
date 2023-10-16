#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

import psutil

from de.p1st.monitor import datetime_util
from de.p1st.monitor.logger import Logger
from de.p1st.monitor.logger_ex import LoggerReadEx
from de.p1st.monitor.warn_data import WarnData


class TempLogger(Logger):
    def __init__(self, sensor_name: str,
                 sensor_label: str,
                 warn_if_above: float = None,
                 warn_threshold: int = 1,
                 warn_data_range: int = 1,
                 ):

        critical_if_above = warn_if_above + 10
        super().__init__(warn_threshold,
                         warn_data_range,
                         warn_if_above,
                         critical_if_above)
        self.name = sensor_name
        self.label = sensor_label

        self.warn_if_above = warn_if_above

    def get_warn_data(self, data: list[any]) -> WarnData:
        temp = data[1]
        message = f'Temperature of {self.name} {self.label} ist at {temp}'
        return WarnData(data[0], temp, message)

    def read_data(self) -> list[any]:
        return [
            datetime_util.now(),
            self.get_temp()
        ]

    def data_schema(self) -> list[str]:
        return [
            'datetime#Date',
            'float#Temperature'
        ]

    def get_log_file(self) -> Path:
        return self.get_log_dir() / f'temp_{self.name}_{self.label}.csv'

    #
    # HELPERS
    #

    def get_temp(self) -> float:
        """
        :return: Temperature in Celsius
        """
        data = psutil.sensors_temperatures(fahrenheit=False)
        if self.name not in data:
            raise LoggerReadEx(f'Sensor {self.name} not found')
        for i in data[self.name]:
            if i.label == self.label:
                return i.current
        raise LoggerReadEx(f'Label {self.label} of sensor {self.name} not found')


def test():
    from de.p1st.monitor.cfg import singleton
    singleton.init_cfg()

    logger = TempLogger('amdgpu', 'edge', 47, 2, 4)
    logger.update()
    logger.log()
    logger.check().print()


if __name__ == '__main__':
    test()
