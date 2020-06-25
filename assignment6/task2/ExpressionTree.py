class VariableNode:
    def __init__(self, value):
        self.__value = value

    def get_value(self) -> float:
        if float(self.__value).is_integer(): return int(self.__value)
        return float(self.__value)

    def __str__(self):
        return str(self.__value)


class ConstantNode:
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
            if c.isnumeric() or c == "." or c == "-":
                value += c
                i += 1
            else:
                break
        while i < len(constant):
            i += 1
            variable += c

        # print('val' + ' ' + value)
        if value == '': value = '1' 
        self.__value = float(value) # assumed that numbers are only in the begining and are valid
        self.__const = variable

    def __str__(self):
        s = []

        if self.get_value() != 1:
            s.append(str(self.get_value()) + str(self.get_constant()))
        else:
            s.append(str(self.get_constant()))
        if self.get_pow() > 1:
            s[-1] = s[-1] + '^' + str(self.__a.get_pow())

        return ' '.join(s)

    def get_value(self) -> float:
        if float(self.__value).is_integer(): return int(self.__value)
        return float(self.__value)

    def get_constant(self) -> str:
        return self.__const

    def get_pow(self) -> str:
        return self.__power


# becaues some old retards think its "cool" to initiate this dances with bicicles
def multiply(x, y):
    r = 0
    for i in range(0, int(x)):
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


def add(o, l, r):
    if isinstance(r, VariableNode):
        return VariableNode(l.get_value() + r.get_value())
    if isinstance(r, ConstantNode):
        # return ConstantNode.create(ConstantNode(""),
        #                            l.get_value() + r.get_value(),
        #                            r.get_constant())
        return ConstantNode(str(l.get_value() + r.get_value()) + str(r.get_constant()))

def sub(o, l, r):
    if l.get_value() < r.get_value():
        if o._OperatorNode__expression == "+":
            o._OperatorNode__expression = "-"
            if isinstance(r, VariableNode):
                return VariableNode(r.get_value() - l.get_value())
            if isinstance(r, ConstantNode):
                return ConstantNode(str(r.get_value() - l.get_value()) + str(r.get_constant()))
        else:
            if o._OperatorNode__expression == "-":
                o._OperatorNode__expression = "+"
                if isinstance(r, VariableNode):
                    return VariableNode(r.get_value() - l.get_value())
                if isinstance(r, ConstantNode):
                    return ConstantNode(str(r.get_value() - l.get_value()) + str(r.get_constant()))

    if isinstance(r, VariableNode):
        return VariableNode(l.get_value() - r.get_value())
    if isinstance(r, ConstantNode):
        return ConstantNode(str(l.get_value() - r.get_value()) + str(r.get_constant()))
        # return ConstantNode.create(ConstantNode(""),
        #                           l.get_value() - r.get_value(),
        #                           r.get_constant())




def mult(o, l, r):
    if isinstance(r, VariableNode):
        return VariableNode(multiply(l.get_value(), r.get_value()))
    if isinstance(r, ConstantNode):
        if l.get_pow() + r.get_pow() == 0:
            return VariableNode(multiply(l.__value, r.get_value()))
        else:
            # return ConstantNode.create(ConstantNode(""),
            #                            multiply(l.__value, r.get_value()),
            #                            r.get_constant(),
            #                            l.get_pow() + r.get_pow())
            return ConstantNode(str(multiply(l.get_value(), r.get_value())) + str(r.get_constant()) + '^' + str(l.get_pow() + r.get_pow()))


def div(o, l, r):
    if isinstance(r, VariableNode):
        return VariableNode(multiply(l.get_value(), r.get_value()))
    if isinstance(r, ConstantNode):
        if l.get_pow() == r.get_pow():
            return VariableNode(divide(l.__value, r.get_value()))
        else:
            # return ConstantNode.create(ConstantNode(""),
            #                            divide(l.__value, r.get_value()),
            #                            r.get_constant(),
            #                            l.get_pow() - r.get_pow())
            return ConstantNode(str(divide(l.get_value(), r.get_value())) + str(r.get_constant()) + '^' + str(l.get_pow() - r.get_pow()))


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

    def get_a(self):
        return self.__a

    def get_b(self):
        return self.__b

    def __str__(self):
        s = []

        if isinstance(self.__a, VariableNode):
            # s.append(str(self.__a.get_value()))
            s.append(str(self.__a))
        elif isinstance(self.__a, ConstantNode):
            # if self.__a.get_value() != 1:
            #     s.append(str(self.__a.get_value()) + str(self.__a.get_constant()))
            # s.append(str(self.__a.get_constant()))
            # if self.__a.get_pow() > 1:
            #     s[-1] = s[-1] + '^' + str(self.__a.get_pow())
            s.append(str(self.__b))

        s.append(str(self.__expression))


        if isinstance(self.__b, VariableNode):
            # s.append(str(self.__b.get_value()))
            s.append(str(self.__a))
        elif isinstance(self.__b, ConstantNode):
            # if self.__b.get_value() != 1:
            #     s.append(str(self.__b.get_value()) + str(self.__b.get_constant()))
            # else:
            #     s.append(str(self.__b.get_constant()))
            # if self.__b.get_pow() > 1:
            #     s[-1] = s[-1] + '^' + str(self.__b.get_pow())
            s.append(str(self.__b))

        return ' '.join(s)

    def evaluate(self):
        if isinstance(self.__a, OperatorNode):
            # print('here')
            self.__a = self.__a.evaluate()
        if isinstance(self.__b, OperatorNode):
            # print('here1')
            self.__b = self.__b.evaluate()
        return self.__execute_operator(self.__a, self.__b, self.__get_operator())

    def __get_operator(self):
        if self.__expression == "+":
            return lambda o, x, y: add(o, x, y)
        if self.__expression == "-":
            return lambda o, x, y: sub(o, x, y)
        if self.__expression == "*":
            return lambda o, x, y: mult(o, x, y)
        if self.__expression == "/":
            return lambda o, x, y: div(o, x, y)

    def __execute_operator(self, a, b, operator):
        if isinstance(a, VariableNode) and isinstance(b, VariableNode):
            return operator(self, a, b)
        if (isinstance(b, VariableNode) and isinstance(a, ConstantNode)) \
                or (isinstance(a, VariableNode) and isinstance(b, ConstantNode)):
            return self
        if isinstance(a, ConstantNode) and isinstance(b, ConstantNode):
            if a.get_constant() == b.get_constant():
                return operator(self, a, b)
            else:
                return self

        def apply_recursively(l: OperatorNode, r):
            if not isinstance(r, OperatorNode):
                if type(l.__a) == type(r):
                    l.__a = operator(l, l.__a, r)
                    return l
                if type(l.__b) == type(r):
                    l.__b = operator(l, l.__b, r)
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
