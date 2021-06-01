import os
import sys
import pandas as pd

project_path = os.path.abspath(__file__+'/../..')
if project_path not in sys.path:
    sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from config.sysfiles.parameters import *
from common.utils.logs import StartEndLogging
from common.utils.logs import Logger as log
from common.wrapper import CodeWrapper as ccw
from stock.wrapper import AccountWrapper as saw
from batchs.crawler import KrxCrawler


def code_init():
    se = StartEndLogging('CodeTable Initialization.')

    ccw.delete_all()
    codes = pd.read_csv(CODE_FILE_PATH, sep=',', encoding='utf-8')
    codes = codes.fillna('')
    ccw.save(codes)

    se.end()


def account_init():
    se = StartEndLogging('AccountTable Initialization.')

    accounts = []
    trading_types = ccw.get_codes(c_type='B')
    for trading_type in trading_types:
        for trading_count in TRADING_COUNTS:
            account_dict = {
                'acc_name'      : f'{trading_type}{trading_count}',
                't_type'        : trading_type,
                't_count'       : trading_count,
                'base_money'    : TRADING_BASE_MONEY
            }
            accounts.append(account_dict)
    saw.delete_all()
    saw.save(accounts)

    se.end()


def start_krx_crawling(s_date):
    skc = KrxCrawler(s_date=s_date)
    skc.start_crawler()


if __name__ == '__main__':
    try:
        # code_init()
        # account_init()
        start_krx_crawling(s_date='20210501')
    except Exception as e:
        log.error(e)