#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
from abc import ABC, abstractmethod

from de.p1st.monitor import csv_util, datetime_util
from de.p1st.monitor.cfg.logging_dir import logging_dir
from de.p1st.monitor.string_conversion import to_string, from_string
from de.p1st.monitor.warn import WarnMessage, WarnLevel
from de.p1st.monitor.warn_data import WarnData


# https://www.geeksforgeeks.org/abstract-classes-in-python/
class Logger(ABC):
    def __init__(self,
                 warn_threshold: int = 1,
                 warn_data_range: int = 1,
                 warn_if_above: int | float = None,
                 critical_if_above: int | float = None,
                 ):
        self.data: list[any] = []
        # True if the data held by this object is already appended to the logfile.
        self.logged = False

        self.warn_threshold = warn_threshold
        self.warn_data_range = warn_data_range

        # Either both variables are given, or both are None
        if warn_if_above is not None and critical_if_above is not None:
            if critical_if_above <= warn_if_above:
                raise Exception(f'The critical limit is not greater that the warning limit:'
                                f' {critical_if_above}, {warn_if_above}')
        else:
            if warn_if_above is not None or critical_if_above is not None:
                raise Exception(
                    'Either both, warn_if_above and critical_if_above, must be given, or both must be None.')
        self.warn_if_above = warn_if_above
        self.critical_if_above = critical_if_above

    def export_data(self) -> Path:
        """
        This method is intended to be overriden in a subclass!

        With most loggers the `get_log_file()` is ready-to-use.
        In this case this method simply returns `get_log_file()`.

        But some loggers require postprocessing of that data before it can be used.
        In this case this method creates a new .csv file and returns it.

        @return: Path to .csv file with ready-to-use data.
        """
        return self.get_log_file()

    def check(self) -> WarnMessage:
        """
        Checks if `self.warn_threshold` or more of the latest `self.warn_data_range` datasets
        contain values higher than `self.warn_if_above` in which case a warning (NORMAL or HIGH)
        might be returned.

        In details:

        If the current value is above `self.critical_if_above`,
        then a HIGH WarnMessage is returned.

        If less than `self.warn_threshold` values are above `self.warn_if_above`,
        then no warning is returned.

        If the current value is lower than the previously logged one
        and if during the previous check a warning was issued,
        then no warning is returned.

        Otherwise, a NORMAL WarnMessage is returned.
        """
        if self.warn_if_above is None:
            # self.critical_if_above is also None
            return WarnMessage(WarnLevel.NONE)

        datasets = self.get_datasets(self.warn_data_range + 1)
        warn_datas = [self.get_warn_data(data) for data in datasets]
        current_warn_data = warn_datas[-1]

        # If current value is critical (or current warning is HIGH), directly return HIGH WarnMessage.
        #
        # -> As we don't want to send the same warning twice,
        #    we check only if the current value is critical.
        if isinstance(current_warn_data, WarnData):
            if current_warn_data.value > self.critical_if_above:
                return WarnMessage(WarnLevel.HIGH, datetime_util.now(), current_warn_data.message)
        elif isinstance(current_warn_data, WarnMessage):
            if current_warn_data.level > WarnLevel.NORMAL:
                return current_warn_data
        else:
            raise ValueError()

        current_warn_datas = warn_datas[-self.warn_data_range:]
        curr_num_warnings, curr_highest_warning = self._get_num_warnings(current_warn_datas)

        # Warning threshold not reached.
        if curr_num_warnings < self.warn_threshold:
            return WarnMessage(WarnLevel.NONE)

        previous_warn_datas = warn_datas[-self.warn_data_range - 1:-1]
        prev_num_warnings, prev_highest_warning = self._get_num_warnings(previous_warn_datas)

        # Don't send warning again if the current value decreased.
        if prev_num_warnings >= self.warn_if_above:
            previous_warn_data = warn_datas[-2]
            if isinstance(current_warn_data, WarnData) \
                    and isinstance(previous_warn_data, WarnData) \
                    and current_warn_data.value <= previous_warn_data.value:
                return WarnMessage(WarnLevel.NONE)

        # Send warning.
        warn_messages = self._get_warn_messages(current_warn_datas)
        message = f'{curr_num_warnings} of the last {len(current_warn_datas)} datasets are above limits:\n\t' \
                  + '\n\t'.join(warn_messages)
        return WarnMessage(WarnLevel.NORMAL, datetime_util.now(), message)

    def _get_num_warnings(self, warn_datas: list[WarnData | WarnMessage]) -> tuple[int, WarnLevel]:
        """
        @precondition: self.warn_if_above and self.critical_if_above are not None
        @return: Number of warnings and the highest WarnLevel
        """
        num_warnings = 0
        highest_warn_level = WarnLevel.NONE

        for warn_data in warn_datas:
            if isinstance(warn_data, WarnMessage):
                highest_warn_level = max(highest_warn_level, warn_data.level)
            elif isinstance(warn_data, WarnData):
                if warn_data.value > self.critical_if_above:
                    num_warnings += 1
                    highest_warn_level = max(highest_warn_level, WarnLevel.HIGH)
                elif warn_data.value > self.warn_if_above:
                    num_warnings += 1
                    highest_warn_level = max(highest_warn_level, WarnLevel.NORMAL)
            else:
                raise ValueError()

        return num_warnings, highest_warn_level

    def _get_warn_messages(self, warn_datas: list[WarnData | WarnMessage]) -> list[str]:
        """
        @precondition: self.warn_if_above and self.critical_if_above are not None
        """
        messages: list[str] = []

        for warn_data in warn_datas:
            if isinstance(warn_data, WarnMessage):
                messages.append(warn_data.formatted_message())
            elif isinstance(warn_data, WarnData):
                if warn_data.value > self.critical_if_above:
                    messages.append(
                        WarnMessage(WarnLevel.HIGH, warn_data.date, warn_data.message).formatted_message())
                elif warn_data.value > self.warn_if_above:
                    messages.append(
                        WarnMessage(WarnLevel.NORMAL, warn_data.date, warn_data.message).formatted_message())
            else:
                raise ValueError()

        return messages

    @abstractmethod
    def get_warn_data(self, data: list[any]) -> WarnData | WarnMessage:
        """
        Calculate warn value from given data and return as part of `WarnData` object.

        If the value can't be calculated, directly return a `WarnMessage` object.

        @return Warn value; Message for normal warning; Message for critical warning
        """
        raise ValueError('Subclasses must implement this')

    def get_all_datasets(self) -> list[list[any]]:
        # See also: self.get_datasets()

        if self.get_log_file().exists():
            # We skip the first row as it is the data schema.
            raw = csv_util.read(self.get_log_file())[1:]
            data = [self.get_data_from_row(row) for row in raw]
        else:
            data = []

        if not self.logged and self.has_data():
            data.append(self.get_data())

        return data

    def get_datasets(self, num: int) -> list[list[any]]:
        """
        Returns the last `num` datasets (including the current dataset).

        The first row is the oldest, and the latest row is the current dataset.
        """
        if not self.logged and self.has_data():
            # We will append the current data manually.
            # Thus, we need to read one less line from the CSV file.
            read_last = num - 1
        else:
            read_last = num

        if self.get_log_file().exists():
            # Read rows from CSV file.
            # We skip the first row as it is the data schema.
            # We keep only the last `read_last` rows.
            raw = csv_util.read_last(self.get_log_file(), read_last, 1)
            # Convert from string to data types defined in the data schema.
            data = [self.get_data_from_row(row) for row in raw]
        else:
            data = []

        if not self.logged and self.has_data():
            # We append the current data.
            # It has not yet been logged and is therefore not included in the CSV file we just read.
            data.append(self.get_data())

        return data

    def log(self) -> None:
        """
        Appends the current data (e.g. temperature of a sensor)
        to a logfile.

        :raise Exception: If method is called but no data is available. Please do call update() first to avoid this!
        """
        if self.logged:
            return

        csv_util.write(file=self.get_log_file(), rows=[self.get_data_as_row()], header=self.data_schema())
        self.logged = True

    def update(self):
        self.set_data(self.read_data())
        self.logged = False

    @abstractmethod
    def read_data(self) -> list[any]:
        """
        Collects current data (e.g. temperature of a sensor).

        :raise LoggerReadEx:
        """
        raise ValueError('Subclasses must implement this')

    @abstractmethod
    def data_schema(self) -> list[str]:
        """
        Describes the type and meaning of the elements in self.values().

        Returns a list with elements f'{data-type}#{column-description}'.

        Example:
            ['datetime#Date', 'float#Disk usage']
        """
        raise ValueError('Subclasses must implement this')

    def get_data_from_row(self, data: list[str]) -> list[any]:
        return [
            from_string(v, type_str)
            for v, type_str
            in zip(data, self.data_type_strs())
        ]

    def get_data_as_row(self) -> list[str]:
        """
        Returns `self.get_data()` as string list that can easily be added as row to a CSV file.
        """
        return self.as_row(self.get_data())

    def as_row(self, data: list, data_schema: list[str] = None) -> list[str]:
        """
        Returns the given `data` as string list that can easily be added as row to a CSV file.
        """
        if data_schema is None:
            data_schema = self.data_schema()
        return [
            to_string(v, type_str)
            for v, type_str
            in zip(data, self.data_type_strs(data_schema))
        ]

    def has_data(self) -> bool:
        return len(self.data) > 0

    def get_data(self) -> list[any]:
        """
        Returns the last data collected by `self.update()`.
        """
        if self.has_data():
            return self.data
        else:
            raise ValueError(f'Data has not yet been read. {self.__str__()}')

    def set_data(self, data: list[any]):
        if len(data) < 1:
            raise ValueError()
        self.data = data

    def data_type_strs(self, data_schema: list[str] = None) -> list[str]:
        if data_schema is None:
            data_schema = self.data_schema()
        return [x.split('#', maxsplit=1)[0] for x in data_schema]

    @abstractmethod
    def get_log_file(self) -> Path:
        raise ValueError('Subclasses must implement this')

    @classmethod
    def get_log_dir(cls) -> Path:
        return logging_dir()

    def __str__(self) -> str:
        key_value_strings = [f'classname: {type(self).__name__}']
        for key, value in vars(self).items():
            key_value_strings.append(f'{key}: {value}')
        return ', '.join(key_value_strings)
