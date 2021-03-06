import os
import subprocess
import sys
import dis
import marshal

actions = ['-py', '-pyc', '-s']

current_action = ''
current_args = []

bytecode_path = os.path.dirname(__file__) + '/dis'

help_str = '''usage: ''' + os.path.basename(__file__) + ''' -flag [value]+

    -py  [filename.py]+  produce human-readable bytecode from python file 
    -pyc [filename.pyc]+ produce human-readable bytecode from compiled .pyc file 
    -s   ["src"]+        produce human-readable bytecode from normal string 

    example: program -py test1.py test2.py  '''

def run():
    try:
        check_args()
        disasemble(current_action)
    except SystemExit:
        print(help_str)

def check_args():
    if len(sys.argv) < 3:
        raise SystemExit

    if sys.argv[1] not in actions:
        raise SystemExit

    global current_action
    current_action = sys.argv[1]

    global current_args
    current_args = sys.argv[2:]

    if current_action == '-py' or current_action == '-pyc':
        for arg in current_args:
            if not os.path.exists(arg):
                raise SystemExit
    

def check_directory():
    if not os.path.exists(bytecode_path):
        os.mkdir(bytecode_path)

def disasemble(act):
    check_directory()

    if act == '-py': dis_py()
    elif act == '-pyc': dis_pyc()
    elif act == '-s': dis_s()


def dis_py():
    for arg in current_args:
        with open(arg) as src:
            source = src.read()
        
        file_name = dis_file_name(arg)

        with open(file_name, 'w') as file:
            dis.dis(source, file = file)
        
        print_dis(file_name, arg)

def dis_pyc():
    header_sizes = [
        (12, (3, 6)), # python version 3.6 - 12 bytes header
        (16, (3, 7)), # python version 3.8 - 16 bytes header
    ]
    header_size = next(s for s, v in reversed(header_sizes) if sys.version_info >= v)

    for arg in current_args:
        with open(arg, 'rb') as src:
            src.seek(header_size)
            source = marshal.load(src)
    
        file_name = dis_file_name(arg)

        with open(file_name, 'w') as file:
            dis.dis(source, file = file)
        
        print_dis(file_name, arg)

def dis_s():
    for arg in current_args:
        arrow = " ------> "
        h_line = '=' * len(arg) + '=' * len(arrow) + "=" * len("dis") + '\n'
        print('', h_line, arg + arrow + 'dis\n' , h_line, end='')
        dis.dis(arg)
        print('',h_line)

def dis_file_name(arg):
    return bytecode_path + '/' + os.path.basename(arg[:arg.rindex('.')] + '.dis')

def print_dis(file_name, src):
    arrow = " ------> "
    h_line = '=' * len(src) + '=' * len(arrow) + "=" * len(os.path.basename(file_name)) + '\n'
    
    with open(file_name, 'r') as file:
        print('',h_line, src + arrow + os.path.basename(file_name) + "\n", h_line, *(x for x in file.readlines()), h_line)
    
def main():
    run()

if __name__ == "__main__":
    main()