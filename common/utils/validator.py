from django.core.validators import RegexValidator
from common.utils.properties import *

# 변경된 validators를 적용하기 위해서는 migrate를 해줘야 함(Model에서 사용하기 때문)

# 임시 유효성 검증기
# 자릿수 상관없이 대소문자 및 숫자 사용가능
temp_regex = r'^[A-Za-z0-9]{3,64}'

username_validators = [
    # 필수항목 체크는 폼필드 기본 속성인 required=True에 의해 자동 수행됨.

    # 영숫자로 된 6~64자리 문자열 체크
    # RegexValidator(r'^[A-Za-z0-9]{6,150}$', prject_error_message['username_type'])

    # 임시 유효성 검증 사용
    RegexValidator(temp_regex, sys_error_message['username_set_err'])
]

password_validators = [
    # 숫자 1~45자리, 특수문자 1~45자리, 대소문자 1~45자리인 전체길이 8~50인 문자열
    # RegexValidator(r'(?=.*\d{1,45})(?=.*[~`!@#$%\^&*()-+=]{1,45})(?=.*[a-zA-Z]{1,45}).{8,50}$',
    #                prject_error_message['password_type'])
    RegexValidator(temp_regex, sys_error_message['password_set_err'])
]

email_validators = [
    # 이메일 유효성 검증기
    # RegexValidator(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
    #                prject_error_message['email_type'])
    RegexValidator(temp_regex, sys_error_message['email_set_err'])
]

gender_validators = [
    RegexValidator(r'^[1-3]', sys_error_message['gender_data_err'])
]