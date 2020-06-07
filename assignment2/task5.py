import os
import subprocess
import sys
import dis
import marshal
import py_compile
import re

flags = ['-py', '-pyc', '-s']
actions = ['compile', 'print', 'compare']

current_action = ''
current_flag = ''
process_queue = {}
dic = {}

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
        elif current_action == 'print': disasemble(key, values, True)
        elif current_action == 'compare': cmpr(key, values)

    if current_action == 'compare':
        normalize(dic)
        print_comparsion_table(dic)


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

def cmpr(flag, args):
    build_compare_dict(flag, args)

def normalize(dic_n):
    u_set = set()
    for value in dic_n.values():
        u_set.update(list(value.keys()))

    for value in dic_n.values():
        for set_v in u_set:
            if set_v not in value.keys():
                value.update([(set_v, 0)])

def build_compare_dict(flag, args):
    if flag != '-s': disasemble(flag, args)
    else: 
        cmpl(flag, args)
        disasemble(flag, 'out.pyc')


    for arg in args:
        file_name = dis_file_name(arg)
        parse_dis_file(file_name, arg)

    
def parse_dis_file(file_name, source_file):

    source_file = os.path.basename(source_file)

    global dic 
    if source_file not in dic.keys(): 
        dic.update([(source_file, dict())])
    else: 
        return
            
    with open(file_name, "r") as file:
        for line in file.readlines():
            line = line.strip()

            if line == '': continue

            
            opcode = re.findall('[A-Z]+_[A-Z]+', line) [0]  
            source_dic = dic[source_file]

            if opcode not in source_dic.keys():
                source_dic.update([(opcode, 1)])
            else:
                source_dic.update([(opcode, source_dic[opcode] + 1)])        

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


def disasemble(flag, current_args, print = False):
    check_directory()

    if flag == '-py': dis_py(current_args, print)
    elif flag == '-pyc': dis_pyc(current_args, print)
    elif flag == '-s': dis_s(current_args)


def dis_py(current_args, print):
    for arg in current_args:
        with open(arg) as src:
            source = src.read()
        
        file_name = dis_file_name(arg)

        with open(file_name, 'w') as file:
            dis.dis(source, file = file)
        
        if print: print_dis(file_name, arg)

def dis_pyc(current_args, print):
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
            
        if print: print_dis(file_name, arg)

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
            opcode_entries[opcode] = max(opcode_entries.get(opcode,0),opcodes[opcode])

    opcode_entries = sorted(opcode_entries.keys(), key=lambda key: opcode_entries[key], reverse = True)

    h_line = "=" * 16 * (len(comparsion_results) + 1)
    head_format = "{:<15}" + "|{:>15}" * len(comparsion_results) + "|"
    row_format = "{:>15}" + "|{:>15}" * len(comparsion_results) + "|"
    column_names = ['INSTRUCTION']
    column_names.extend(comparsion_results.keys())

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