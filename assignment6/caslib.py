class Parser:

    @classmethod
    def validate(cls,expr:str):
        ib = 0
        cb = 0
        for ch in expr:
            if ch == '(': cb += 1
            if ch == ')': cb -= 1
            if ch == '[': ib += 1
            if ch == ']': ib -= 1

        return cb + ib == 0
    
    @classmethod
    def tokenize(cls,expr:str):
        l = []

        expression = expr

        if not cls.validate(expr):
            raise SyntaxError

        splited = expression.strip().split()
        
        for token in splited:
            t_word = []
            is_bracket = False
            for ch in token:

                t_word.append(ch)  
            
                if ch == '(':
                    if t_word != []:
                        l.append(''.join(t_word))
                        t_word.clear()

                if ch == ')':
                    if t_word != [] and len(t_word) != 1:
                        l.append(''.join(t_word[:-1]))
                        l.append(t_word[-1])
                    else:
                        l.append(t_word[0])
                    
                    t_word.clear()

            if t_word != []:
                l.append(''.join(t_word))

        return l

    @classmethod
    def parse(cls,expr:str):
        pfix = []
        tokens = Parser.tokenize(expr)
        print(tokens)

        prec = {'^':4, '*':3, '/':3, '+':2, '-':2, '(':1}
        precKeys = prec.keys()
        
        operators = []

        for token in tokens:
            if token not in precKeys and token not in [')']:
                pfix.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                top = operators.pop()
                while top != '(':
                    pfix.append(top)
                    top = operators.pop()
            else:
                while operators != [] and (prec[operators[-1]] >= prec[token]):
                    pfix.append(operators.pop())

                operators.append(token)

        while operators != []:
            pfix.append(operators.pop())

        return pfix

class BinaryTree:
    pass



if __name__ == '__main__':
    print(" ".join(Parser.parse('((42 * 5 * (5 + z) / -8) * (4 ^ 2)) + [0]')))
    print(" ".join(Parser.parse('A + B * S')))
        