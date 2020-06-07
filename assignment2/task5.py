import os
import subprocess
import sys
import dis
import marshal
import py_compile

flags = ['-py', '-pyc', '-s']
actions = ['compile', 'print']

current_action = ''
current_flag = ''
process_queue = {}

bytecode_path = os.path.dirname(__file__) + '/dis'

exit_message = 'usage: ' + os.path.basename(__file__) + ' ' + str(flags) + ' args'

def run():
    try:
        parse_args()
        process()
    except SystemExit:
        print(exit_message)

def process():
    for key,values in process_queue.items():
        if current_action == 'compile': cmpl(key, values)
        elif current_action == 'print': disasemble(key, values)


def parse_args():
    if len(sys.argv) < 4:
        raise SystemExit

    if sys.argv[1] not in actions:
        raise SystemExit

    if sys.argv[2] not in flags:
        raise SystemExit

    global current_action
    current_action = sys.argv[1]

    flags_indx = []
    current_index = -1

    for indx,arg in enumerate(sys.argv[2:]):
        if arg.startswith('-'):
            flags_indx.append(indx + 2)
            current_index += 1

            process_queue.update([(arg, [])])

            if(current_index >= 1):
                if ((flags_indx[current_index] - flags_indx[current_index - 1]) < 2):
                    raise SystemExit
        else:
            arg_p = sys.argv[flags_indx[current_index]]
            if arg_p == '-py':
                if not os.path.exists(arg):
                    raise SystemExit

                if not os.path.isfile(arg):
                    raise SystemExit
                
                if not arg.endswith('.py'):
                    raise SystemExit
                
                process_queue[arg_p].append(arg)
            
            elif arg_p == '-pyc':

                if not os.path.exists(arg):
                    raise SystemExit

                if not os.path.isfile(arg):
                    raise SystemExit
                
                if not arg.endswith('.pyc'):
                    raise SystemExit
                
                process_queue[arg_p].append(arg)

            else:

                if os.path.exists(arg):
                    raise SystemExit

                process_queue[arg_p].append(arg)
    
    if current_action == 'compile' and '-pyc' in process_queue.keys():
        raise SystemExit
    
    

def check_directory():
    if not os.path.exists(bytecode_path):
        os.mkdir(bytecode_path)

def cmpl(flag, args):
    if flag == '-py': compile_py(args)
    if flag == '-s': compile_s(args)
    return

def compile_py(current_args):
    for arg in current_args:
        py_compile.compile(arg, cfile= compile_file_name(arg))

def compile_s(current_args):
        for arg in current_args:
            obj = compile(arg,'_',mode='exec')
            marshal.dump(obj, open(compile_file_name(), 'ab+'))


def disasemble(flag, current_args):
    check_directory()

    if flag == '-py': dis_py(current_args)
    elif flag == '-pyc': dis_pyc(current_args)
    elif flag == '-s': dis_s(current_args)


def dis_py(current_args):
    for arg in current_args:
        with open(arg) as src:
            source = src.read()
        
        file_name = dis_file_name(arg)

        with open(file_name, 'w') as file:
            dis.dis(source, file = file)
        
        print_dis(file_name, arg)

def dis_pyc(current_args):
    header_sizes = [
        (12, (3, 6)), # python version 3.6 - 12 bytes header
        (16, (3, 7)), # python version 3.8 - 16 bytes header
    ]
    header_size = next(s for s, v in reversed(header_sizes) if sys.version_info >= v)

    for arg in current_args:
        with open(arg, 'rb') as src:
            if os.path.basename(arg) != 'out.pyc':
                src.seek(header_size)
            source = marshal.load(src)
        
        file_name = dis_file_name(arg)

        with open(file_name, 'w') as file:
            dis.dis(source, file = file)
            
        print_dis(file_name, arg)

def dis_s(current_args):
    for arg in current_args:
        arrow = " ------> "
        h_line = '=' * len(arg) + '=' * len(arrow) + "=" * len("dis") + '\n'
        print('', h_line, arg + arrow + 'dis\n' , h_line, end='')
        dis.dis(arg)
        print('',h_line)

def compile_file_name(arg = 'out'):
    path = os.path.dirname(__file__) + '/__pycache__' + '/'
    if arg != 'out':
        path = path + os.path.basename(arg[:arg.rindex('.')] + '.pyc')
    else:
        path = path + 'out.pyc'
    
    return path

def dis_file_name(arg):
    return bytecode_path + '/' + os.path.basename(arg[:arg.rindex('.')] + '.dis')

def print_dis(file_name, src):
    arrow = " ------> "
    h_line = '=' * len(src) + '=' * len(arrow) + "=" * len(os.path.basename(file_name)) + '\n'
    
    with open(file_name, 'r') as file:
        print('',h_line, src + arrow + os.path.basename(file_name) + "\n", h_line, *(x for x in file.readlines()), h_line)


def print_comparsion_table(comparsion_results):
    opcode_entries = dict()

    for file in comparsion_results:
        opcodes = comparsion_results[file]
        for opcode in opcodes:
            opcode_entries[opcode] = opcodes[opcode]

    opcode_entries = sorted(opcode_entries.keys(), key=lambda key: opcode_entries[key])

    h_line = "=" * 16 * (len(comparsion_results) + 1)
    head_format = "{0:<15}" + "|{2:>15}" * len(comparsion_results) + "|"
    row_format = "{0:>15}" + "|{2:>15}" * len(comparsion_results) + "|"
    column_names = ['INSTRUCTION']
    column_names.extend(comparsion_results.keys())

    print(row_format)

    print(h_line,
          head_format.format(*column_names),
          h_line,
          *[
              row_format.format(*(
                      [k] + list([comparsion_results[f][k] for f in comparsion_results])))
              for k in opcode_entries],
          h_line, sep='\n')

def main():
    run()

if __name__ == "__main__":
    main()