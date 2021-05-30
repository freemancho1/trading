import os
import platform
from datetime import datetime
from enum import Enum, IntEnum

# USER PATH
_USER_PATH              = os.path.expanduser('~')

# PROJCET PATH
_PROJECT_NAME           = 'trading'
_PROJECT_BASE           = os.path.join(_USER_PATH, 'projects')
_PROJECT_PATH           = os.path.join(_PROJECT_BASE, _PROJECT_NAME)
_PROJECT_SYSFILE_PATH   = os.path.join(_PROJECT_PATH, 'config', 'sysfile')

# WEB DRIVER PATH
_WEB_DRIVER_BASE        = os.path.join(_USER_PATH, '.local', 'bin')
if 'Windows' in platform.platform():
    WEB_DRIVER_PATH     = os.path.join(_WEB_DRIVER_BASE, 'chromedriver.exe')
else:
    WEB_DRIVER_PATH     = os.path.join(_WEB_DRIVER_BASE, 'chromedriver')

# CODE TABLE PARAMETER
_CODE_FILE_NAME         = 'code.csv'
CODE_FILE_PATH          = os.path.join(_PROJECT_SYSFILE_PATH, _CODE_FILE_NAME)
SYSTEM_CODE_TYPE        = '0'

# CRAWLING PARAMETER
CRAWLING_TIME           = '17:00:00'
CRAWLING_WAITING_TIME   = 6 if 9 <= int(datetime.now().strftime('%H')) < 16 else 3

# TRADING PARAMETER
FIRST_TRADING_DATE      = '19950502'
BASE_TRADING_DATE       = '20000529'
TRADING_MIN_COUNT       = 1
TRADING_MID_COUNT       = 3
TRADING_MAX_COUNT       = 5
TRADING_COUNTS          = [TRADING_MIN_COUNT, TRADING_MID_COUNT, TRADING_MAX_COUNT]
TRADING_BASE_MONEY      = 5000000

# CRAWLING PARAMETER
