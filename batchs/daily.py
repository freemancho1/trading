import os
import sys

project_path = os.path.abspath(__file__+'/../..')
if project_path not in sys.path:
    sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from common.utils.logs import Logger as log
from modeling.nn_models import lstm
from batchs.crawler import KrxCrawler
from stock.save_tables import *
from stock.wrapper import ModelInfoWrapper as smiw
from stock.wrapper import ModelingInfoWrapper as smliw


def start_krx_crawling():
    skc = KrxCrawler()
    skc.start_crawler()


def update_tables():
    save_marketdata_from_crawler(is_delete=False)
    save_modelingdata_from_marketdata(is_delete=False)


def daily_predict():

    se = StartEndLogging('Daily Prediction.')

    select_models = smiw.get_predict_models()
    # log.debug(f'select model count: {len(select_models)}')
    for model_info in select_models:
        model = lstm(model_info.info)
        model.load_weights(model_info.model_path)


    se.end()


if __name__ == '__main__':
    try:
        # start_krx_crawling()
        # update_tables()
        daily_predict()
    except Exception as e:
        log.error(e)