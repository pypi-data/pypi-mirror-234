#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Callable

from de.p1st.monitor import datetime_util


def data_types() -> dict[str, dict[str, Callable[[any], any]]]:
    """
    Returns a dictionary. Its key-value pairs contain the following:

    Key: Name of type.
    Value: Dict containing to_string and from_string conversion methods, called 'to' and 'from'.
    """
    return {
        'str': {'to': lambda x: x, 'from': lambda x: x},
        'int': {'to': lambda x: str(x), 'from': lambda x: int(x)},
        'float': {'to': lambda x: str(x), 'from': lambda x: float(x)},
        'datetime': {'to': datetime_util.to_str, 'from': datetime_util.from_str},
    }


def to_string(v: any, type_str: str) -> str:
    return data_types()[type_str]['to'](v)


def from_string(v: str, type_str: str) -> any:
    return data_types()[type_str]['from'](v)
