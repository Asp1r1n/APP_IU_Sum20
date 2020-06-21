import sanalyzelib

@sanalyzelib.Decorators.stat_complexity
def test_complexity():

    def is_valid_var_ch(ch):
        ''' Define is the char within the valid variable name'''
        return (ord(ch) >= 65 and ord(ch) <= 90) or \
           (ord(ch) >= 97 and ord(ch) <= 122) or \
           (ord(ch) >= 48 and ord(ch) <= 57) or ord(ch) == 95

    def is_py_name(token: str):
        ''' Define is the token represents the valid python variable name'''

        ret = True
        for indx, ch in enumerate(token):
            if indx == 0:
                if is_valid_var_ch(ch) and ch == '_':
                    ret = False
                    break
            elif not is_valid_var_ch(ch):
                ret = False
                break

        return ret
    
    print('test')

if __name__ == '__main__':
    test_complexity()

    print(sanalyzelib.Tokenizer.tokens('def is_valid_char():'))