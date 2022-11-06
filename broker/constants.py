
DATA_FOLDER = 'data'

# For login.py
ZERODHA_LOGIN_URL = "https://kite.zerodha.com/api/login"
ZERODHA_TWOFA_URL = "https://kite.zerodha.com/api/twofa"
BROKER_INFO_FILE = "broker_info.dat"

# For downloader.py
# URL format is as :
# https://kite.zerodha.com/oms/instruments/historical/1270529/day?user_id=VY5511&oi=1&from=2021-11-09&to=2022-11-04
ZERODHA_HISTORICAL_DATA_URL_PREFIX = "https://kite.zerodha.com/oms/instruments/historical/"
ZERODHA_HIST_DT_URL_Q_USER_ID = "user_id"
ZERODHA_HIST_DT_URL_Q_DATE_FROM = "from"
ZERODHA_HIST_DT_URL_Q_DATE_TO = "to"
ZERODHA_HIST_DT_URL_Q_OI = "oi"
ZERODHA_HIST_DT_URL_Q_OI_VAL = "1"
ZERODHA_INTERVAL_TYPES = {"day": "day", "5minute": "5minute", "60minute": "60minute"}
ZERODHA_INTERVAL_LIMITS_IN_DAYS = {"day": 2000, "5minute": 100, "60minute" : 400}

STOCK_DATA_HEADERS = ["TIME", "OPEN", "HIGH", "LOW", "CLOSE", "VOLUME", "-"]
STOCK_DATA_INDEX = "TIME"
STOCK_DATA_DIR = "stock_data"
