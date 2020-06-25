from caslib import Parser
from caslib import BinaryTree
from ExpressionTree import VariableNode
import sys

execs = {}
exec_num = 0

def check_execs(expr):
    splited = expr.split()
    ret = []
    for token in splited:

        if token[0] == '[':
            if token in execs.keys():
                if isinstance(token, BinaryTree):
                    token = str(execs[token].evaluate_())
                else:
                    token = str(execs[token])   
            else:
                raise ValueError
        
        ret.append(token)
    
    return ' '.join(ret)


while True:
    input_ = input('>>>  ')

    if input_ == 'exit()':
        sys.exit()

    expression = input_
    if len(input_.split()) >= 3:
        input_ = check_execs(input_)
        expression = BinaryTree(input_)
        hash_indx = '[' + str(exec_num) + ']'
        execs[hash_indx] = expression
        print('[' + str(exec_num) + ']: ' + str(expression.evaluate_()))
    elif len(input_.split()) >= 1:
        input_ = check_execs(input_)
        expression = input_
        hash_indx = '[' + str(exec_num) + ']'
        execs[hash_indx] = VariableNode(expression)
        print('[' + str(exec_num) + ']: ' + str(expression))
    
    exec_num += 1
