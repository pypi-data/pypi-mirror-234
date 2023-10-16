#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

from de.p1st.monitor.cfg.singleton import get_cfg


def logging_dir() -> Path:
    cfg = get_cfg()
    default = '/var/log/de-p1st-monitor'
    if 'logging' not in cfg:
        return Path(default)
    return Path(cfg['logging'].get('dir', default))
