import inspect


def reflect(function):
    lines = inspect.getsource(function)
    print(lines)