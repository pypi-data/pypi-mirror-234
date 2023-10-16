#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import NamedTuple
from datetime import datetime


class WarnData(NamedTuple):
    date: datetime
    value: int | float
    message: str
