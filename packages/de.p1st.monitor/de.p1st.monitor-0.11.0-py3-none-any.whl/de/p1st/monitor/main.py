#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import sys
from pathlib import Path

from de.p1st.monitor.cfg.singleton import init_cfg
from de.p1st.monitor.cfg.loggers import get_loggers
from de.p1st.monitor.logger_ex import LoggerReadEx


def main():
    parser = argparse.ArgumentParser(prog='de-p1st-monitor',
                                     description='Iterates over all config sections. '
                                                 'For each section the current sensor data is read '
                                                 'and logged to a .csv file.')
    parser.add_argument('--config', '-c', default=None, type=Path,
                        help='Path to .ini configuration file.')
    parser.add_argument('--export', '-e', default=False, action='store_true',
                        help='If `True`, export .csv files and print their paths to stdout. '
                             'No sensor data is logged during this.')
    # parser.add_argument('--export', '-e', default=False, type=bool,
    #                     help='If `True`, export .csv files and print their paths to stdout.
    #                     No sensor data is logged during this.')
    args = parser.parse_args()
    init_cfg(args.config)

    if args.export:
        export()
    else:
        log()


def export():
    loggers, logger_arg_exs = get_loggers()
    if len(logger_arg_exs) > 0:
        print('\nCONFIGURATION ERROR: Could not instantiate some of the loggers!', file=sys.stderr)
        print_exs(logger_arg_exs, [f'{n}.' for n in range(1, 1 + len(logger_arg_exs))])
        exit(1)

    for logger in loggers:
        export_path: Path = logger.export_data()
        print(export_path)


def log():
    loggers, logger_arg_exs = get_loggers()
    logger_read_exs = []
    logger_warnings = 0
    for logger_ct, logger in enumerate(loggers, start=1):
        print(f'Running logger {logger_ct}/{len(loggers)} ...')
        try:
            logger.update()
        except LoggerReadEx as e:
            logger_read_exs.append(e)
            continue
        logger.log()
        if logger.check().print().is_warning():
            logger_warnings += 1

    if len(logger_arg_exs) > 0:
        print('\nCONFIGURATION ERROR: Could not instantiate some of the loggers!', file=sys.stderr)
        print_exs(logger_arg_exs, [f'{n}.' for n in range(1, 1 + len(logger_arg_exs))])
    if len(logger_read_exs) > 0:
        print('\nRUNTIME ERROR: Some loggers could not fetch sensor data!', file=sys.stderr)
        print_exs(logger_read_exs, [f'{n}.' for n in range(1, 1 + len(logger_read_exs))])

    if len(logger_arg_exs) + len(logger_read_exs) > 0 or logger_warnings > 0:
        exit(1)


def print_exs(exs: list[Exception], headers: list):
    for e, header in zip(exs, headers):
        # Indent str(e) with \t
        body = '\t' + '\n\t'.join(str(e).splitlines())

        print(f'{header}\n{body}', file=sys.stderr)


if __name__ == '__main__':
    main()
