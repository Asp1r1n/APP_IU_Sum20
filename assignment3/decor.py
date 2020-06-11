import inspect
import types
import io
import re
from printer import print_reflection
from contextlib import redirect_stdout

def complexity(lines, word):
    count = 0
    splited_lines = lines.splitlines()
    
    symbols = [')','(',';','"','"', "'", ':', '[',']','{','}']
    for line in splited_lines:
        new_line = ''
        for indx in range(len(line)):
            if line[indx] in symbols: new_line += ' '
            else: new_line += line[indx]
            
        for token in new_line.split():
            if token == word:
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
                            Complx = "{'" + word + "': " + str(complexity(lines, word)) + "}",
                            Source = lines,
                            Out = out.getvalue())
    return wrapper
  return reflect_decorator