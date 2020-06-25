import ExpressionTree

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
        # print(tokens)
        prec = {'*':3, '/':3, '+':2, '-':2, '(':1}
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

        # print(' '.join(pfix))

        return pfix

class BinaryTree:

    def __init__(self,expr:str):
        self.head = self.__buildtree(expr)

    def __buildtree(self,expr:str):
        operators = ['*','/','+','-']
        pfix = Parser.parse(expr)
        stack = []
        first = True
        for token in pfix:
            # print(token)
            # print(stack)
            if token not in operators:
                node = token
                if self.__is_float(token):
                    print(token)
                    if '/' in token:
                        node = ExpressionTree.ConstantNode(token)
                    # print(token + ' -variable')
                    else:
                        node = ExpressionTree.VariableNode(token)
                else:
                    # print(token + ' -constant')
                    node = ExpressionTree.ConstantNode(token)

                stack.append(node)
            else:
                # print(token)
                left = stack.pop()
                right = stack.pop()
                opNode = ExpressionTree.OperatorNode(token, right, left)
                stack.append(opNode)

        # print(stack)

        if len(stack) != 1:
            raise ValueError
            
        return stack.pop()


    # def show(self, node):
    #     if not isinstance(node, ExpressionTree.VariableNode) \
    #         and not isinstance(node, ExpressionTree.ConstantNode):
    #             self.show(node.get_b())
    #             self.show(node.get_a())

    #     print(node)

    def evaluate_(self):
        return self.head.evaluate()

    def __is_float(self,s:str):
        try:
            if '/' in s:
                x = int(s[:s.find('/')]) / int(s[s.find('/') + 1:])
                float(x)
            else:
                float(s)
            return True
        except ValueError:
            return False



if __name__ == '__main__':
    print(" ".join(Parser.parse('((42 * 5 * (5 + z) / -8) * (x^2)) + [0]')))
    print(" ".join(Parser.tokenize('(5/6) - 1/6')))
    x = BinaryTree('x + 5x')
    print(x.evaluate_())
        