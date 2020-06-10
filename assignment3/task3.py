import inspect
import types
import io
from printer import print_reflection
from contextlib import redirect_stdout

def reflect(function):

  if not isinstance(function, types.FunctionType):
    raise TypeError
  
  def wrapper(*args, **kwargs):
      out = io.StringIO()
      with redirect_stdout(out):
          function(args, kwargs)
      print_reflection(Name = function.__name__, 
                        Type = str(type(function)),
                        Sign = str(inspect.signature(function)),
                        Args = ('positional ' + str(args), 'key=worded ' + str(kwargs)),
                        Doc = str(function.__doc__),
                        Source = ''.join(inspect.getsourcelines(function)[0][1:]),
                        Out = out.getvalue())
  return wrapper
