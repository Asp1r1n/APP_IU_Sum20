import inspect
import types
import io
import re
from printer import print_reflection
from contextlib import redirect_stdout

def complexity(lines, word):
    pattern = re.compile(r'\n *' + word + r'.*:\n')
    iterator = re.finditer(pattern, lines)
    count = 0
    for match in iterator:
        count += 1
    return count

def reflect(word = 'if'):

  def reflect_decorator(function):

    if not isinstance(function, types.FunctionType):
        raise TypeError
  
    def wrapper(*args, **kwargs):
        
        out = io.StringIO()
        with redirect_stdout(out):
            function(args, kwargs)

        lines = ''.join(inspect.getsourcelines(function)[0][1:])

        print_reflection(Name = function.__name__, 
                            Type = str(type(function)),
                            Sign = str(inspect.signature(function)),
                            Args = ('positional ' + str(args), 'key=worded ' + str(kwargs)),
                            Doc = str(function.__doc__),
                            Complexity = complexity(lines, word),
                            Source = lines,
                            Out = out.getvalue())
    return wrapper
  return reflect_decorator