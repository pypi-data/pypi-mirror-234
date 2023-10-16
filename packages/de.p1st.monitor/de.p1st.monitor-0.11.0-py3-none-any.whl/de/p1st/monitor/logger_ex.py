#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class LoggerReadEx(Exception):
    """
    Used by Logger subclasses if
    - sensor data could not be read
    """
    pass


class LoggerArgEx(Exception):
    """
    Used by Logger subclasses if
    - Logger object created with illegal arguments
    """
    pass
