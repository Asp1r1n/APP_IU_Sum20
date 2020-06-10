import os
import subprocess
import sys
import dis

actions = ['-py']

current_action = ''
current_args = []

bytecode_path = os.path.dirname(__file__) + '/dis'

help_str = '''usage: ''' + os.path.basename(__file__) + ''' -flag [value]+

    -py  [filename.py]+  produce human-readable bytecode from python file 

    example: program -py test1.py test2.py  '''

def run():
    try:
        check_args()
        disasemble()
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

    if current_action == '-py':
        for arg in current_args:
            if not os.path.exists(arg):
                raise SystemExit
    

def check_directory():
    if not os.path.exists(bytecode_path):
        os.mkdir(bytecode_path)

def disasemble():
    check_directory()

    for arg in current_args:
        with open(arg) as src:
            source = src.read()
        
        file_name = bytecode_path + '/' + os.path.basename(arg.replace('.py', '.dis'))

        with open(file_name, 'w') as file:
            dis.dis(source, file = file)
        
        with open(file_name, 'r') as file:
            h_line = '=' * len(arg) + '=' * 9 + "=" * len(os.path.basename(file_name)) + '\n'
            print('',h_line, arg + " ------> " + os.path.basename(file_name) + "\n", h_line, *(x for x in file.readlines()), h_line)

def main():
    run()

if __name__ == "__main__":
    main()
    