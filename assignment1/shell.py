import sys
import os
from datetime import datetime as dt

EXIT_MESSAGE = 'Goodbye!'
LOG_FILE_NAME = 'myshell'

LOGS_DIRECTORY = 'logs'
OUT_DIRECTORY = LOGS_DIRECTORY + '/out'
ERR_DIRECTORY = LOGS_DIRECTORY + '/err'

current_outlog_file = ''
current_errlog_file = ''
ERR_LOG_FILE = ''

def path_cutter(path):
    path_split = path.split('/')
    cutted_path = '/' + '/'.join(x[0] if x[0] != '.' else x[0:2] for x in path_split[1:])
    return cutted_path


def process(cmd):
    def exit():
        raise StopIteration

    def cd():
        directory = cmd.split(' ')
        if len(directory) > 1:
            os.chdir(directory[1])
        else:
            os.chdir(os.path.expanduser('~'))

    def command(cmd):
        os.system(cmd)

    if cmd == 'exit()':
        exit()
    elif cmd.startswith('cd'):
        cd()
    else:
        command(cmd)


def log(exception):
    ERR_LOG_FILE.write(str(exception) + "\n")


def sys_info():
    os.system('python3 -V')


def init():
    def create_log_file():
        if not (os.path.exists(LOGS_DIRECTORY)):
            os.makedirs(LOGS_DIRECTORY)

        if not (os.path.exists(OUT_DIRECTORY)):
            os.makedirs(OUT_DIRECTORY)

        if not (os.path.exists(ERR_DIRECTORY)):
            os.makedirs(ERR_DIRECTORY)

        current_date = dt.today().strftime('%d%m%Y')
        current_log_file = OUT_DIRECTORY + '/'+LOG_FILE_NAME + '_' + current_date + '.log'
        global current_errlog_file
        current_errlog_file = ERR_DIRECTORY + '/'+LOG_FILE_NAME + '_' + current_date + '.stderr'
        global ERR_LOG_FILE
        ERR_LOG_FILE = open(current_errlog_file, "a")

    create_log_file()
    # sys_info()
    read()

def read():
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
        except Exception as e:
            log(e)

def main():
    init()
    
main()