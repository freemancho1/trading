import re
import shutil
import pandas as pd
from django_pandas.io import read_frame
from tqdm import tqdm
from dateutil.parser import parse

from config.sysfiles.parameters import *
from common.utils.logs import StartEndLogging
from common.utils.logs import Logger as log
from common.wrapper import CodeWrapper as ccw
from stock.wrapper import CompanyWrapper as scw
from stock.wrapper import ModelingDataWrapper as smldw
from stock.wrapper import MarketDataWrapper as smdw


def save_marketdata_from_crawler(is_delete=False):

    market_type_dict = ccw.get_name_to_code_dict(c_type='A')

    def file_processing(csv_file_name):
        trading_df = pd.read_csv(os.path.join(CRAWLING_TARGET_PATH, csv_file_name),
                                 sep=',', encoding='CP949', names=COLUMN_NAMES,
                                 skiprows=[0])
        trading_df = trading_df.fillna(0)
        trading_df['date'] = parse(str(re.findall('\d{8}', csv_file_name)[0])).date()
        trading_df['m_type'] = trading_df['m_type'].apply(lambda m_type: market_type_dict[str(m_type)])
        trading_df = trading_df.drop(['m_dept'], axis=1)

        smdw.save(trading_df)

        shutil.move(os.path.join(CRAWLING_TARGET_PATH, csv_file_name),
                    os.path.join(CRAWLING_BACKUP_PATH, csv_file_name))

    se = StartEndLogging('save marketdata from crawler')

    if is_delete:
        log.debug('marketdata delete all start!.')
        smdw.delete_all()
        log.debug('marketdata delete all end!.')

    for file_name in tqdm(sorted(os.listdir(CRAWLING_TARGET_PATH))):
        file_processing(file_name)
        se.mid(file_name)

    se.end()


def save_company_from_marketdata(is_delete=True):

    se = StartEndLogging('save company from market data')

    if is_delete:
        log.debug('company delete all start!.')
        scw.delete_all()
        log.debug('company delete all end!.')

    market_qs = smdw.get_last_date_data()
    log.debug(f'select date: {smdw.get_last_date()}, market_qs size: {len(market_qs)}')

    company_objects = []
    for market_data in market_qs:
        company_objects.append(scw.make_object(market_data))
    scw.save(company_objects)

    se.end()


def save_modelingdata_from_marketdata(is_delete=True):

    se = StartEndLogging('save modeling data from market data')

    if is_delete:
        log.debug('marketdata delete all start!.')
        smldw.delete_all()
        log.debug('marketdata delete all end!.')

    company_qs = scw.get_all()
    market_qs = smdw.get_all()

    def get_normal_marketdata(com_code):
        market_company_qs = market_qs.filter(com_code=com_code)
        first_data = market_company_qs.first()
        yesterday_data, first_normal_data = first_data, first_data

        if first_data.t_volume != 0:
            diff_ratio = market_company_qs.last().t_volume / first_data.t_volume
        else:
            # 첫번째 t_volume값이 0이기 때문에 전체 변동량 체크가 불가능함.
            # 따라서 세부 체크가 수행될 수 있도록 diff_ratio를 설정함
            diff_ratio = TOTAL_CHECK_MAX_RATIO + 1.

        if diff_ratio > TOTAL_CHECK_MAX_RATIO or diff_ratio < TOTAL_CHECK_MIN_RATIO:
            for market_data in market_company_qs[1:]:
                if yesterday_data.t_volume != 0 and market_data.t_volume != 0:
                    diff_ratio = market_data.t_volume / yesterday_data.t_volume
                    if diff_ratio > DAY_CHECK_MAX_RATIO or diff_ratio < DAY_CHECK_MIN_RATIO:
                        first_normal_data = market_data
                    if market_data.volume == 0:
                        first_normal_data = market_data
                yesterday_data = market_data

        normal_qs = market_company_qs.filter(date__gte=first_normal_data.date)
        log.debug(f'com_code: {com_code}, '
                  f'modeling data size: total={len(market_company_qs)}, normal={len(normal_qs)}')
        return normal_qs

    for company in tqdm(company_qs):
        market_df = read_frame(get_normal_marketdata(company.com_code))
        company.data_size = len(market_df)
        company.save()
        market_df = market_df[['date', 'com_code'] + MODELING_COLUMNS]
        smldw.save(market_df)

    se.end()
    
    
def append_modelingdata_from_marketdata():
    """
    save_modelingdata_from_marketdata()는,
        갑자기 변경된 데이터를 걸러내고, 각 회사의 데이터 크기를 저장하지만,
    이 함수는 save_..() 함수가 실행된 다음에 수행되는 함수로,
    이후 데이터를 추가하기만 하고, 각 회사의 데이터 크기를 추가하지 않음
    :return: 없음 
    """
    last_date = smldw.get_last_date()
    log.info(f'ModelingData Last Date: {last_date}')
    append_market_df = read_frame(smdw.get_daily_datas(last_date))
    log.info(f'Append Market Data Size: {len(append_market_df)}')
    append_market_df = append_market_df[['date', 'com_code']+MODELING_COLUMNS]
    smldw.save(append_market_df)