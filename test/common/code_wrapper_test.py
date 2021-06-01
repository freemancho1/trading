import os
import sys
import pandas as pd

project_path = os.path.abspath(__file__+'/../../..')
if project_path not in sys.path:
    sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from config.sysfiles.parameters import *
from common.utils.logs import Logger as log
from common.utils.logs import StartEndLogging
from common.wrapper import CodeWrapper as cw


def code_init():
    se = StartEndLogging()
    cw.delete_all()
    code_df = pd.read_csv(CODE_FILE_PATH, sep=',', encoding='utf-8')
    code_df = code_df.fillna('')
    cw.save(code_df)
    se.end()

def code_save():
    code_dt = {
        'c_type': 'B',
        'code': 'B003',
        'name': 'Next Close vs Next Open',
        'memo': 'Next day predict close price vs next day predict open price'
    }
    cw.save(code_dt)

def get_code():
    log.info('get code: A006 = error!')
    log.debug(cw.get_by_code('A006'))

def code_list():
    log.info('== get code to name dict : c_type = 0')
    for code in cw.get_code_to_name_dict():
        log.debug(code)

    log.info('== get name to code dict : c_type = A')
    for code in cw.get_name_to_code_dict(c_type='A'):
        log.debug(code)

    log.info('== get all')
    for code in cw.get_all():
        log.debug(code)


if __name__ == '__main__':
    try:
        # code_init()
        code_save()
        # get_code()
        # code_list()
    except Exception as e:
        log.error(e)
    print('program ended!.')