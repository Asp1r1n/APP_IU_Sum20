from decor import reflect_print
from decor import reflect

@reflect_print
def foo():
    print('bar')

@reflect_print
def GG():
    print('GG')

if __name__ == '__main__':
    foo()
    GG()
