from sanalyzelib import Reflection
from sanalyzelib import Decorators

@Reflection.reflect_decorator
@Decorators.stat_complexity
class Hello:
    x = 1
    y = 2


if __name__ == '__main__':
    Hello()