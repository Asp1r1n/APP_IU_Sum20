import math
format_str = "{:>10}:   {}"
sub_str = "{:>10}    {}"


def print_(*args, **kwargs):
    indx = 1
    for key, value in kwargs.items():
        print('[' + key + ']')

        for k, v in list(value.items())[:-5]:
            print(format_str.format(k, str(v)))

        N1 = str(sum(list(value.values())[0:-5]))
        print('\n', format_str.format('N1', N1))


        for k, v in list(value.items())[-5:]:
            print(format_str.format(k, str(v)))

        N2 = str(sum(list(value.values())[-5:]))
        print('\n', format_str.format('N2', N2))

