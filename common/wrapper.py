from models import *
from utils.base_wrapper import BaseWrapper as bw
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
        try:
            data_qs = bw.gets(Code, 'code', c_type=c_type)
        except Exception as e:
            raise Exception(f'gets Code table error!: c_type={c_type}\n{str(e)}')
        else:
            datas = {}
            for data in data_qs:
                if is_name_index:
                    datas[data.name] = data.code
                else:
                    datas[data.code] = data.name
        return datas

    @staticmethod
    def get_name_to_code_dict(c_type=SYSTEM_CODE_TYPE):
        return CodeWrapper._get_type_dict(c_type, is_name_index=True)

    @staticmethod
    def get_code_to_name_dict(c_type=SYSTEM_CODE_TYPE):
        return CodeWrapper._get_type_dict(c_type, is_name_index=False)