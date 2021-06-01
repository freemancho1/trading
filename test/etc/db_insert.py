import os
import sys
import pandas as pd

project_path = os.path.abspath(__file__+'/../../..')
if project_path not in sys.path:
    sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from common.models import Code
from config.sysfiles.parameters import *
from common.utils.logs import Logger as log
from common.wrapper import CodeWrapper as cw


def code_save():
    code_dict = {
        'id': None,
        'c_type': 'B',
        'code': 'B003',
        'name': 'Next Close vs Next Open',
        'memo': 'Next day predict close price vs next day predict open price'
    }

    code_obj = Code(**code_dict)
    # code_obj.save()
    # new_code = code_obj             # new_code에 값(id)이 전달됨
    new_code = code_obj.save()        # new_code에 값이 전달되지 않음(None)
    log.debug(f'new code: {new_code}')


if __name__ == '__main__':
    try:
        code_save()
    except Exception as e:
        log.error(e)
    print('db_insert test end.')