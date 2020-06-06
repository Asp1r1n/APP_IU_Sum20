import subprocess
import sys
import os
import time

COLUMN_NAMES = ["PROGRAM", "RANK", "TIME ELAPSED"]


def compile_all():
    for path in sys.argv[1:]:
        try:
            start = time.process_time()
            completed = subprocess.check_call(['python3', path], stdout=subprocess.DEVNULL)
            end = time.process_time()
            dif = end - start
            yield path, dif
        except Exception as e:
            print(e)
            yield path, sys.maxsize


def rank(run_data):
    run_data.sort(key=lambda tup: tup[1])
    r = 0
    prev_time = 0
    for item in run_data:
        if item[1] < sys.maxsize:
            if item[1] != prev_time:
                prev_time = item[1]
                r = r + 1
            yield item[0], r, item[1]
        else:
            yield item[0], '-', 'failed to run'


def print_table(column_names, data):
    h_line = "=" * 60 + "=" * 3
    head_format = "{0:<30}|{1:<15}|{2:<15}|"
    row_format = "{0:>30}|{1:>15}|{2:>15f}|"
    print(h_line,head_format.format(*column_names), h_line, *(row_format.format(*x) for x in data), h_line, sep='\n')


if len(sys.argv[1:]) != 0:
    ranked_statistics = list(compile_all())
    ranked_statistics = rank(ranked_statistics)
    print_table(COLUMN_NAMES, ranked_statistics)
else:
    print("usage: compare.py [files]")
    print("This program...")
