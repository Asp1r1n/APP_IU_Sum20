import inspect


def reflect(function):
    '''Decorator return the code of the call function.
        get sources from file, and print it (more info in inspect module)
        This is not quine because we print out only part of the program'''

    def wrapper(*args, **kwargs):
        lines = ''.join(inspect.getsourcelines(function)[0][1:])
        print(lines)
    return wrapper
