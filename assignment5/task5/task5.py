from sanalyzelib import Reflection
from sanalyzelib import Decorators

# @sanalyzelib.Decorators.stat_object
# @sanalyzelib.Decorators.stat_complexity
@Reflection.reflect_decorator
@Decorators.stat_complexity
def test_complexity():

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


if __name__ == '__main__':
    test_complexity()