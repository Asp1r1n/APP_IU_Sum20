import inspect
import types

def reflect(func):

    if not isinstance(func, types.FunctionType):
        raise TypeError
    
    def wrapper():
        print(inspect.getsource(func))
    return wrapper

def reflect_print(func):

    '''Get the source file of func object, find the line of call decorator,
        print the line of source func wrapped by this decorator '''

    if not isinstance(func, types.FunctionType):
        raise TypeError
    
    def wrapper():
        print(''.join(inspect.getsourcelines(func)[0][1:]))
    return wrapper