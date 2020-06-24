from ExpressionTree import *


print(multiply(10 , 10))
#print(divide(1,10))
print(divide(1,7))

v = VariableNode("5x^8")

print(v.get_value())
print(v.get_constant())
print(v.get_pow())