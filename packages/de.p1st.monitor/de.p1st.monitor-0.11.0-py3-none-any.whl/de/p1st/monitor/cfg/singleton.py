#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import configparser
from pathlib import Path
import importlib.resources as importlib_resources

_cfg: configparser.ConfigParser | None = None


def init_cfg(config_file: Path = None):
    global _cfg
    if _cfg is not None:
        raise ValueError('Already initialized.')

    # Use the given config file.

    # Otherwise, use config file from /etc/de-p1st-monitor/.
    if config_file is None:
        import socket
        hostname: str = socket.gethostname()
        config_file = Path(f'/etc/de-p1st-monitor/{hostname}.ini')
        if not config_file.is_file():
            config_file = None

    # Otherwise, use packaged config file.
    if config_file is None:
        pkg = importlib_resources.files('de.p1st.monitor')
        config_file = pkg / 'data' / f'{hostname}.ini'
        if not config_file.is_file():
            config_file = None

    if config_file is None or not config_file.is_file():
        raise Exception(f'Configuration file does not exist! {config_file}')

    _cfg = configparser.ConfigParser()
    _cfg.read(config_file)


def get_cfg() -> configparser.ConfigParser:
    global _cfg

    if _cfg is None:
        raise ValueError('uninitialized')
    return _cfg
