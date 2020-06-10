import inspect


def reflect(function):
    def wrapper(*args, **kwargs):
        lines = ''.join(inspect.getsourcelines(function)[0][1:])
        print(lines)
    return wrapper
