from common.models import *
from common.utils.base_wrapper import BaseWrapper as bw
from config.sysfiles.parameters import *

class CodeWrapper:

    @staticmethod
    def _get_type_dict(c_type, is_name_index=False):
        """
        코드 타입별로 리스트를 구함
        :param c_type: 추출할 코드 타입(기본값은 시스템 코드)
        :param is_name_index:
          - True : 코드명을 인덱스로 생성, 값은 코드
          - False : 코드를 인덱스로 생성, 값은 코드명
        :return: 코드 타입의 리스트
        """
        data_qs = bw.gets(Code, 'code', c_type=c_type)
        data_dict = {}
        for data in data_qs:
            if is_name_index:
                data_dict[data.name] = data.code
            else:
                data_dict[data.code] = data.name
        return data_dict

    @staticmethod
    def _get_type_list(c_type, is_name_index=False):
        data_qs = bw.gets(Code, 'code', c_type=c_type)
        data_list = []
        for data in data_qs:
            if is_name_index:
                data_list.append(data.name)
            else:
                data_list.append(data.code)
        return data_list

    @staticmethod
    def get_name_to_code_dict(c_type=SYSTEM_CODE_TYPE):
        return CodeWrapper._get_type_dict(c_type, is_name_index=True)

    @staticmethod
    def get_code_to_name_dict(c_type=SYSTEM_CODE_TYPE):
        return CodeWrapper._get_type_dict(c_type, is_name_index=False)

    @staticmethod
    def get_names(c_type=SYSTEM_CODE_TYPE):
        return CodeWrapper._get_type_list(c_type, is_name_index=True)

    @staticmethod
    def get_codes(c_type=SYSTEM_CODE_TYPE):
        return CodeWrapper._get_type_list(c_type, is_name_index=False)

    @staticmethod
    def get_by_code(code):
        return bw.get(Code, code=code)

    @staticmethod
    def get_by_name(name):
        return bw.get(Code, name=name)

    @staticmethod
    def get_all():
        return bw.gets(Code)

    @staticmethod
    def save(datas):
        bw.save(Code, datas)

    @staticmethod
    def delete_all():
        bw.delete(Code)
