import os
import sys

project_path = os.path.abspath(__file__+'/../..')
if project_path not in sys.path:
    sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django_pandas.io import read_frame

from config.sysfiles.parameters import *
from common.utils.logs import Logger as log
from common.utils.logs import StartEndLogging
from modeling.utils import ModelingUtils as mu
from stock.wrapper import ModelInfoWrapper as smiw
from stock.wrapper import ModelingDataWrapper as smdw


def save_max_volume():

    se = StartEndLogging('Save Max Volume.')

    invalid_cnt = 0
    last_models = smiw.get_all_last_models()
    for model in last_models:
        modeling_data = read_frame(smdw.get_modeling_datas(model.com_code))
        max_price = mu.get_max_value(modeling_data[PRICE_COLUMNS])
        max_volume = mu.get_max_value(modeling_data['volume'])
        if max_price != model.max_price:
            invalid_cnt += 1
            log.info(f'new max_price: {max_price}, old max_price: {model.max_price}')
        else:
            model.max_volume = max_volume
            smiw.save(model)

    se.end(f'invalid count: {invalid_cnt}')


if __name__ == '__main__':
    try:
        save_max_volume()
    except Exception as e:
        log.error(e)