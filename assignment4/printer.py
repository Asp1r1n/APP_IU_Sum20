
format_str = "{:>10}:   {}"
sub_str = "{:>10}    {}"

def print_(*args, **kwargs):

    indx = 1
    for key,value in kwargs.items():
        print('[' + key + ']')

        for k,v in value.items():
            print(format_str.format(k,str(v)))


        print('\n',format_str.format('N' + str(indx),str(sum(value.values()))))
        indx += 1
