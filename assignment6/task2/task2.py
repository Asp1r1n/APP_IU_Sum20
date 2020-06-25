from caslib import Parser
from caslib import BinaryTree
from ExpressionTree import VariableNode
import sys

execs = {}
expands = {}
exec_num = 0

#define is the complex token Example: 5/7
def istoken(s:str):

    for indx, ch in enumerate(s):
        if indx != 0:
            if ch in ['*','+','-']:
                return False
    return True

#expand the result of execution back to expression
def expand(expr):
    ret = []
    for token in expands[expr].split():

        if not istoken(token):
            ret = []
            break

        if token[0] == '[':
            if token in execs.keys():
                token = '(' + str(expands[token]) + ')'
            else:
                raise ValueError
        
        ret.append(token)
    
    return ' '.join(ret)

#validate method
#check is the expression is correctly formed
def check_execs(expr):
    splited = Parser.tokenize(expr)
    ret = []
    for token in splited:

        if not istoken(token):
            ret = []
            break

        if token[0] == '[':
            if token in execs.keys():
                token = '(' + str(execs[token]) + ')'
            else:
                raise ValueError
        
        ret.append(token)
    
    return ' '.join(ret)


# Exec loop
while True:
    input_ = input('>>>  ')

    if input_ == 'exit()':
        sys.exit()

    expression = input_

    

    


    try:
        expression = input_.split()
        if expression[0] == 'expand':
            if expression[1][0] != '[':
                raise ValueError
            
            print('[~]: ' + expand(expression[1]))

        elif len(input_.split()) >= 3:
            input_ = check_execs(input_)
            expression = input_
            hash_indx = '[' + str(exec_num) + ']'
            expands[hash_indx] = expression
            execs[hash_indx] = BinaryTree(expression).evaluate_()
            print('[' + str(exec_num) + ']: ' + str(execs[hash_indx]))
            exec_num += 1
        elif len(input_.split()) >= 1:
            if istoken(input_):
                input_ = check_execs(input_)
                expression = input_
                hash_indx = '[' + str(exec_num) + ']'
                expands[hash_indx] = expression
                execs[hash_indx] = expression
                print('[' + str(exec_num) + ']: ' + str(expression))
                exec_num += 1
            else:
                print('invalid expression')
    except ValueError:
        print('invalid expression')
    
