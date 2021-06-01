import re
import shutil
import traceback

from config.sysfiles.parameters import *


class Logger:

    @staticmethod
    def __log_writer(label, msg, is_trace=True):
        if IS_WRITE(label):
            if is_trace:
                get_trace = re.findall('.*/([\w_\-\.]+).* (.*)', traceback.format_stack()[-3])
                try:
                    trace_msg = f'{get_trace[0][0]}:{get_trace[0][1]} - '
                except:
                    trace_msg = ''
            else:
                trace_msg = ''
            Logger.__file_checker()
            with open(LOG_FILE_PATH, 'a') as logfile:
                logfile.write(f'{datetime.now():%Y-%m-%d %H:%M:%S} '
                              f'[{label.upper():>8}] {trace_msg}{msg}\n')

    @staticmethod
    def __file_checker():
        if not os.path.exists(LOG_PATH):
            os.makedirs(LOG_PATH, exist_ok=True)
        try:
            f_size = os.path.getsize(LOG_FILE_PATH)
            try:
                max_size = ByteSize[LOG_FILE_SIZE[-1:]].value * int(LOG_FILE_SIZE[:-1])
            except:
                max_size = DEFAULT_LOG_FILE_SIZE
            if f_size > max_size:
                Logger.__logfile_move()
        except:
            Logger.__logfile_create()

    @staticmethod
    def __logfile_create():
        logfile = open(LOG_FILE_PATH, 'w')
        logfile.close()

    @staticmethod
    def __logfile_move():
        log_file_cnt = 0
        max_log_file_cnt = min(LOG_FILE_COUNT_MAX, LOG_FILE_COUNT)
        min_ctime, max_ctime = float('inf'), float('inf')
        min_file_name, max_file_name = '', ''
        for file_name in os.listdir(LOG_PATH):
            if re.findall(LOG_FILE_NAME_PREFIX + '\-\d{5}\.log', file_name):
                log_file_cnt += 1
                curr_ctime = os.path.getctime(os.path.join(LOG_PATH, file_name))
                if min_ctime > curr_ctime:
                    min_ctime, min_file_name = curr_ctime, file_name
                if max_ctime < curr_ctime:
                    max_ctime, max_file_name = curr_ctime, file_name

        if log_file_cnt >= max_log_file_cnt:
            os.remove(os.path.join(LOG_PATH, min_file_name))
        if log_file_cnt == 0:
            new_file_number = 0
        else:
            new_file_number = int(re.findall('\d{5}', max_file_name)[0])
            if new_file_number > LOG_FILE_COUNT_MAX:
                new_file_number = 0
            else:
                new_file_number += 1
        new_log_file_name = f'{LOG_FILE_NAME_PREFIX}-{new_file_number:05d}.log'
        shutil.move(LOG_FILE_PATH, os.path.join(LOG_PATH, new_log_file_name))

        Logger.__logfile_create()

    @staticmethod
    def debug(msg, is_trace=True):
        Logger.__log_writer('debug', msg, is_trace=is_trace)

    @staticmethod
    def info(msg, is_trace=True):
        Logger.__log_writer('info', msg, is_trace=is_trace)

    @staticmethod
    def warning(msg, is_trace=True):
        Logger.__log_writer('warning', msg, is_trace=is_trace)

    @staticmethod
    def error(msg, is_trace=True):
        Logger.__log_writer('error', msg, is_trace=is_trace)

    @staticmethod
    def critical(msg, is_trace=True):
        Logger.__log_writer('critical', msg, is_trace=is_trace)


class StartEndLogging(object):

    def __init__(self, msg=None):
        self.start = datetime.now()
        self.init_msg = '' if msg is None else msg + ' '
        try:
            self.call_func = re.findall('.*/([\w_\-\.]+).* (.*)', traceback.format_stack()[-3])
            self.func_msg = f'{self.call_func[0][0]} {self.call_func[0][1]} ' \
                            f'{self.init_msg}'
        except:
            self.func_msg = f' {self.init_msg}'
        Logger.info(f'{self.func_msg} started - {self.start}', is_trace=False)

    def mid(self, msg=None):
        curr_datetime = datetime.now()
        curr_msg = '' if msg is None else msg + ' '
        Logger.debug(f'{self.func_msg} {curr_msg} processing - {curr_datetime}, '
                     f'so far processing time: {curr_datetime - self.start}', is_trace=False)

    def end(self, msg=None):
        curr_datetime = datetime.now()
        curr_msg = '' if msg is None else msg + ' '
        Logger.info(f'{self.func_msg} {curr_msg} ended - {curr_datetime}, '
                    f'total processing time: {curr_datetime - self.start}', is_trace=False)