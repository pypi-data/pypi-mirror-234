#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
from collections import deque
from pathlib import Path


def read(file: Path) -> list[list[str]]:
    """
    Returns all rows from the CSV file `file`.
    """
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        return [row for row in reader]


def read_last(file: Path, num_rows: int, skip: int = 0) -> list[list[str]]:
    """
    Returns the last `num_rows` from the CSV file `file`.

    :param file:
    :param num_rows:
    :param skip: If given, the first `skip` rows are skipped.
    """
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Skip the first `skip` rows.
        for i in range(skip):
            try:
                next(reader)
            except StopIteration:
                break  # EOF

        # Read all other rows but only keep the last `num_rows` rows.
        q = deque(reader, num_rows)
        # Return the last `num_rows` as list.
        return [row for row in q]


def write(file: Path,
          rows: list[list[str]],
          header: list[str] = None,
          create_parent_dirs: bool = True,
          recreate_file: bool = False) -> None:
    """
    Create new .csv file if missing or append to existing .csv file.

    :param file:
    :param rows: The rows to write as csv table to file.
    :param header: If given will be inserted as first row into the csv table.
    :param create_parent_dirs: If `file.parent` does not exist, create it.
    :param recreate_file: Never append, always recreate the .csv file.
    """
    if create_parent_dirs and not file.parent.exists():
        file.parent.mkdir(parents=True, exist_ok=False)
    if recreate_file and file.exists():
        file.unlink(missing_ok=False)
    if file.exists():
        append(file, rows)
    else:
        if header is not None:
            rows = [header] + rows
        create(file, rows)

        text = file.read_text()
        if text.count('\n') != len(rows) or not text.endswith('\n'):
            raise Exception(f'Created a new csv file with {len(rows)} rows but it does not have {len(rows)} lines. '
                            f'Make sure that there are no concurrent writes to this file!')


def create(file: Path, rows: list[list[str]]) -> None:
    with open(file, 'x', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(rows)


def append(file: Path, rows: list[list[str]]) -> None:
    with open(file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(rows)


def test():
    file = Path('/var/log/de-p1st-monitor/cpu_avg.csv')
    data = read_last(file, 4, 10)
    print(data)


if __name__ == '__main__':
    test()
