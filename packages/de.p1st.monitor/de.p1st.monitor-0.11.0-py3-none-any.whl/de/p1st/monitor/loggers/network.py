#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import psutil

from de.p1st.monitor import datetime_util, csv_util
from de.p1st.monitor.logger import Logger
from de.p1st.monitor.logger_ex import LoggerReadEx
from de.p1st.monitor.warn import WarnLevel, WarnMessage


class NetworkLogger(Logger):
    def __init__(self, network_interface: str):
        super().__init__()
        self.network_interface = network_interface

    def export_data(self) -> Path:
        data = self.get_all_datasets()

        # This includes some duplicate data.
        # The bare minimum would be
        # - start time and duration in seconds
        # - bytes sent and received
        export_schema = [
            'datetime#Date',
            'float#Bytes sent per second',
            'float#Bytes received per second',
            'float#Bytes sent',
            'float#Bytes received'
        ]
        export_data = []
        # Append all other rows.
        for prev_row, curr_row in zip(data[:-1], data[1:]):
            # if boot time differs -> reboot between data points -> invalid sent/received deltas
            if prev_row[3] != curr_row[3]:
                continue

            elapsed_time: timedelta = curr_row[0] - prev_row[0]
            delta_sent = curr_row[1] - prev_row[1]
            delta_received = curr_row[2] - prev_row[2]

            if delta_sent < 0 or delta_received < 0:
                print(f'bytes received/sent counter did overflow after {prev_row[0]}',
                      file=sys.stderr)
                continue

            elapsed_seconds = elapsed_time.total_seconds()
            export_data.append([
                # datetime#Date
                prev_row[0] + 0.5 * elapsed_time,
                # float#Bytes sent per second
                delta_sent / elapsed_seconds,
                # float#Bytes received per second
                delta_received / elapsed_seconds,
                # float#Bytes sent
                delta_sent,
                # float#Bytes received
                delta_received,
            ])

        export_file = self.get_log_file().parent.joinpath(self.get_log_file().name + '.exported.csv')
        rows = [self.as_row(export_row, export_schema) for export_row in export_data]
        csv_util.write(file=export_file, rows=rows, header=export_schema, recreate_file=True)
        return export_file

    def get_warn_data(self, data: list[any]) -> WarnMessage:
        # TODO
        return WarnMessage(WarnLevel.NONE)

    def data_schema(self) -> list[str]:
        return [
            'datetime#Date',
            'int#Bytes sent since boot',
            'int#Bytes received since boot',
            'datetime#Boot date',
        ]

    def read_data(self) -> list[any]:
        sent, received = self.get_net_usage()
        return [
            datetime_util.now(),
            sent,
            received,
            self.get_boot_time(),
        ]

    def get_log_file(self) -> Path:
        return self.get_log_dir() / f'net_{self.network_interface}.csv'

    #
    # HELPERS
    #

    def get_net_usage(self) -> tuple[int, int]:
        """
        Warning: The returned values may overflow if the system is running for a long time.

        :return: bytes sent, bytes received
        """
        # noinspection PyTypeChecker
        nics_data: dict[str, psutil._common.snetio] = psutil.net_io_counters(pernic=True, nowrap=True)

        if self.network_interface not in nics_data:
            raise LoggerReadEx(f'Network interface {self.network_interface} not found')

        nic_data = nics_data[self.network_interface]
        return nic_data.bytes_sent, nic_data.bytes_recv

    @classmethod
    def get_boot_time(cls) -> datetime:
        epoch_seconds = psutil.boot_time()
        return datetime.fromtimestamp(epoch_seconds, tz=timezone.utc)


def test():
    from de.p1st.monitor.cfg.singleton import init_cfg
    init_cfg()

    logger = NetworkLogger('wlp1s0')
    logger.update()
    logger.log()


if __name__ == '__main__':
    test()
