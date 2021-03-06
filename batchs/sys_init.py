import os
import sys

project_path = os.path.abspath(__file__+'/../..')
if project_path not in sys.path:
    sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.contrib.auth.hashers import make_password

from common.wrapper import UserWrapper as cuw
from stock.save_tables import *
from stock.wrapper import AccountWrapper as saw
from batchs.crawler import KrxCrawler


def user_init(user_count=100, is_delete=False):

    if is_delete:
        cuw.delete_all()

    user_list = []
    super_user = {
        'username'      : 'freeman',
        'password'      : make_password('1111'),
        'email'         : 'freeman.cho@gmail.com',
        'first_name'    : 'freeman',
        'last_name'     : 'cho',
        'is_staff'      : True,
        'is_active'     : True,
        'is_superuser'  : True,
        'gender'        : 1
    }
    user_list.append(super_user)

    for i in range(user_count):
        user_dict = {
            'username'  : f'freeman{i}',
            'password'  : make_password('1111'),
            'email'     : f'freeman{i}.cho@gmail.com',
            'first_name': f'freeman{i}',
            'last_name' : 'cho',
            'is_staff'  : True if i%6==0 else False,
            'is_active' : True,
            'is_superuser': False,
            'gender'    : 1
        }
        user_list.append(user_dict)

    cuw.save(user_list)


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


def save_tables():
    save_marketdata_from_crawler(is_delete=True)
    save_company_from_marketdata(is_delete=True)
    save_modelingdata_from_marketdata(is_delete=True)


if __name__ == '__main__':
    try:
        user_init(100)
        # code_init()
        # account_init()
        # start_krx_crawling(s_date='all')   # ?????? ?????? ????????? ????????? ???
        # save_tables()
    except Exception as e:
        log.error(e)
    print('program ended.')