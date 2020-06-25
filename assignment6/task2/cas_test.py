from caslib import Parser
from caslib import BinaryTree


if __name__ == '__main__':
    x = BinaryTree('x * y + y * x')
    print(x.evaluate_())


