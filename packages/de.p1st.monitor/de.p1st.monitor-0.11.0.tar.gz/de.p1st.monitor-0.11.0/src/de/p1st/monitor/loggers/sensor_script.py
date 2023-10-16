#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
from pathlib import Path

from de.p1st.monitor import datetime_util
from de.p1st.monitor.logger import Logger
from de.p1st.monitor.logger_ex import LoggerReadEx
from de.p1st.monitor.warn_data import WarnData


class ScriptLogger(Logger):
    def __init__(self, command: list[str],
                 sensor_name: str,
                 warn_if_above: float = None,
                 warn_threshold: int = 1,
                 warn_data_range: int = 1,
                 ):
        if warn_if_above is None:
            critical_if_above = None
        else:
            critical_if_above = warn_if_above + 10

        super().__init__(warn_threshold,
                         warn_data_range,
                         warn_if_above,
                         critical_if_above)

        self.name = sensor_name
        self.command = command
        self.warn_if_above = warn_if_above

    def get_warn_data(self, data: list[any]) -> WarnData:
        value = data[1]
        message = f'Value of {self.name} ist at {value}'
        return WarnData(data[0], value, message)

    def read_data(self) -> list[any]:
        return [
            datetime_util.now(),
            self.get_value()
        ]

    def data_schema(self) -> list[str]:
        return [
            'datetime#Date',
            'float#Value'
        ]

    def get_log_file(self) -> Path:
        return self.get_log_dir() / f'sensor_script_{self.name}.csv'

    #
    # HELPERS
    #

    def get_value(self) -> float:
        """
        :return: Value of sensor
        """
        completed: subprocess.CompletedProcess = subprocess.run(
            self.command,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            raise LoggerReadEx(f'Script to read value of {self.name} failed with exit code {completed.returncode}.\n'
                               f'stderr: {completed.stderr}\n'
                               f'stdout: {completed.stdout}')
        value: str = completed.stdout.strip()
        return float(value)


def test():
    from de.p1st.monitor.cfg import singleton
    singleton.init_cfg()

    logger = ScriptLogger(["echo", "1.0"], 'test-script')
    logger.update()
    logger.log()
    logger.check().print()


if __name__ == '__main__':
    test()
