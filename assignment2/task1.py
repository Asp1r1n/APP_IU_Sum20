import subprocess
import sys
import timeit

COLUMN_NAMES = ["PROGRAM", "RANK", "TIME ELAPSED"]


def compile_all():
    for path in sys.argv[1:]:
        try:
            start = timeit.timeit()
            #subprocess.popen(path)
            exec(open(path).read(), {})
            end = timeit.timeit()
            dif = end - start
            yield path, dif
        except Exception:
            yield path, sys.maxsize


def rank(run_data):
    run_data.sort(key=lambda tup: tup[1])
    r = 1
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
    row_format = "{:>30}" * len(column_names)
    print(row_format.format(*column_names))
    for row in data:
        print(row_format.format(*row))


ranked_statistics = list(compile_all())
ranked_statistics = rank(ranked_statistics)
print_table(COLUMN_NAMES, ranked_statistics)
