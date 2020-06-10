import inspect
# can`t do it because reflect is not defined at the moment @reflect is used on it

def reflect(function):
    print("Name: " + function.__name__)
    print("Type: " + str(type(function)))
    print("Sign: " + str(inspect.signature(function)))
    print("Args: " + str(inspect.getargs(function.__code__).args))
    print("Doc: " + str(function.__doc__))
    lines = inspect.getsource(function)
    print("Source: " + lines)
