#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
from pathlib import Path

import psutil
from de.p1st.monitor import datetime_util, csv_util
from de.p1st.monitor.exec_capture import execute_capture

from de.p1st.monitor.logger import Logger
from de.p1st.monitor.logger_ex import LoggerArgEx, LoggerReadEx
from de.p1st.monitor.warn import WarnLevel, WarnMessage
from de.p1st.monitor.warn_data import WarnData


class NotMounted(Exception):
    pass


class FilesystemLogger(Logger):
    def __init__(self, uuid: str = None,
                 mountpoint: Path = None,
                 unmounted_ok: bool = False,
                 warn_if_above: float = 1.0,
                 warn_threshold: int = 1,
                 warn_data_range: int = 1,
                 ):

        # The space between disk is at `self.warn_if_above` and disk is full at `1.0`.
        buffer = 1 - warn_if_above
        critical_if_above = warn_if_above + 0.5 * buffer
        super().__init__(warn_threshold,
                         warn_data_range,
                         warn_if_above,
                         critical_if_above,
                         )

        if uuid is None and mountpoint is None:
            raise LoggerArgEx('uuid or mountpoint required')

        self.uuid = uuid
        self.mountpoint = mountpoint
        self.unmounted_ok = unmounted_ok
        self.warn_if_above = warn_if_above

        self.mounted = True

        #
        #
        #

        # If uuid and mountpoint are both specified,
        # raise warning if unexpected uuid is mounted at mountpoint.
        if self.mountpoint is not None and self.uuid is not None:
            try:
                actual_uuid = self.get_uuid(self.mountpoint)
                self.mounted = True
                if self.uuid != actual_uuid:
                    raise LoggerReadEx(f'Expected {self.uuid} at {self.mountpoint} but got {actual_uuid}')
            except NotMounted as e:
                if self.unmounted_ok:
                    self.mounted = False
                else:
                    raise LoggerArgEx(getattr(e, 'message', e))

        # Try to get UUID (if only mountpoint given)
        if self.uuid is None:
            try:
                self.uuid = self.get_uuid(self.mountpoint)
                self.mounted = True
            except NotMounted as e:
                if self.unmounted_ok:
                    self.mounted = False
                else:
                    raise LoggerArgEx(getattr(e, 'message', e))

        # Try to get mountpoint (if only uuid given)
        if self.mountpoint is None:
            try:
                self.mountpoint = self.get_mountpoint(self.uuid)
                self.mounted = True
            except NotMounted as e:
                if self.unmounted_ok:
                    self.mounted = False
                else:
                    raise LoggerReadEx(getattr(e, 'message', e))

    def export_data(self) -> Path:
        data = self.get_all_datasets()

        export_schema = self.data_schema()

        # Filter rows where `Disk usage` is NAN.
        export_data = [row for row in data
                       if not math.isnan(row[1])]

        export_file = self.get_log_file().parent.joinpath(self.get_log_file().name + '.exported.csv')
        rows = [self.as_row(export_row, export_schema) for export_row in export_data]
        csv_util.write(file=export_file, rows=rows, header=export_schema, recreate_file=True)
        return export_file

    def get_warn_data(self, data: list[any]) -> WarnData | WarnMessage:
        disk_usage = data[1]
        if math.isnan(disk_usage):
            if self.unmounted_ok:
                return WarnMessage(WarnLevel.NONE)
            else:
                return WarnMessage(WarnLevel.HIGH, data[0], 'Disk is not mounted')

        message = f'Disk usage of {self.uuid} ist at {disk_usage}'
        return WarnData(data[0], disk_usage, message)

    def read_data(self) -> list[any]:
        if not self.mounted:
            return [
                datetime_util.now(),
                float('nan')
            ]

        disk_usage: float = self.get_disk_usage(self.mountpoint)
        return [
            datetime_util.now(),
            disk_usage,
        ]

    def data_schema(self) -> list[str]:
        """
        If no disk usage value could be read (if a disk was unmounted),
        NAN is stored as `Disk usage`.
        """
        return ['datetime#Date', 'float#Disk usage']

    def get_log_file(self) -> Path:
        # The mountpoint of a filesystem might change overtime.
        # Thus, we use self.uuid to identify a filesystem.
        return self.get_log_dir() / f'filesystem_{self.uuid}.csv'

    #
    # HELPERS
    #

    @classmethod
    def get_disk_usage(cls, mountpoint: Path) -> float:
        """
        :returns: used space / total space
        """
        return psutil.disk_usage(str(mountpoint)).percent / 100.0

    @classmethod
    def get_mountpoint(cls, uuid: str) -> Path:
        """
        Throws an error if the corresponding partition is not mounted.
        """

        partition_list: list[psutil._common.sdiskpart] = psutil.disk_partitions(all=False)
        partitions: dict[Path, psutil._common.sdiskpart] = {Path(partition.device).resolve(): partition for partition in
                                                            partition_list}

        partition_path = cls.get_partition_path(uuid)
        if partition_path not in partitions:
            raise NotMounted(
                f'Partition {partition_path} is probably not mounted '
                f'as it is not in psutil partition list: {partitions}')

        partition = partitions[partition_path]
        return Path(partition.mountpoint)

    @classmethod
    def get_uuid(cls, mountpoint: Path) -> str:
        # Returns the UUID of the device mounted at `/`.
        # Fails if there is no disk mounted at `/`.
        #
        # findmnt / -o UUID -n

        returncode, stdout, stderr = execute_capture(['findmnt', str(mountpoint), '-o', 'UUID', '-n'])
        if returncode != 0:
            raise NotMounted(
                f'No partition mounted at {mountpoint}. Stderr of findmnt: {stderr}')

        return stdout.strip()

    @classmethod
    def get_partition_path(cls, uuid: str) -> Path:
        """
        :return: Partition path, e.g. /dev/sda1
        """
        return Path(f'/dev/disk/by-uuid/{uuid}').resolve()
