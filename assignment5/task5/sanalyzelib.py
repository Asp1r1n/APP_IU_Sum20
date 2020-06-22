import inspect
import types
import io
import math
from contextlib import redirect_stdout

class Grammar:

    IDENTIFIERS = ['ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789_']
    KEYWORDS = ['if', 'elif', 'else', 'try', 'for', 'with', 'return', 'def', 'import', 'except']
    OPERATORS = ['+', '-', '/', '*', '==', '!=', 'and', 'not', 'or', '=']
    ARITHMETIC_OPERATORS = ['+', '-', '/', '*']
    LOGIC_OPERATORS = ['==', '!=', 'and', 'not', 'or']
    DELIMETERS_S = ['{', '}', '(', ')', '[', ']', ',', ':', '.', ';', '@']
    DELIMETERS_C = ['//=', '%=', '@=', '&=', '|=', '^=', '>>=', '<<=', '**=', '->', '+=', '-=', '*=', '/=']
    SPECIAL_CHARS = ['"', "'", '#', '\\']
    PY_OPS = ['+', '-', '*', '**', '/', '//', '%', '@', '<<', '>>', '&', '|',
                '^', '~', ':=', '<', '>', '<=', '>=', '==','!=']
    PY_DELIMETERS_S = ['=', '{', '}', '(', ')', '[', ']', ',', ':', '.', ';', '@',
                        '+', '-', '/', '*', '!', '<', '%', '>','|', '&', '^']
    PY_DELIMETERS_C = ['//=', '%=', '@=', '&=', '|=', '^=', '>>=', '<<=', '**=', '->', '+=', '-=', '*=', '/=']
    cmm_ch = '#'
    str_chs = ['"', "'"]

    @staticmethod
    def is_valid_var_ch(ch):
        ''' Define is the char within the valid variable name'''
        return (ord(ch) >= 65 and ord(ch) <= 90) or \
           (ord(ch) >= 97 and ord(ch) <= 122) or \
           (ord(ch) >= 48 and ord(ch) <= 57) or ord(ch) == 95

    @staticmethod
    def isstrliteral(token):
        return (token.startswith('"') and token.endswith('"')) \
            or (token.startswith("'") and token.endswith("'"))

    @staticmethod
    def isnumericliteral(l_tokens):
        if len(l_tokens) == 1:
            return l_tokens[0].isdigit()

        elif len(l_tokens) == 3:
            return l_tokens[0].isdigit() and l_tokens[1] == '.' and l_tokens [2].isdigit()

    @staticmethod
    def is_doctoken(token):
        """ Identify is the token is doc token"""

        ret = -1

        if (token.startswith("'''") and token.endswith("'''")) or \
                (token.startswith('"""') and token.endswith('"""')):
            ret = 1
        elif token.endswith('"""') or token.endswith("'''"):
            ret = 2
        elif token.startswith("'''") or token.startswith('"""'):
            ret = 0

        return ret

    @staticmethod
    def isinlinecomment(token):
        return token.startswith("#")

    @staticmethod
    def is_entity(l_tokens, rec_indx):
        ''' Define is the tokens form the entity'''

        for indx, token in enumerate(l_tokens):
            if token == 'def':
                return True
            if token == 'class':
                return True
            if token == '=':
                if rec_indx != 0:
                    if Grammar.is_py_name(l_tokens[indx - 1]):
                        return True

    @staticmethod
    def is_py_name(token: str):
        ''' Define is the token represents the valid python variable name'''

        ret = True
        for indx, ch in enumerate(token):
            if indx == 0:
                if Grammar.is_valid_var_ch(ch) and (ord(ch) < 48 and ord(ch) > 57):
                    ret = False
                    break
            elif not Grammar.is_valid_var_ch(ch):
                ret = False
                break

        return ret


class Helper:
    
    @staticmethod
    def list_as_str(l: list, jch=''):
        """ Conver the list of char to string """
        return jch.join(l)

    @staticmethod
    def iscll(line):
        """ Identify is the line is complete logic line"""
        return line[-1] not in [',', '\\']

    @staticmethod
    def startswith(line_tokens: list, starts: list):
        if line_tokens != []: return line_tokens[0] in starts
    


class Tokenizer:

    @staticmethod
    def tokens(line):

        ''' Split the line into tokens
            Example:
                    String: Source = ''.join(inspect.getsourcelines(function)[0][1:]) 
                    Output: ['Source', '=', "''", '.', 'join', '(', 'inspect', '.', 'getsourcelines', '(', 'function', ')', '[', '0', ']', '[', '1', ':', ']', ')'] '''

        def add_token():
            tokens.append(Helper.list_as_str(c_word))
            c_word.clear()
        
        
        tokens = []
        is_delim = False
        is_cmpd_delim = False
        is_word = False
        is_comment = False
        is_str_lit = False

        str_lit_ch = ''
        c_word = []

        for ch in line:

            if ch == ' ' and not is_comment:
                is_word = False
                is_delim = False
                is_comment = False
            elif ch in Grammar.str_chs:
                if not is_str_lit:
                    if c_word != []:
                        add_token()
                        str_lit_ch = ch
                        is_str_lit = True
                else:
                    if ch == str_lit_ch:
                        c_word.append(ch)
                        add_token()
                        is_str_lit = False
                        continue
            elif ch == Grammar.cmm_ch:
                if c_word != []:
                    add_token()
                is_comment = True;
            elif ch not in Grammar.PY_DELIMETERS_S:
                if is_delim and not is_str_lit:
                    if c_word != []:
                        add_token()
                    is_delim = False
                is_word = True
            else:
                if is_word and not is_str_lit:
                    if c_word != []:
                        add_token()
                    is_word = False
                is_delim = True

            if is_str_lit:
                c_word.append(ch)
            elif is_comment:
                if len(c_word) == 0 and ch == ' ':
                    continue
                c_word.append(ch)
            elif is_word or is_delim:
                c_word.append(ch)
                if is_delim:
                    if Helper.list_as_str(c_word) not in Grammar.DELIMETERS_S:
                        add_token()
            if ch == ' ' and c_word != []:
                if not is_comment and not is_str_lit:
                    add_token()

        if c_word != []:
            add_token()

        return tokens

    @staticmethod
    def normalize_docs(tokens: list):
        ''' Normalize the tokens of the particular string to form docs token as join
            Example: 
                    String: """ This is doc string """; print('hello') 
                    Tokens = ['""', '" This is doc string ", '""', ';' ,'print', '(' ,"'hello'", ')']
                    Normilized string: ['""" This is doc string """', ';' ,'print', '(' ,"'hello'", ')'] '''

        empty_str_lit = ['""', "''"]

        new_tokens = []

        start_indx = -1;
        end_indx = -1;
        is_empty_str_lit = False
        doc_ch = ''

        is_doc_token = False
        doc_token = ''

        for indx, token in enumerate(tokens):
            if token in empty_str_lit:
                if not is_empty_str_lit:
                    doc_ch = token[0]
                    start_indx = indx
                    is_empty_str_lit = True
                else:
                    if token[0] == doc_ch:
                        end_indx = indx
                        is_empty_str_lit = False

            if start_indx != -1 and not is_doc_token:
                if start_indx == indx - 1:
                    if token.startswith(doc_ch):
                        is_doc_token = True
                        doc_token = tokens[start_indx] + token
                    else:
                        is_empty_str_lit = False
                        is_doc_token = False
                        new_tokens.append(tokens[start_indx])
                        start_indx = -1
                        end_indx = -1

            if is_doc_token:
                if end_indx == -1:
                    if start_indx != indx - 1:
                        doc_token += ' ' + token
                else:
                    doc_token += token
                    is_empty_str_lit = False
                    is_doc_token = False
                    start_indx = -1
                    end_indx = -1
                    new_tokens.append(doc_token)
                    doc_token = ''
            elif start_indx == -1 and not is_doc_token:
                new_tokens.append(token)

        if doc_token != '':
            if tokens[0] in empty_str_lit:
                new_tokens.append(doc_token)
            elif tokens[len(tokens) - 2] in empty_str_lit:
                new_tokens = [' '.join(tokens[0:len(tokens) - 2]) + doc_token]

        return new_tokens
    

class Reflection:

    @staticmethod
    def print_reflection(*args, **kwargs):

        format_str = "{:>10}:   {}"
        sub_str = "{:>10}    {}"

        for key,value in kwargs.items():
            if type(value) is str:
                value = value.splitlines()    
            
            for indx, val in enumerate(value):
                if indx == 0: print(format_str.format(key, val))
                else: print(sub_str.format('',val))

            print()


    @staticmethod
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



    @staticmethod
    def reflect_decorator(function):

        is_func = True

        if not isinstance(function, types.FunctionType):
            is_func = False

        def wrapper():

                lines = ''.join(inspect.getsourcelines(function)[0][1:])
                args = ''
                kwargs = ''

                
                if is_func:
                    if hasattr(function, 'args'):
                        args = getattr(function, args)
                    if hasattr(function, 'kwargs'):
                        kwargs = getattr(function,'kwargs')
                
                out = io.StringIO()

                if is_func:
                    with redirect_stdout(out):
                        if args != '' and kwargs != '':
                            function(args, kwargs)
                        elif args != '':
                            function(args)
                        elif kwargs != '':
                            function(kwargs)
                        else:
                            function()


                o_dict = ''
                
                if is_func:
                    o_dict = {'Name': function.__name__, 'Type': str(type(function)), 'Sign':  str(inspect.signature(function)),
                            'Args': ('positional ' + str(args), 'key=worded ' + str(kwargs)), 'Doc': str(function.__doc__),
                            'Source': lines[1:], 'Out': out.getvalue() }

                else:
                    o_dict = {'Name': function.__name__, 'Type': str(type(function)), 'Doc': str(function.__doc__), 'Members': str(inspect.getmembers(function, lambda a:not(inspect.isroutine(a)))),
                            'Source': lines[1:]}

                

                # Reflection.print_reflection(Name = function.__name__, 
                #                     Type = str(type(function)),
                #                     Sign = str(inspect.signature(function)),
                #                     Args = ('positional ' + str(args), 'key=worded ' + str(kwargs)),
                #                     Doc = str(function.__doc__),
                #                     Source = lines,
                #                     Out = out.getvalue())

                print(o_dict)
        return wrapper

class Analyzer:

    @staticmethod
    def normalize(lines: list):
        ''' Normalize the physical lines to logical lines if possible, also includes the normilizing of multiple docs comments to one line
            Exmaple:
                    E1:  """asd asd asd 
                            asd asd asd asd 
                            asdasd asd asd asd 
                            asd asd asd asd as d
                            asd asd asd asd asd """
                    Output:  """asd asd asd\nasd asd asd asd\nasdasd asd asd asd\nasd asd asd asd as d\nasd asd asd asd asd """
                    
                    
                    E2: print_reflection(Name = function.__name__, 
                            Type = str(type(function)),
                            Sign = str(inspect.signature(function)),
                            Args = ('positional ' + str(args), 'key=worded ' + str(kwargs)),
                            Doc = str(function.__doc__),
                            Source = ''.join(inspect.getsourcelines(function)[0][1:]),
                            Out = out.getvalue()) 
                            
                    Output: print_reflection(Name = function.__name__,Type = str(type(function)),
                            Sign = str(inspect.signature(function)),Args = ('positional ' + str(args), 'key=worded ' + str(kwargs)),
                            Doc = str(function.__doc__),Source = ''.join(inspect.getsourcelines(function)[0][1:]),Out = out.getvalue()) 
                            as single line
                    
                    E3:   a = 'asd' + \\
                            'asd
                            
                    Output: a = 'asd' + \\'asd '''
        new_lines = []

        is_cll = False
        is_doc = False
        ln = ''
        for line in lines:
            strip_line = line.strip()

            if strip_line == '': continue

            ln += strip_line

            if Helper.iscll(strip_line):

                doc_str = Grammar.is_doctoken(strip_line)
                if doc_str != -1:
                    dst = Tokenizer.normalize_docs(Tokenizer.tokens(strip_line))
                    if len(dst) == 1:
                        if doc_str == 0:
                            is_doc = True
                            ln += '\\n '
                            continue
                        if doc_str == 2:
                            is_doc = False

                if is_doc:
                    ln += '\\n'

                elif not is_doc:
                    new_lines.append(ln)
                    ln = ''

        return new_lines

    @staticmethod
    def find_args_end(l_tokens):
        brakets_counter = 1;
        for indx, token in enumerate(l_tokens):
            if token == '(': brakets_counter += 1;
            if token == ')': brakets_counter -= 1;
            if brakets_counter == 0: return indx
    
    @staticmethod
    def calc_operators(lines: list):
        ''' Calculates the define operators within the source code'''

        # operators list 
        operands = []
        operands.extend(Grammar.ARITHMETIC_OPERATORS)
        operands.extend(Grammar.KEYWORDS)
        operands.extend(Grammar.LOGIC_OPERATORS)
        operands.append('=')
        operands.append('calls')
        ops_dict = {key:0 for key in operands}
        opns_dict = {'inlinedocs': 0, 'docstrings': 0, 'literals': 0, 'entities': 0, 'args': 0}

        def process(l_tokens,idx = 0,o_dict = ops_dict,on_dict = opns_dict):
            args_count = 0
            offset = 0

            indx = 0
            while indx < len(l_tokens):
                offset = indx
                token = l_tokens[indx]

                if Grammar.is_entity(l_tokens[0:], idx):
                    opns_dict['entities'] += 1
                    break


                if idx != 0:
                    if token == ',':
                        args_count += 1

                if token == ')':
                    if idx != 0:
                        if len(l_tokens) > 1:
                            if args_count == 0:
                                args_count = 1
                        return offset, args_count


                if token == '(':
                    if indx != 0 and not Grammar.is_entity(l_tokens[0:indx], idx):
                        tkn = l_tokens[indx - 1]
                        if Grammar.is_py_name(tkn) and tkn not in Grammar.KEYWORDS  and tkn not in Grammar.SPECIAL_CHARS:
                            ops_dict['calls'] += 1
                            offset, args_count = process(l_tokens[indx + 1:],idx + 1)
                            opns_dict['args'] += args_count
                            indx += offset + 2
                            continue
                
                if Grammar.is_doctoken(token) != -1:
                    opns_dict['docstrings'] += 1

                if Grammar.isinlinecomment(token):
                    opns_dict['inlinedocs'] += 1
                            
                if Grammar.isstrliteral(token):
                    opns_dict['literals'] += 1

                if token.isdigit():
                    if indx + 2  < len(l_tokens):
                        if Grammar.isnumericliteral([token, l_tokens[indx + 1], l_tokens[indx + 2]]):
                            opns_dict['literals'] += 1
                        else:
                            opns_dict['literals'] += 1
                    else:
                         opns_dict['literals'] += 1
                
                if token in operands[:len(operands)]:
                    ops_dict[token] += 1

                indx += 1

            return offset, args_count

        for line in lines:
            line_tokens = Tokenizer.normalize_docs(Tokenizer.tokens(line))
            offset, args_count = process(line_tokens, 0)

        return ops_dict, opns_dict

    # @staticmethod
    # def print_(*args, **kwargs):

    #     format_str = "{:>11}:   {}"
    #     sub_str = "{:>10}:    {}"

    #     indx = 1
    #     for key, value in kwargs.items():
    #         print('[operators]')

    #         for k, v in list(value.items())[0:-5]:
    #             print(format_str.format(k, str(v)))

    #         N1 = sum(list(value.values())[0:-5])
    #         print(sub_str.format('N1', N1))
    #         print('\n')

    #         print('[operands]')
    #         for k, v in list(value.items())[-5:]:
    #             print(format_str.format(k, str(v)))

    #         N2 = sum(list(value.values())[-5:])
    #         print(sub_str.format('N2', N2))

    #         n1 = 21
    #         n2 = args[0][0]

    #         Pv = n1+n2
    #         N = N1+N2

    #         print('\n', '[program]')
    #         print(format_str.format('vocabulary', Pv))
    #         print(format_str.format('length', N))
    #         L = n1 * math.log2(n1) + n2 * math.log2(n2)
    #         print(format_str.format('calc_length', L))
    #         V = N * math.log2(Pv)
    #         print(format_str.format('volume', V))
    #         D = n1/2 * N2/n2
    #         print(format_str.format('difficulty', D))
    #         E = D*V
    #         print(format_str.format('effort', E))

    @staticmethod
    def calc_program(ops_dict, opns_dict):

        prog_dict = {key:0 for key in ['vocabulary', 'length', 'calc_length', 'volume', 'difficulty', 'effort']}

        n1 = len(ops_dict.keys())
        n2 = len(opns_dict.keys())

        n = n1 + n2

        prog_dict['vocabulary'] = n
        prog_dict['length'] = sum(ops_dict.values()) + sum(opns_dict.values())
        prog_dict['calc_length'] =  int(n1 * math.log2(n1) + n2 * math.log2(n2))
        prog_dict['volume'] = int(prog_dict['length'] * math.log2(n))
        prog_dict['difficulty'] = int(n1 / 2 * sum(opns_dict.values()) / n2)
        prog_dict['effort'] = prog_dict['difficulty'] * prog_dict['volume']

        return prog_dict


    @staticmethod
    def print_(*args, **kwargs):

        format_str = "{:>11}:   {}"
        sub_str = "{:>11}    {}"

        indx = 1
        for key, value in kwargs.items():
            print('[' + key + ']')

            for k, v in value.items():
                print(format_str.format(k, str(v)))

            if key != 'program':
                print('\n', format_str.format('N' + str(indx), str(sum(value.values()))))
            indx += 1

class Decorators:
    
    stat_object = Reflection.reflect_decorator
    
    @staticmethod
    def stat_complexity(function):
        
        lines = inspect.getsourcelines(function)[0][1:]
        n_lines = Analyzer.normalize(lines)
        ops_dict, opns_dict  = Analyzer.calc_operators(n_lines)
        prog_dict = Analyzer.calc_program(ops_dict, opns_dict)
            # Analyzer.print_(operators = ops_dict, operands= opns_dict, program = prog_dict)
        a_dict = {'operators': ops_dict, 'operands': opns_dict, 'program': prog_dict}
        print(a_dict)

        return function

class Stat_object:
    pass




