import sys
import os
import platform
import subprocess
from datetime import datetime as dt

EXIT_MESSAGE = 'Goodbye!'
LOG_FILE_NAME = 'myshell'

LOGS_DIRECTORY = 'logs'
OUT_DIRECTORY = LOGS_DIRECTORY + '/out'
ERR_DIRECTORY = LOGS_DIRECTORY + '/err'

current_outlog_file = ''
current_errlog_file = ''
ERR_LOG_FILE = ''
OUT_LOG_FILE = ''


class Colors:
    light_green = '\033[92m'
    light_blue = '\033[94m'
    remove = '\033[0m'
    bold = '\033[1m'

    @staticmethod
    def color(str, color):
        return color + Colors.bold + str + Colors.remove

def path_cutter(path):
    path_split = path.split('/')
    cutted_path = '/' + '/'.join(x[0] if x[0] != '.' else x[0:2] for x in path_split[1:])
    return cutted_path


def process(cmd):
    def exit():
        raise StopIteration

    def cd():
        directory = cmd.split(' ')
        if (len(directory) > 1):
            os.chdir(directory[1])
        else:
            os.chdir(os.path.expanduser('~'))

    def command(cmd):
        executed = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, universal_newlines = True)
        out = executed.stdout

        def running():
            datetime = dt.now()

            lines_out = 0
            while True:
                try:
                    output = out.readline()
                    print(output, end='')
                    lines_out += 1
                    
                    return_code = executed.poll()
                    if (return_code is not None): 
                        lines = out.readlines()
                        for output in lines:
                            print(output, end='')
                            lines_out += 1
                        break
                except KeyboardInterrupt:
                    print()
                    break

            log(str_log(executed, datetime.strftime('%Y-%m-%d %H:%M:%S'), lines_out), OUT_LOG_FILE)
            
        running()


    if (cmd == 'exit()'): exit()
    elif (cmd.startswith('cd')): cd()
    else: command(cmd)

def log(str, where = sys.stdout):
    if not (where  == sys.stdout): print(str, file = where, flush = True)
    else: print(str)

def str_log(process, timestamp, stdout_count = 0):
    cmd = process.args[0]
    args = process.args[1:] if len(process.args) > 1 else []
    pid = process.pid
    exit_code = process.returncode

    log_string = '[{0}] cmd: {1}, args: {2}, stdout: {3}, pid: {4}, exit: {5}'.format(timestamp, cmd, args, stdout_count, pid, exit_code )
    return log_string

def sys_info():
    print('Python shell run platform: ' + platform.system() + ', Version: ' + str(platform.linux_distribution()) + ', Python ' + platform.python_version())


def init():
    def create_log_file():
        if not (os.path.exists(LOGS_DIRECTORY)):
            os.makedirs(LOGS_DIRECTORY)

        if not (os.path.exists(OUT_DIRECTORY)):
            os.makedirs(OUT_DIRECTORY)

        if not (os.path.exists(ERR_DIRECTORY)):
            os.makedirs(ERR_DIRECTORY)

        current_date = dt.today().strftime('%d%m%Y')

        global current_outlog_file
        current_outlog_file = OUT_DIRECTORY + '/' +LOG_FILE_NAME + '_' + current_date + '.log'

        global current_errlog_file
        current_errlog_file = ERR_DIRECTORY + '/' +LOG_FILE_NAME + '_' + current_date + '.stderr'
        
        global ERR_LOG_FILE
        ERR_LOG_FILE = open(current_errlog_file, "a")

        global OUT_LOG_FILE
        OUT_LOG_FILE = open(current_outlog_file, "a")
    
    create_log_file()
    sys_info()
    read()

def end():
    if not ERR_LOG_FILE.closed: ERR_LOG_FILE.close()
    if not OUT_LOG_FILE.closed: OUT_LOG_FILE.close()

# TODO - terminal like input (terminal keymanipulations in subshell)
def readch():
    import tty, sys, termios

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def read():
    input_promt = Colors.color('L_Shell', Colors.light_green) + Colors.color(' [{0}]: ', Colors.light_blue)

    while True:
        current_path =  path_cutter(os.getcwd())
        try:
            cmd = input(input_promt.format(current_path))
            process(cmd)
        except EOFError:
            print("^D")
            print(EXIT_MESSAGE)
            break
        except KeyboardInterrupt:
            print()
            print(EXIT_MESSAGE)
            break
        except StopIteration:
            print(EXIT_MESSAGE)
            break
        except Exception as e:
            log(e)
        finally:
            end()


def start():
    init()    

start()