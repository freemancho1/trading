import os
import sys
# Tensorflow CPU 강제사용 - 이 데이터는 CPU가 조금 더 빨랐음
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = ""

project_path = os.path.abspath(__file__+'/../..')
if project_path not in sys.path:
    sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from batchs.crawler import KrxCrawler
from modeling.nn_training import LstmTraining
from stock.save_tables import *
from common.utils.logs import Logger as log


def start_krx_crawling():
    skc = KrxCrawler()
    skc.start_crawler()


def update_tables():
    # save_marketdata_from_crawler(is_delete=False)
    save_company_from_marketdata(is_delete=True)
    save_modelingdata_from_marketdata(is_delete=True)


def weekly_modeling():

    se = StartEndLogging('start modeling')

    modeling_target_qs = scw.get_modeling_target()
    proc_cnt, skip_trend_cnt, skip_accuracy_cnt = 0, 0, 0

    log.info(f'modeling count: {len(modeling_target_qs)}')

    for modeling_company in modeling_target_qs:
        model = LstmTraining(modeling_company.com_code, LSTM_KWARGS)
        is_skip = model.modeling()
        proc_cnt += 1
        skip_trend_cnt += 1 if is_skip['trend'] else 0
        skip_accuracy_cnt += 1 if is_skip['accuracy'] else 0
        se.mid(f'{modeling_company.com_code} {proc_cnt} / {skip_trend_cnt} / {skip_accuracy_cnt} '
               f'{"SKIP" if is_skip["trend"] or is_skip["accuracy"] else "    "}')

    log.info(f'modeling total count: {proc_cnt}, '
             f'trend skip: {skip_trend_cnt}, accuracy skip: {skip_accuracy_cnt}')

    se.end()


if __name__ == '__main__':
    update_tables()
    weekly_modeling()