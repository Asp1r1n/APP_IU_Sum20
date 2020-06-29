### Python Programming for Software Engineers
### Assignment 7
### 'Lambda De Parser'


# Mikhail Sheinberg

# Task 1
# ----------------------------------------------
# Given the following:
f = lambda x, y: x * y

# 1. Rewrite to its logical equivalence using ordinary funcion definition(s)
# [code]

def f(x,y):
    return  x*y

# Task 2
# ----------------------------------------------
# Given the following:
f = lambda x: (lambda y: (lambda z: x + y + z))

# 1. How would you call it to get the result of `x + y + z`?
# [code]

r = f(4)(3)(2)
print(r)

# 2. Rewrite it using only one lambda expression and show how to call it
# [code]

f = lambda x,y,z:x+y+z

print(f(4,3,2))

# Task 3
# ----------------------------------------------
# Given the following:
(lambda b = (lambda *c: print(c)): b("a", "b"))()

# 1. What happens here? Rewrite it so that the code can be
# understood by a normal or your mate who has no idea what the lambda is!
# Provide comments, neat formatting and a bit more meaningful var names.


def two_args_func_caller(function = None):
    # default value for param, cause lambdas are prohibited
    def defult_function(*c):
        print(c)
    # if no value for function is provided we use default
    if function == None:
        function = defult_function
    function("a","b")

two_args_func_caller()
# Task 4 (soft)
# ----------------------------------------------
# What are the main restrictions on the lambda?
# Provide "If yes, why? If not, why not?" for each of the following:
# 1. Does lambda restrict side effects? No, you can call any function within lambda nd in it you can do anything:
# for example: lambda x,y : reboot_system()
# 2. Does lambda restrict number of allowed statements? Yes, it can have only one expression result of which will
# be returned as result of lambda
# 3. Does lambda restrict assignments? Yes, no =, +=, -= and so on are prohibited
# 4. Does lambda restrict number of return values? No, any tuple can be returned, next example is valid:
# f = lambda x, y: (x, y)
# a,b = f(3,4)
# print(a,b)
# 5. Does lambda restrict the use of default arguments values? Yes, you can use defualt values. Next example is valid:
# f = lambda x=10,y=100:x+y
# print(f())
# 6. Does lambda restrict possible function signatures? No they doesnt, all lambdas restrictions ae related to its body
# but they can take any number of parammeters of any type, and return same range of results as any normal function



# Task 5
# ----------------------------------------------
# Given the following:
(lambda f = (lambda a: (lambda b: print(list(map(lambda x: x+x, a+b))))):
f((1,2,3))((4,5,6)))()

# 1. What happens here? Do the same as in Task 3 and
# we have lambda f that contains one param that, have default value,
# which is lambda with param a and which returns lambda with param b
# param f is called with tuple (1,2,3) wich is passed to param a.
# f returns lambda with param b , that is called with tuple
# (4,5,6). Inside this lambda (with param b) two tuples (passed to a and b) are merged
# and each value inside of them is added two itself (lambda x)
# map will return generator so it is wrapped by list before be passed into print
# final brackets are used to call initial lambda (with param f) itself, and because no params are provided
# default value is used
# enumerate order of execution using (1,2,3...) in comments
# [multiline code interlaced with comments]
#           2                           9   8    7        6        5        3          4         1
# (lambda f = (lambda a: (lambda b: print(list(map(lambda x: x+x, a+b))))): f((1,2,3))((4,5,6)))()

# 2. Why does map() requires list() call?
# cause map will return iterator

