#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import configparser
import json
from pathlib import Path

from de.p1st.monitor.cfg.singleton import get_cfg
from de.p1st.monitor.logger_ex import LoggerArgEx
from de.p1st.monitor.loggers.cpu import CPULogger1, CPULogger5, CPULogger15
from de.p1st.monitor.loggers.drive import DriveLogger
from de.p1st.monitor.loggers.drive_temp import DriveTempLogger
from de.p1st.monitor.loggers.filesystem import FilesystemLogger
from de.p1st.monitor.loggers.memory import MemoryLogger
from de.p1st.monitor.loggers.network import NetworkLogger
from de.p1st.monitor.loggers.sensor_script import ScriptLogger
from de.p1st.monitor.loggers.swap import SwapLogger
from de.p1st.monitor.loggers.temp import TempLogger
from de.p1st.monitor.logger import Logger


def get_or_raise(cfg: configparser.SectionProxy, key: str) -> str:
    if key in cfg:
        return cfg[key]
    else:
        raise LoggerArgEx(f'Missing key {key} in section {cfg.name}')


def get_loggers() -> tuple[list[Logger], list[LoggerArgEx]]:
    def temp(cfg_: configparser.SectionProxy) -> Logger:
        sensor = get_or_raise(cfg_, 'sensor')
        label = get_or_raise(cfg_, 'label')
        warn_if_above = float(cfg_['warn_if_above']) if 'warn_if_above' in cfg_ else None
        warn_threshold = int(cfg_.get('warn_threshold', '1'))
        warn_data_range = int(cfg_.get('warn_data_range', '1'))
        return TempLogger(sensor, label, warn_if_above, warn_threshold, warn_data_range)

    def sensor_script(cfg_: configparser.SectionProxy) -> Logger:
        cmd_json_str = get_or_raise(cfg_, 'cmd')
        cmd_json: list[str] = json.loads(cmd_json_str)
        assert isinstance(cmd_json, list)
        for arg in cmd_json:
            assert isinstance(arg, str)

        name = get_or_raise(cfg_, 'name')
        warn_if_above = float(cfg_['warn_if_above']) if 'warn_if_above' in cfg_ else None
        warn_threshold = int(cfg_.get('warn_threshold', '1'))
        warn_data_range = int(cfg_.get('warn_data_range', '1'))
        return ScriptLogger(cmd_json, name, warn_if_above, warn_threshold, warn_data_range)

    def cpu1(cfg_: configparser.SectionProxy) -> Logger:
        warn_if_above = float(cfg_['warn_if_above']) if 'warn_if_above' in cfg_ else None
        warn_threshold = int(cfg_.get('warn_threshold', '1'))
        warn_data_range = int(cfg_.get('warn_data_range', '1'))
        return CPULogger1(warn_if_above, warn_threshold, warn_data_range)

    def cpu5(cfg_: configparser.SectionProxy) -> Logger:
        warn_if_above = float(cfg_['warn_if_above']) if 'warn_if_above' in cfg_ else None
        warn_threshold = int(cfg_.get('warn_threshold', '1'))
        warn_data_range = int(cfg_.get('warn_data_range', '1'))
        return CPULogger5(warn_if_above, warn_threshold, warn_data_range)

    def cpu15(cfg_: configparser.SectionProxy) -> Logger:
        warn_if_above = float(cfg_['warn_if_above']) if 'warn_if_above' in cfg_ else None
        warn_threshold = int(cfg_.get('warn_threshold', '1'))
        warn_data_range = int(cfg_.get('warn_data_range', '1'))
        return CPULogger15(warn_if_above, warn_threshold, warn_data_range)

    def net(cfg_: configparser.SectionProxy) -> Logger:
        network_interface = get_or_raise(cfg_, 'network_interface')
        return NetworkLogger(network_interface)

    def filesystem(cfg_: configparser.SectionProxy) -> Logger:
        uuid = cfg_.get('uuid', None)
        mountpoint = Path(cfg_.get('mountpoint')) if 'mountpoint' in cfg_ else None
        unmounted_ok = bool(cfg_.get('unmounted_ok', 'false'))
        warn_if_above = float(cfg_.get('warn_if_above', '1.0'))
        warn_threshold = int(cfg_.get('warn_threshold', '1'))
        warn_data_range = int(cfg_.get('warn_data_range', '1'))
        return FilesystemLogger(uuid, mountpoint, unmounted_ok, warn_if_above, warn_threshold, warn_data_range)

    def drive(cfg_: configparser.SectionProxy) -> Logger:
        uuid = cfg_.get('uuid', None)
        id_ = cfg_.get('id', None)
        device = Path(cfg_.get('device')) if 'device' in cfg_ else None
        warn_if_above = int(cfg_['warn_if_above']) if 'warn_if_above' in cfg_ else None
        warn_threshold = int(cfg_.get('warn_threshold', '1'))
        warn_data_range = int(cfg_.get('warn_data_range', '1'))
        return DriveLogger(uuid, id_, device, warn_if_above, warn_threshold, warn_data_range)

    def drive_temp(cfg_: configparser.SectionProxy) -> Logger:
        type_ = cfg_.get('type', None)
        warn_if_above = int(cfg_['warn_if_above']) if 'warn_if_above' in cfg_ else None
        warn_threshold = int(cfg_.get('warn_threshold', '1'))
        warn_data_range = int(cfg_.get('warn_data_range', '1'))
        return DriveTempLogger(type_, warn_if_above, warn_threshold, warn_data_range)

    def memory(cfg_: configparser.SectionProxy) -> Logger:
        warn_if_above = float(cfg_.get('warn_if_above', '1.0'))
        warn_threshold = int(cfg_.get('warn_threshold', '1'))
        warn_data_range = int(cfg_.get('warn_data_range', '1'))
        return MemoryLogger(warn_if_above, warn_threshold, warn_data_range)

    def swap(cfg_: configparser.SectionProxy) -> Logger:
        warn_if_above = float(cfg_.get('warn_if_above', '1.0'))
        warn_threshold = int(cfg_.get('warn_threshold', '1'))
        warn_data_range = int(cfg_.get('warn_data_range', '1'))
        return SwapLogger(warn_if_above, warn_threshold, warn_data_range)

    mapping = {
        'temp': temp,
        'sensor_script': sensor_script,
        'cpu1': cpu1,
        'cpu5': cpu5,
        'cpu15': cpu15,
        'network': net,
        'filesystem': filesystem,
        'drive': drive,
        'drive_temp': drive_temp,
        'memory': memory,
        'swap': swap,
    }

    loggers = []
    exceptions = []
    cfg: configparser.ConfigParser = get_cfg()
    for section_name in cfg.sections():
        if section_name == 'logging':
            continue
        prefix = section_name.split('.', maxsplit=1)[0]
        try:
            loggers.append(
                mapping[prefix](cfg[section_name])
            )
        except LoggerArgEx as e:
            exceptions.append(e)

    return loggers, exceptions
