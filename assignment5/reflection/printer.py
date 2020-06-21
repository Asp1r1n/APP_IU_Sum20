
format_str = "{:>10}:   {}"
sub_str = "{:>10}    {}"

def print_reflection(*args, **kwargs):

    for key,value in kwargs.items():

        if type(value) is str:
            value = value.splitlines()    
        
        for indx, val in enumerate(value):
            if indx == 0: print(format_str.format(key, val))
            else: print(sub_str.format('',val))

        print()
