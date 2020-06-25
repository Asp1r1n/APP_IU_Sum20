from caslib import Parser
from caslib import BinaryTree


if __name__ == '__main__':
    x = BinaryTree('x * (2 + 4 * y)')
    print(x.evaluate_())


