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
    return jch.join(l)

def normalize_docs(tokens:list):
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

def tokens(line):

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

        if ch == ' ' and not is_comment: is_word = False; is_delim = False; is_comment = False
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
                 if list_as_str(c_word) in DELIMETERS_S:
                     add_token()
        if ch == ' ' and c_word != []:
            if not is_comment and not is_str_lit:
                add_token()
    
    if c_word != []:
        add_token()
        
    return tokens


def startswith(line_tokens:list, starts:list):
    if line_tokens != []: return line_tokens[0] in starts

def calc_operators(lines:list, operators:list):
    ops_dict = dict.fromkeys(operators, 0)

    for line in lines:
        line_tokens = tokens(line)
        # TODO

    return ops_dict
    


input_file = fileinput.input()

for line in input_file:
    tokens_list = tokens(line.strip())
    mn_list = normalize_docs(tokens_list)
    print(line.strip())
    print('--->' + str(mn_list))





