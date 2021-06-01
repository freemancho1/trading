from stock.models import *
from config.sysfiles.parameters import *
from common.utils.datautils import DataConverter as dc
from common.utils.base_wrapper import BaseWrapper as bw

class CompanyWrapper:

    @staticmethod
    def make_object(data, update_data=None):
        company_dict = {}
        try:
            source = dc.other_to_dict(data)
            company_dict['com_code'] = source['com_code']
            company_dict['data_size'] = source.get('data_size', 0)
            if update_data is None:
                company_dict['id'] = None
            else:
                company_dict['id'] = source['id']
                source = dc.other_to_dict(update_data)
            company_dict['com_name'] = source['com_name']
            company_dict['m_type'] = source['m_type']
            company_dict['t_volume'] = source['t_volume']
            new_object = Company(**company_dict)
        except Exception as e:
            raise Exception(f'Company table make object error: '
                            f'soc_data={data}, upd_data={update_data}, save_data={company_dict}')
        return new_object

    @staticmethod
    def get_all():
        return bw.gets(Company)

    @staticmethod
    def get_company(com_code):
        return bw.get(Company, com_code=com_code)

    @staticmethod
    def get_modeling_target():
        return bw.gets(Company, 'com_code', data_size__gt=MODELING_SKIP_DATA_SIZE)

    @staticmethod
    def save(datas):
        bw.save(Company, datas)

    @staticmethod
    def delete_all():
        bw.delete(Company)


class MarketDataWrapper:

    @staticmethod
    def get_all():
        return bw.gets(MarketData)

    @staticmethod
    def get_last_date():
        return bw.get_date(MarketData, is_add_one=False)

    @staticmethod
    def get_last_date_add_one():
        return bw.get_date(MarketData)

    @staticmethod
    def get_min_date():
        return bw.get_date(MarketData, is_min=True, is_add_one=False)

    @staticmethod
    def save(datas):
        bw.save(MarketData, datas)

    @staticmethod
    def delete_all():
        bw.delete(MarketData)


class ModelingDataWrapper:

    @staticmethod
    def get_all():
        return bw.gets(ModelingData)

    @staticmethod
    def get_last_date():
        return bw.get_date(ModelingData, is_add_one=False)

    @staticmethod
    def get_last_date_add_one():
        return bw.get_date(ModelingData)

    @staticmethod
    def get_min_date():
        return bw.get_date(ModelingData, is_min=True, is_add_one=False)

    @staticmethod
    def save(datas):
        bw.save(ModelingData, datas)

    @staticmethod
    def delete_all():
        bw.delete(ModelingData)


class ModelInfoWrapper:

    @staticmethod
    def get_all():
        return bw.gets(ModelInfo)

    @staticmethod
    def save(datas):
        bw.save(ModelInfo, datas)

    @staticmethod
    def delete_all():
        bw.delete(ModelInfo)


class AccountWrapper:

    @staticmethod
    def get_all():
        return bw.gets(Account)

    @staticmethod
    def save(datas):
        bw.save(Account, datas)

    @staticmethod
    def delete_all():
        bw.delete(Account)