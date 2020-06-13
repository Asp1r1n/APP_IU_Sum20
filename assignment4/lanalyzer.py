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


def tokens(line):

    tokens = []
    is_delim = False
    is_cmpd_delim = False
    is_word = False
    is_comment = False
    is_str_lit = False

    str_lit_ch  = ''
    c_word = []
    for indx,ch in enumerate(line):

        if ch == ' ' and not is_comment: is_word = False; is_delim = False; is_comment = False
        elif ch in str_chs:
            if not is_str_lit: 
                if c_word != []:
                    tokens.append(list_as_str(c_word))
                    c_word.clear()
                
                str_lit_ch = ch
                is_str_lit = True
            else:
                if ch == str_lit_ch:
                    c_word.append(ch)
                    tokens.append(list_as_str(c_word))
                    c_word.clear()
                    is_str_lit = False
                    continue
        elif ch == cmm_ch:
            if c_word != []: 
                tokens.append(list_as_str(c_word))
                c_word.clear()
            is_comment = True;
        elif ch not in PY_DELIMETERS_S:
            if is_delim and not is_str_lit:
                if c_word != []:
                    tokens.append(list_as_str(c_word))
                    c_word.clear()
                is_delim = False
            is_word = True
        else:
            if is_word and not is_str_lit:
                if c_word != []:
                    tokens.append(list_as_str(c_word))
                    c_word.clear()
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
                     tokens.append(ch)
                     c_word.clear()

        if ch == ' ' and c_word != []:
            if not is_comment and not is_str_lit:
                tokens.append(list_as_str(c_word))
                c_word.clear()
    
    if c_word != []:
        tokens.append(list_as_str(c_word))
        
    return tokens


input_file = fileinput.input()

for line in input_file:
    tokens_list = tokens(line.strip())
    print(tokens_list)





