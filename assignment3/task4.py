import inspect
import re
def reflect(function):
    print("Name: " + function.__name__)
    print("Type: " + str(type(function)))
    print("Sign: " + str(inspect.signature(function)))
    print("Args: " + str(inspect.getargs(function.__code__).args))
    print("Doc: " + str(function.__doc__))
    lines = inspect.getsource(function)
    print("Source: " + lines)

    pattern = re.compile(r'^ *if.*:$')
    iterator = re.finditer(pattern, lines)
    count = 0
    for match in iterator:
        count += 1
    print("Complexity:" + str(count))