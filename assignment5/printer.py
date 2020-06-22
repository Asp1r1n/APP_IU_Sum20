import math
format_str = "{:>11}:   {}"
sub_str = "{:>10}:    {}"


def print_(*args, **kwargs):
    indx = 1
    for key, value in kwargs.items():
        print('[operators]')

        for k, v in list(value.items())[0:-5]:
            print(format_str.format(k, str(v)))

        N1 = sum(list(value.values())[0:-5])
        print(sub_str.format('N1', N1))
        print('\n')

        print('[operands]')
        for k, v in list(value.items())[-5:]:
            print(format_str.format(k, str(v)))

        N2 = sum(list(value.values())[-5:])
        print(sub_str.format('N2', N2))

        n1 = 21
        n2 = args[0][0]

        Pv = n1+n2
        N = N1+N2

        print('\n', '[program]')
        print(format_str.format('vocabulary', Pv))
        print(format_str.format('length', N))
        L = n1 * math.log2(n1) + n2 * math.log2(n2)
        print(format_str.format('calc_length', L))
        V = N * math.log2(Pv)
        print(format_str.format('volume', V))
        D = n1/2 * N2/n2
        print(format_str.format('difficulty', D))
        E = D*V
        print(format_str.format('effort', E))