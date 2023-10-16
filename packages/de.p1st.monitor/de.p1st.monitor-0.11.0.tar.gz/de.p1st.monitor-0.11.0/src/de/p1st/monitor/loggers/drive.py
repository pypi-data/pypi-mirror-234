#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from pathlib import Path

from de.p1st.monitor import datetime_util

from de.p1st.monitor.exec_capture import execute_capture
from de.p1st.monitor.logger import Logger
from de.p1st.monitor.logger_ex import LoggerArgEx, LoggerReadEx
from de.p1st.monitor.warn_data import WarnData


class BlkidException(Exception):
    pass


class UUIDException(Exception):
    pass


class IDException(Exception):
    pass


class DriveLogger(Logger):
    def __init__(self,
                 uuid: str = None,
                 id_: str = None,
                 device: Path = None,
                 warn_if_above: int = None,
                 warn_threshold: int = 1,
                 warn_data_range: int = 1,
                 ):

        critical_if_above = warn_if_above + 10
        super().__init__(warn_threshold,
                         warn_data_range,
                         warn_if_above,
                         critical_if_above
                         )

        if uuid is None and id_ is None and device is None:
            raise LoggerArgEx('uuid, id_ or device required')
        # `device` might be `None`.
        if uuid is not None:
            device = self.get_partition_from_uuid(uuid)
        if id_ is not None:
            device = self.get_partition_from_id(id_)
        # `device` is not `None`.
        # `id_` might be `None`.
        if id_ is None:
            id_ = self.get_id_from_device(device)
        # Store as attributes.
        self.id_ = id_
        self.device = device

        self.warn_if_above = warn_if_above

    def get_warn_data(self, data: list[any]) -> WarnData:
        temp = data[1]
        message = f'Temperature of {self.id_} ist at {temp}'
        return WarnData(data[0], temp, message)

    def read_data(self) -> list[any]:
        return [
            datetime_util.now(),
            self.get_temp_from_device(self.device),
        ]

    def data_schema(self) -> list[str]:
        return ['datetime#Date', 'int#Temperature']

    def get_log_file(self) -> Path:
        # self.device might change overtime.
        # Thus, we use self.id_ to identify a partition.
        return self.get_log_dir() / f'drive_{self.id_}.csv'

    #
    # HELPERS
    #

    @classmethod
    def get_partition_from_uuid(cls, uuid: str) -> Path:
        """
        :return: Partition path, e.g. /dev/sda1
        """
        device = Path(f'/dev/disk/by-uuid/{uuid}').resolve()
        if not device.is_relative_to('/dev'):
            raise UUIDException(f'Could not determine /dev/* path from UUID: {uuid}')
        return device

    @classmethod
    def get_partition_from_id(cls, id_: str) -> Path:
        """
        :return: Partition path, e.g. /dev/sda1
        """
        device = Path(f'/dev/disk/by-id/{id_}').resolve()
        if not device.is_relative_to('/dev'):
            raise IDException(f'Could not determine /dev/* path from ID: {id_}')
        return device

    @classmethod
    def get_id_from_device(cls, device: Path) -> str:
        id_paths = Path('/dev/disk/by-id/').iterdir()
        # Filter.
        id_paths = [id_path for id_path in id_paths
                    if id_path.resolve() == device]
        # We expect at least one result.
        if len(id_paths) == 0:
            raise IDException(f'Could not determine /dev/disk/by-id/* from device: {device}')
        # Sort by path length => Sort by ID length.
        id_paths = sorted(id_paths, key=lambda x: len(str(x)))
        # Return shortest ID.
        return id_paths[0].name

    @classmethod
    def get_uuid_from_partition(cls, device: Path) -> str:
        """
        :param device: Partition path, e.g. /dev/sda1
        :return: UUID of given partition
        :raise BlkidException: If UUID could not be determined.
        """
        returncode, stdout, stderr = execute_capture(['blkid', '-s', 'UUID', '-o', 'value', f'{device}'])
        if returncode != 0:
            raise BlkidException(f'blkid failed for device {device} with returncode {returncode}\nstdout: {stdout}\nstderr: {stderr}')

        uuid = stdout.strip()
        if len(uuid) == 0:
            raise BlkidException(f'blkid had exit code zero, but the UUID is empty.'
                                 f' Did you maybe provide a device instead of a partition? {device}')

        return uuid

    @classmethod
    def get_temp_from_device(cls, device: Path) -> int:
        """
        Use `smartctl` to get HDD/SSD temperature.

        As reading SMART data wakes up standby HDD drives, we skip them.

        :param device: Partition path, e.g. `/dev/sda`
        :return: Temperature in Celsius
        """

        # -n standby: Don't spin-up an HDD if it is in standby mode.
        # -j: JSON output.
        # -a: Print all SMART device information.
        #     For NVMe, this is equivalent to: '-H -i -c -A -l error -l selftest'.
        # -H: Print health status.
        # -A: Prints only the  vendor  specific  SMART Attributes.
        returncode, stdout, stderr = execute_capture(['smartctl', '-n', 'standby', '-j', '-A', f'{device}'])

        if returncode == 2 and 'Device is in STANDBY mode' in stdout:
            raise LoggerReadEx(f'Could not read drive temperature as it is in standby mode: {device}')
        if returncode != 0:
            raise LoggerReadEx(f'smartctl failed with returncode {returncode}\nstdout: {stdout}\nstderr: {stderr}')
        j = json.loads(stdout)

        temp_key = 'temperature'
        if temp_key not in j:
            raise LoggerReadEx(f'smartctl JSON does not contain key {temp_key}. {device}')
        current_key = 'current'
        if current_key not in j[temp_key]:
            raise LoggerReadEx(f'smartctl JSON does not contain key {temp_key}.{current_key}. {device}')
        return j[temp_key][current_key]
