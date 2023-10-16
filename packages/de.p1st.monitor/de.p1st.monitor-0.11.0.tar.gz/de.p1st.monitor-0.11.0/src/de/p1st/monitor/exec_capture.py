#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess


def execute_capture(command: list[str]) -> tuple[int, str, str]:
    completed: subprocess.CompletedProcess = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )
    return completed.returncode, completed.stdout, completed.stderr
