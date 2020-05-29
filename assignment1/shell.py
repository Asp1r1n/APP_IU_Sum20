import sys
import os

EXIT_MESSAGE = 'Goodbye!'

def path_cutter(path):
    path_split = path.split('/')
    cutted_path = '/' + '/'.join(x[0] if x[0] != '.' else x[0:2] for x in path_split[1:])
    return cutted_path

def process(cmd):
    def exit():
        raise StopIteration

    def cd():
        directory = cmd.split(' ')
        if (len(directory) > 1): os.chdir(directory[1])
        else: os.chdir(os.path.expanduser('~'))

    def command(cmd):
        os.system(cmd)


    if (cmd == 'exit()'): exit()
    elif (cmd.startswith('cd')): cd()
    else: command(cmd)

def log():
    #TODO
    return


while True:
    current_path = '[' + path_cutter(os.getcwd()) + ']'
    try:
        cmd = input('L_Shell {0}: '.format(current_path))
        process(cmd)
    except EOFError:
        print("^D")
        print(EXIT_MESSAGE)
        break
    except StopIteration:
        print(EXIT_MESSAGE)
        break