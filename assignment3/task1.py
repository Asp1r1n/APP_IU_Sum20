from decor import reflect_print

@reflect_print  
@reflect_print
def foo(bar,sar):
    print(bar,sar)

@reflect_print
def GG():
    print('GG')

if __name__ == '__main__':
    foo()
    GG()
