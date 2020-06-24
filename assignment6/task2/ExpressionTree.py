class ConstantNode:
    def __init__(self, value):
        self.__value = value

    def get_value(self) -> float:
        return self.__value


class VariableNode:
    def create(self, value, name, power=1):
        self.__value = float(value)
        self.__const = str(name)
        self.__power = int(power)

    def __init__(self, constant: str):
        value = ""
        variable = ""
        i = 0;
        self.__power = 1
        if len(constant.split("^")) > 1:
            self.__power = constant.split("^")[1]
        constant = constant.split("^")[0]
        for c in constant:
            if c.isnumeric() or c == ".":
                value += c
                i += 1
            else:
                break
        while i < len(constant):
            i += 1
            variable += c
        self.__value = float(c)  # assumed that numbers are only in the begining and are valid
        self.__const = variable

    def get_value(self) -> float:
        return self.__value

    def get_constant(self) -> str:
        return self.__const

    def get_pow(self) -> str:
        return self.__power


# becaues some old retards think its "cool" to initiate this dances with bicicles
def multiply(x, y):
    r = 0
    for i in range(0, x):
        r += y
    return r


def divide(x, y):
    r = 0
    digit = 1

    while digit <= 100000000:
        if x >= y:
            x -= y
            r += 1 / digit
        if x < y:
            digit = multiply(10, digit)
            x = multiply(10, x)
    return r


def add(l, r):
    if isinstance(r, ConstantNode):
        return ConstantNode(l.get_value() + r.get_value())
    if isinstance(r, VariableNode):
        return VariableNode.create(VariableNode(""),
                                   l.__value + r.get_value(),
                                   r.get_constant())


def sub(l, r):
    if isinstance(r, ConstantNode):
        return ConstantNode(l.get_value() - r.get_value())
    if isinstance(r, VariableNode):
        return VariableNode.create(VariableNode(""),
                                   l.__value + r.get_value(),
                                   r.get_constant())


def mult(l, r):
    if isinstance(r, ConstantNode):
        return ConstantNode(multiply(l.get_value(), r.get_value()))
    if isinstance(r, VariableNode):
        if l.get_pow() + r.get_pow() == 0:
            return ConstantNode(multiply(l.__value, r.get_value()))
        else:
            return VariableNode.create(VariableNode(""),
                                       multiply(l.__value, r.get_value()),
                                       r.get_constant(),
                                       l.get_pow() + r.get_pow())


def div(l, r):
    if isinstance(r, ConstantNode):
        return ConstantNode(multiply(l.get_value(), r.get_value()))
    if isinstance(r, VariableNode):
        if l.get_pow() == r.get_pow():
            return ConstantNode(divide(l.__value, r.get_value()))
        else:
            return VariableNode.create(VariableNode(""),
                                       divide(l.__value, r.get_value()),
                                       r.get_constant(),
                                       l.get_pow() - r.get_pow())


class OperatorNode:
    def __init__(self, expression: str, a, b):
        if expression != "+" \
                and expression != "-" \
                and expression != "*" \
                and expression != "/":
            raise AttributeError()
        self.__expression = expression
        self.__a = a
        self.__b = b

    def evaluate(self):
        if isinstance(self.__a, OperatorNode):
            self.__a = self.__a.evaluate()
        if isinstance(self.__b, OperatorNode):
            self.__b = self.__b.evaluate()
        return self.__execute_operator(self.__a, self.__b, self.__get_operator())

    def __get_operator(self):
        if self.__expression == "+":
            return lambda x, y: add(x, y)
        if self.__expression == "-":
            return lambda x, y: sub(x, y)
        if self.__expression == "*":
            return lambda x, y: mult(x, y)
        if self.__expression == "/":
            return lambda x, y: div(x, y)

    def __execute_operator(self, a, b, operator):
        if isinstance(a, ConstantNode) and isinstance(b, ConstantNode):
            return operator(a, b)
        if (isinstance(b, ConstantNode) and isinstance(a, VariableNode)) \
                or (isinstance(a, ConstantNode) and isinstance(b, VariableNode)):
            return self
        if isinstance(a, VariableNode) and isinstance(b, VariableNode):
            if a.get_constant() == b.get_constant():
                return operator(a, b)
            else:
                return self

        def apply_recursively(l: OperatorNode, r):
            if not isinstance(r, OperatorNode):
                if isinstance(l.__a, VariableNode):
                    l.__a = operator(a, r)
                    return l
                if isinstance(l.__b, VariableNode):
                    l.__b = operator(b, r)
                    return l

            if apply_recursively(l.__a, r) is not None:
                return l
            if apply_recursively(l.__b, r) is not None:
                return l
            return None

        if isinstance(a, OperatorNode) and not isinstance(b, OperatorNode):
            result = apply_recursively(a, b)
            if result is not None:
                return result
        if isinstance(b, OperatorNode) and not isinstance(a, OperatorNode):
            result = apply_recursively(b, a)
            if result is not None:
                return result

        if isinstance(a, OperatorNode) and isinstance(b, OperatorNode):
            # idk what to do in this case
            1 + 1
        return self
