import os
import sys

project_path = os.path.abspath(__file__+'/../../..')
if project_path not in sys.path:
    sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.db.models import Sum, Count, Max, Min, Avg, F
from stock.models import MarketData, Company
from common.utils.logs import Logger as log
from common.utils.logs import StartEndLogging

def print_qs(data_qs, p_size=15):
    d_size = len(data_qs)
    log.info(f'Total Record Size: {d_size}')
    p_size = p_size if p_size < d_size else d_size
    for i in range(p_size):
        log.debug(f'{i:<10d} {data_qs[i]}')

# .filter(sum_volume__gt=2000000000) \
def get_group_data():
    group_qs = MarketData.objects\
        .filter(date__gt='2020-12-31')\
        .values('date', 'm_type')\
        .order_by('date', 'm_type')\
        .annotate(sum_volume=Sum('volume'), avg_volume=Avg('volume'))\
        .filter(sum_volume__gt=3000000000)\
        .values('date', 'm_type', 'sum_volume')\
        .order_by('-avg_volume')
    print_qs(group_qs)

def get_group_data1():
    se = StartEndLogging('get_group_data1')
    group_qs = MarketData.objects.values('date').filter(date__gt='2020-12-31')\
        .aggregate(avg_volume=Sum('volume'))
    log.info(f'QuerySet size: {len(group_qs)}')
    log.debug(group_qs)
    se.end()

def get_group_data2():
    se = StartEndLogging('get_group_data2')
    group_qs = \
        MarketData\
            .objects\
            .filter(date__gt='2020-12-31')\
            .values('m_type')\
            .annotate(Avg('volume'))
    log.info(f'QuerySet size: {len(group_qs)}')
    log.debug(group_qs)
    se.end()

def get_data():
    data_qs = MarketData.objects.filter(date__gt='2020-12-31').values('volume') \
        .order_by('date', 'com_code')
    log.info(f'QuerySet size: {len(data_qs)}')
    log.debug(data_qs)

def get_id_count():
    summary = MarketData.objects.aggregate(total_rec=Count('id'))
    log.info(f'summary.total_rec: {summary["total_rec"]}')

def get_id_count1():
    total_rec = MarketData.objects.values('volume').annotate(total_vol=Sum('volume'))
    log.info(f'Total Record Count: {total_rec}')

def get_mtype_count():
    # group_qs = Company.objects.values('m_type').annotate(mtype_size=Count('id'))
    # group_qs = Company.objects.annotate(Count('m_type'))
    group_qs = Company.objects.values('m_type')\
        .order_by('m_type')\
        .annotate(mtype_sum=Sum('t_volume'))
    log.info(f'Total Record Count: {len(group_qs)}')
    idx = 1
    for data in group_qs[:5]:
        log.debug(f'{idx:<10d} {data}')
        idx += 1

if __name__ == '__main__':
    get_group_data()
    # get_group_data1()
    # get_group_data2()
    # get_data()
    # get_id_count()
    # get_id_count1()
    # get_mtype_count()