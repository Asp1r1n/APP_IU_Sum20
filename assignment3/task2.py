import inspect


def reflect(function):
    print("Name: " + function.__name__)
    print("Type: " + str(type(function)))
    print("Sign: " + str(inspect.signature(function)))
    print("Args: " + str(inspect.getargs(function.__code__).args))
    print("Doc: " + str(function.__doc__))
   # Args: positional(None,)

  #  Doc: This

    lines = inspect.getsource(function)
    print("Source: " + lines)
