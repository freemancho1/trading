import re
from datetime import timedelta
from dateutil.parser import parse
from django.db.models import Max, Min

from config.sysfiles.parameters import *
from common.utils.datautils import DataConverter as dc

class BaseWrapper:

    @staticmethod
    def save(base_table, datas):

        datas_type = re.findall(".*\.(\w+)\.",
                                str(type(datas)).replace("'", "."))[0]
        # datas의 type이 'base_table'값이면 len()함수가 오류가 나기 때문에 1로 지정
        datas_size = 1 if datas_type in str(base_table) else len(datas)

        def make_object(new_data):
            if 'DataFrame' in str(type(new_data)):
                new_data = dc.other_to_dict(new_data)
            new_data['id'] = new_data.get('id', None)
            return base_table(**new_data)

        def save_list(data_list):
            list_size = len(data_list)
            if list_size > MIN_BULK_DATA_SIZE and data_list[0].id is None:
                loop_cnt = int(list_size / BULK_DATA_SIZE) + 1
                for idx in range(loop_cnt):
                    data_pos = idx * BULK_DATA_SIZE
                    if list_size > data_pos + BULK_DATA_SIZE:
                        base_table.objects.bulk_create(data_list[data_pos:data_pos+BULK_DATA_SIZE])
                    else:
                        base_table.objects.bulk_create(data_list[data_pos:])
            else:
                for data in data_list:
                    data.save()

        def make_list(data_list):
            sub_data_type = re.findall(".*\.(\w+)\.", str(type(data_list[0])).replace("'", "."))[0]
            if sub_data_type in str(base_table):
                save_list(data_list)
            elif sub_data_type in ['dict', 'Series']:
                new_objects = []
                for data in data_list:
                    new_objects.append(make_object(data))
                save_list(new_objects)
            else:
                raise Exception(f'{base_table} insert error: data type({datas_type} - {sub_data_type})')

        def save_df(dataframes):
            new_objects = []
            for _, data in dataframes.iterrows():
                new_objects.append(make_object(data))
            save_list(new_objects)

        try:
            if datas_type in str(base_table):
                datas.save()
            elif (datas_type == 'DataFrame' and datas_size == 1) or datas_type in ['dict', 'Series']:
                make_object(datas).save()
            elif datas_type == 'list':
                make_list(datas)
            elif datas_type == 'DataFrame':
                save_df(datas)
            else:
                raise Exception(f'{base_table} insert error: data type({datas_type})')
        except Exception as e:
            raise Exception(str(e))


    @staticmethod
    def get(base_table, **kwargs):
        """
        해당 테이블(base_table)에서 주어진 조건(**kwargs)을 이용해 데이터를 읽는다.
        :param base_table: 데이터를 읽은 테이블(ex, Code, ModelingData..)
        :param kwargs: 읽을 조건
            - 사용 예:
              id=1 or
              c_type='A', code='A001'
            - 읽어올 값이 없거나 하나 이상일 경우 에러가 발생한다.
            - 오직 하나의 데이터만 읽는다.
        :return:
        """
        try:
            data = base_table.objects.get(**kwargs)
        except Exception as e:
            raise Exception(f'{base_table} get error! : {kwargs} - {str(e)}')
        return data


    @staticmethod
    def gets(base_table, *order, **kwargs):
        """
        해당 테이블(base_table)에서 주어진 조건(**kwargs)을 이용해 데이터를 읽는다.
        :param base_table: 데이터를 읽은 테이블(ex, Code, ModelingData..)
        :param order: 추출된 데이터의 정렬 순서
            - 사용 예:
              아무값도 입력하지 않아도 됨 or
              'code' or '-code' or
              '-c_type', 'code'.. (여러 컬럼 지정 가능)
        :param kwargs: 읽을 조건
            - 사용 예:
              아무값도 입력하지 않아도 됨 or
              id=1 or
              c_type='A', code='A001' or
              date__gte=000000, date__lte=999999 ...
            - 단 kwargs가 None(아무 입력도 없으면)이면 해당 테이블의 모든 데이터를 읽어온다.
        :return: 해당 조건에 맞는 데이터(들)
        """
        try:
            if kwargs is None:
                data_qs = base_table.objects.all()
            else:
                data_qs = base_table.objects.filter(**kwargs)
            data_qs = data_qs.order_by(*order)
        except Exception as e:
            raise Exception(f'{base_table} get datas error! : '
                            f'order {order}, kwargs({kwargs}) - {str(e)}')
        return data_qs


    @staticmethod
    def get_date(base_table, date_col='date', is_min=False, is_add_one=True):
        """
        base_table의 date_col의 최대/최소 일자를 구한다.
        :param base_table: 일자를 구하려는 테이블 정보
        :param date_col: 테이블에서 일자를 구하려는 컬럼명(기본값: 'date')
        :param is_min: Treu - 최소일자, False - 최대일자
        :param is_add_one: 최대일자에(만) 참이면 1일을 더한다.
        :return: 최소/최대(또는 +1일) 일자, 단, Table에 값이 없으면 최초 거래일
        """
        try:
            if is_min:
                date = base_table.objects.all().aggregate(min_date=Min(date_col))['min_date']
            else:
                date = base_table.objects.all().aggregate(max_date=Max(date_col))['max_date']
            if date is not None:
                if is_add_one and not is_min:
                    date = date + timedelta(days=1)
            else:
                date = parse(BASE_TRADING_DATE).date()
        except Exception as e:
            raise Exception(f'{base_table} get date error!: column_name={date_col}\n{str(e)}')
        return date


    @staticmethod
    def delete(base_table, **kwargs):
        """
        해당 테이블(base_table)을 주어진 조건(**kwargs)을 이용해 삭제한다.
        :param base_table: 데이터를 삭제할 테이블(ex, Code, ModelingData..)
        :param kwargs: 삭제조건
            - 사용 예:
              아무값도 입력하지 않아도 됨 or
              id=1 or
              c_type='A', code='A001' or
              date__gte=000000, date__lte=999999 ...
            - 단 kwargs가 None(아무 입력도 없으면)이면 해당 테이블의 모든 데이터가 삭제된다.
        :return: 없음
        """
        try:
            if kwargs is None:
                base_table.objects.all().delete()
            else:
                base_table.objects.filter(**kwargs).delete()
        except Exception as e:
            raise Exception(f'{base_table} delete error!: kwargs({kwargs})\n{str(e)}')