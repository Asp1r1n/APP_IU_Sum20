import fileinput


IDENTIFIERS = ['ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789_']
KEYWORDS = ['if', 'elif', 'else', 'try', 'for', 'with', 'return', 'def', 'import', 'except']
OPERATORS = ['+', '-', '/', '*', '==', '!=', 'and', 'not', 'or', '=']
ARITHMETIC_OPERATORS = ['+', '-', '/', '*']
LOGIC_OPERATORS = ['==', '!=', 'and', 'not', 'or']
DELIMETERS_S = ['{','}', '(', ')', '[',']', ',', ':', '.', ';', '@']
DELIMETERS_C = ['//=', '%=','@=', '&=', '|=', '^=', '>>=', '<<=', '**=', '->', '+=', '-=', '*=', '/=']
SPECIAL_CHARS = ['"',"'", '#', '\\']
PY_OPS = ['+','-','*','**','/','//','%', '@' ,'<<','>>','&','|','^','~',':=','<','>','<=','>=','==','!=']
PY_DELIMETERS_S = ['=','{','}', '(', ')', '[',']', ',', ':', '.', ';', '@', '+', '-', '/','*','!','<','%','>','|','&','^']
PY_DELIMETERS_C = ['//=', '%=','@=', '&=', '|=', '^=', '>>=', '<<=', '**=', '->', '+=', '-=', '*=', '/=']
cmm_ch = '#'
str_chs = ['"',"'"]


def list_as_str(l:list, jch = ''):
    """ Conver the list of char to string """
    return jch.join(l)

def iscll(line):
    """ Identify is the line is complete logic line"""

    return line[-1] not in [',', '\\']

def isdoctoken(token):

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

def isinlinecomment(token):
    return token.startswith('#')


def normalize_docs(tokens:list):

    ''' Normalize the tokens of the particular string to form docs token as join
        Example: 
                String: """ This is doc string """; print('hello') 
                Tokens = ['""', '" This is doc string ", '""', ';' ,'print', '(' ,"'hello'", ')']
                Normilized string: ['""" This is doc string """', ';' ,'print', '(' ,"'hello'", ')'] '''

    empty_str_lit = ['""',"''"]

    new_tokens = []

    start_indx = -1;
    end_indx = -1;
    is_empty_str_lit = False
    doc_ch = ''

    is_doc_token = False
    doc_token = ''

    for indx,token in enumerate(tokens):
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

def normalize(lines:list):

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
                        
                Output: print_reflection(Name = function.__name__,Type = str(type(function)),Sign = str(inspect.signature(function)),Args = ('positional ' + str(args), 'key=worded ' + str(kwargs)),Doc = str(function.__doc__),Source = ''.join(inspect.getsourcelines(function)[0][1:]),Out = out.getvalue()) 
                
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

        if iscll(strip_line):

            doc_str = isdoctoken(strip_line)
            if doc_str != -1:
                dst = normalize_docs(tokens(strip_line))
                print(dst)
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

def tokens(line):

    ''' Split the line into tokens
    
        Example:
                String: Source = ''.join(inspect.getsourcelines(function)[0][1:]) 
                Output: ['Source', '=', "''", '.', 'join', '(', 'inspect', '.', 'getsourcelines', '(', 'function', ')', '[', '0', ']', '[', '1', ':', ']', ')'] '''

    tokens = []
    is_delim = False
    is_cmpd_delim = False
    is_word = False
    is_comment = False
    is_str_lit = False

    str_lit_ch  = ''
    c_word = []

    def add_token():
        tokens.append(list_as_str(c_word))
        c_word.clear()


    for ch in line:

        if ch == ' ' and not is_comment:
            is_word = False
            is_delim = False
            is_comment = False
        elif ch in str_chs:
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
        elif ch == cmm_ch:
            if c_word != []: 
                add_token()
            is_comment = True;
        elif ch not in PY_DELIMETERS_S:
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
                 if list_as_str(c_word) in DELIMETERS_C:
                     add_token()
        if ch == ' ' and c_word != []:
            if not is_comment and not is_str_lit:
                add_token()
    
    if c_word != []:
        add_token()
        
    return tokens


def startswith(line_tokens:list, starts:list):
    if line_tokens != []: return line_tokens[0] in starts

def is_entity(l_tokens, rec_indx):

    ''' Define is the tokens form the entity'''

    for indx,token in enumerate(l_tokens):
        if token == 'def':
            return True
        if token == '=':
            if rec_indx == 0 :
                if is_py_name(l_tokens[indx - 1]):
                    return True

def is_valid_var_ch(ch):

    ''' Define is the char within the valid variable name'''

    return (ord(ch) >= 65 and ord(ch) <= 90) or \
                (ord(ch) >= 97 and ord(ch) <= 122) or \
                    (ord(ch) >= 48 and ord(ch) <= 57) or ord(ch) == 95

def is_py_name(token:str):

    ''' Define is the token represents the valid python variable name'''

    ret = True
    for indx,ch in enumerate(token):
        if indx == 0:
            if is_valid_var_ch(ch) and (ord(ch) < 48 and ord(ch) > 57):
                ret = False
                break
        elif not is_valid_var_ch(ch):
            ret = False
            break

    return ret

def calc_total_sum(dict):
    return sum(dict.values())


def isstrliteral(token):
    return (token.startswith('"') and token.endswith('"')) \
           or (token.startswith("'") and token.endswith("'"))


def isnumericliteral(l_tokens):
    if len(l_tokens) == 1:
        return l_tokens[0].isdigit()

    elif len(l_tokens) == 3:
        return l_tokens[0].isdigit() and l_tokens[1] == '.' and l_tokens [2].isdigit()


def calc_operators(lines:list):
    ''' Calculates the define operators within the source code'''

    # operators list 
    operands = []
    operands.extend(ARITHMETIC_OPERATORS)
    operands.extend(KEYWORDS)
    operands.extend(LOGIC_OPERATORS)
    operands.append('=')
    operands.append('calls')
    print(operands)
    ops_dict = {key:0 for key in operands}
    opns_dict = {'inlinedocs': 0, 'docstrings': 0, 'literals': 0, 'entities': 0, 'args': 0}

    def process(l_tokens,idx = 0,o_dict = ops_dict,on_dict = opns_dict):
        print(l_tokens, ' ', idx)

        args_count = 0
        offset = 0

        indx = 0
        while indx < len(l_tokens):
            offset = indx
            token = l_tokens[indx]

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
                if indx != 0 and not is_entity(l_tokens[0:indx], idx):
                    tkn = l_tokens[indx - 1]
                    if is_py_name(tkn) and tkn not in KEYWORDS  and tkn not in SPECIAL_CHARS:
                        ops_dict['calls'] += 1
                        offset, args_count = process(l_tokens[indx + 1:],idx + 1)
                        opns_dict['args'] += args_count
                        indx += offset + 2
                        continue
            
            if is_entity(l_tokens[0:], idx):
                print(l_tokens[0:])
                opns_dict['entities'] += 1
                break

            if isdoctoken(token) != -1:
                opns_dict['docstrings'] += 1

            if isinlinecomment(token):
                opns_dict['inlinedocs'] += 1
                        
            if isstrliteral(token):
                opns_dict['literals'] += 1

            if token.isdigit():
                if indx + 2  < len(l_tokens):
                    if isnumericliteral([token, l_tokens[indx + 1], l_tokens[indx + 2]]):
                        opns_dict['literals'] += 1
                    else:
                        opns_dict['literals'] += 1
            
            if token in operands[:len(operands)]:
                ops_dict[token] += 1

            indx += 1

        return offset, args_count

    for line in lines:
        line_tokens = normalize_docs(tokens(line))
        process(line_tokens, 0)

    return ops_dict, opns_dict
    


input_file = fileinput.input()

if __name__ == '__main__':
    import printer
    n_lines = normalize(input_file)

    ret_dict, opns_dict = calc_operators(n_lines)
    printer.print_(operators = ret_dict, operands = opns_dict)




