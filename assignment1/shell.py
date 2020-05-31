import os
import platform
import subprocess
import sys
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

running_platform = ''


# colors support for posix shells
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
        if len(directory) > 1:
            os.chdir(directory[1])
        else:
            os.chdir(os.path.expanduser('~'))

    def command(cmd):
        executed = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, universal_newlines=True, shell=running_platform!='Linux')
        out = executed.stdout

        def running():
            datetime = dt.now()

            lines_out = 0

            # read output from executed  or running subprocess
            while True:
                try:
                    output = out.readline()
                    print(output, end='')
                    lines_out += 1

                    return_code = executed.poll()
                    if return_code is not None:
                        lines = out.readlines()
                        for output in lines:
                            print(output, end='')
                            lines_out += 1
                        break
                except KeyboardInterrupt:  # interrupt for long-running subprocess (tail, ping, etc...)
                    print()
                    break

            log(str_log(executed, datetime.strftime('%Y-%m-%d %H:%M:%S'), lines_out), OUT_LOG_FILE)

        running()

    if cmd == 'exit()':
        exit()
    elif cmd.startswith('cd'):
        cd()
    else:
        command(cmd)


# log with out path
def log(str, where=sys.stdout):
    if not (where == sys.stdout):
        print(str, file=where, flush=True)
    else:
        print(str)


def str_log(process, timestamp, stdout_count=0):
    cmd = process.args[0]
    args = process.args[1:] if len(process.args) > 1 else []
    pid = process.pid
    exit_code = process.returncode

    log_string = '[{0}] cmd: {1}, args: {2}, stdout: {3}, pid: {4}, exit: {5}'.format(timestamp, cmd, args,
                                                                                      stdout_count, pid, exit_code)
    return log_string


def sys_info():
    global running_platform
    running_platform = platform.system()

    sys_info_str = 'Python shell rub platform: {0}, Version: {1}, Python {2}'

    if running_platform == 'Linux':
        print(sys_info_str.format(running_platform, platform.linux_distribution(), platform.python_version()))
    else:
        print(sys_info_str.format(running_platform, platform.win32_ver(), platform.python_version()))


# shell init configuration
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
        current_outlog_file = OUT_DIRECTORY + '/' + LOG_FILE_NAME + '_' + current_date + '.log'

        global current_errlog_file
        current_errlog_file = ERR_DIRECTORY + '/' + LOG_FILE_NAME + '_' + current_date + '.stderr'

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


# input read method (simple str input)
def read():
    linux_prompt = '{1} ' + Colors.color('L_Shell', Colors.light_green) + Colors.color(' [{0}] # ', Colors.light_blue)
    win_prompt = '{1} W_Shell [{0}] # '
    input_promt = linux_prompt if running_platform == 'Linux' else win_prompt

    while True:
        current_path = path_cutter(os.getcwd())
        try:
            cmd = input(input_promt.format(current_path, dt.now().strftime('%H:%M:%S')))
            process(cmd)
        except EOFError:
            if running_platform == 'Linux':
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
            log(e, ERR_LOG_FILE)

    end()


def start():
    init()


start()
