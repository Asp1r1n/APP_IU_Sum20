from sanalyzelib import Reflection
from sanalyzelib import Decorators


# @sanalyzelib.Decorators.stat_object
# @sanalyzelib.Decorators.stat_complexity
@Reflection.reflect_decorator
@Decorators.stat_complexity
def test_complexity():
    """ This function does nothing useful
        :param bar1: description
        :param bar2: description
    """
    if True == True:
        print("Its ok")
    else:
        print("Ay-ya-ya-ya-Indiaaaaaaa")
        print("ruppy comes ruppy goes")
        print("give me my money")

    if False == True:
        print("We do american magic hear")
    else:
        print("And hear we do real")

    for val in [1, 2, 3]:
        print(val)

    print(1);
    print(2);
    print(3);
    print(5)

    print('test')


if __name__ == '__main__':
    test_complexity()
