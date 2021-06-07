from django.db import models


class Company(models.Model):

    com_code            = models.CharField('Company Code', max_length=7, null=False, db_index=True)
    com_name            = models.CharField('Company Name', max_length=500, null=False)
    m_type              = models.CharField('Market Type', max_length=4, null=False)
    chg_date            = models.DateField('Change Date', null=False, auto_now=True)
    t_volume            = models.FloatField('Number of Listed Stocks', null=False)
    data_size           = models.IntegerField('Data Size', null=True)

    class Meta:
        db_table        = 'trading_stock_company'
        ordering        = ['com_code']

    def __init__(self,
                 id, com_code, com_name, m_type, chg_date=None, t_volume=0., data_size=0,
                 *args, **kwargs):
        super(Company, self).__init__(*args, **kwargs)

        self.id         = id
        self.com_code   = com_code
        self.com_name   = com_name
        self.m_type     = m_type
        self.chg_date   = chg_date
        self.t_volume   = t_volume
        self.data_size  = data_size

    def __str__(self):
        return f'COMPANY(ID={self.id}, ' \
               f'COM_CODE={self.com_code}, COM_NAME={self.com_name}, ' \
               f'MARKET_TYPE={self.m_type}, CHG_DATE={self.chg_date}, ' \
               f'TOTAL_VOLUME={self.t_volume}, DATA_SIZE={self.data_size})'


class MarketData(models.Model):

    date                = models.DateField('Trading Date', null=False, db_index=True)
    com_code            = models.CharField('Company Code', max_length=7, null=False, db_index=True)
    com_name            = models.CharField('Company Name', max_length=500, null=False)
    m_type              = models.CharField('Market Type', max_length=4, null=False)
    open                = models.FloatField('Open Price', null=False)
    low                 = models.FloatField('Low Price', null=False)
    high                = models.FloatField('High Price', null=False)
    close               = models.FloatField('Close Price', null=False)
    diff                = models.FloatField('Difference Price', null=False)
    ratio               = models.FloatField('Difference Ratio', null=False)
    volume              = models.FloatField('Volume', null=False)
    value               = models.FloatField('Trading Value', null=False)
    t_volume            = models.FloatField('Number of Listed Stocks', null=False)
    t_value             = models.FloatField('Total Value', null=False)

    class Meta:
        db_table        = 'trading_stock_marketdata'
        ordering        = ['-date', 'com_code']

    def __init__(self,
                 id, date, com_code, com_name, m_type,
                 open, low, high, close, diff, ratio,
                 volume, value, t_volume, t_value, *args, **kwargs):
        super(MarketData, self).__init__(*args, **kwargs)

        self.id         = id
        self.date       = date
        self.com_code   = com_code
        self.com_name   = com_name
        self.m_type     = m_type
        self.open       = open
        self.low        = low
        self.high       = high
        self.close      = close
        self.diff       = diff
        self.ratio      = ratio
        self.volume     = volume
        self.value      = value
        self.t_volume   = t_volume
        self.t_value    = t_value

    def __str__(self):
        return f'MARKET_DATA(ID={self.id}, ' \
               f'DATE={self.date}, COM_CODE={self.com_code}, ' \
               f'PRICES=[{self.open}/ {self.low}/ {self.high}/ {self.close}], ' \
               f'DIFF={self.diff}, RATIO={self.ratio}, ' \
               f'VOLUME={self.volume}, VALUE={self.value}, ' \
               f'TOTAL_VOLUME={self.t_volume}, TOTAL_VALUE={self.t_value})'


class ModelingData(models.Model):

    date                = models.DateField('Trading Date', null=False, db_index=True)
    com_code            = models.CharField('Company Code', max_length=7, null=False, db_index=True)
    open                = models.FloatField('Open Price', null=False)
    low                 = models.FloatField('Low Price', null=False)
    high                = models.FloatField('High Price', null=False)
    close               = models.FloatField('Close Price', null=False)
    volume              = models.FloatField('Volume', null=False)

    class Meta:
        db_table        = 'trading_stock_modelingdata'
        ordering        = ['-date']

    def __init__(self, id, date, com_code, open, low, high, close, volume,
                 *args, **kwargs):
        super(ModelingData, self).__init__(*args, **kwargs)

        self.id         = id
        self.date       = date
        self.com_code   = com_code
        self.open       = open
        self.low        = low
        self.high       = high
        self.close      = close
        self.volume     = volume


    def __str__(self):
        return f'MODELING_DATA(ID={self.id}, ' \
               f'DATE={self.date}, COM_CODE={self.com_code}, ' \
               f'PRICES=[{self.open}/ {self.low}/ {self.high}/ {self.close}], ' \
               f'VOLUME={self.volume})'


class ModelingInfo(models.Model):

    date                = models.DateField('Modeling Date', null=False, db_index=True)
    com_code            = models.CharField('Company Code', max_length=7, null=False, db_index=True)
    r_open              = models.FloatField('Real Today Open Price', null=True)
    r_close             = models.FloatField('Real Today Close Price', null=True)
    p_open              = models.FloatField('Predict Open Price', null=True)
    p_close             = models.FloatField('Predict Close Price', null=True)
    o_ratio             = models.FloatField('Open Price Ratio', null=True)
    c_ratio             = models.FloatField('Close Price Ratio', null=True)
    p_ratio             = models.FloatField('Predict Open-Close Price Ratio', null=True)
    accuracy            = models.FloatField('Test Accuracy', null=True)

    class Meta:
        db_table        = 'trading_stock_modelinginfo'
        ordering        = ['-date']

    def __init__(self,
                 id, date, com_code,
                 r_open=None, r_close=None, p_open=None, p_close=None,
                 o_ratio=None, c_ratio=None, p_ratio=None, accuracy=None,
                 *args, **kwargs):
        super(ModelingInfo, self).__init__(*args, **kwargs)

        self.id         = id
        self.date       = date
        self.com_code   = com_code
        self.r_open     = r_open
        self.r_close    = r_close
        self.p_open     = p_open
        self.p_close    = p_close
        self.o_ratio    = o_ratio
        self.c_ratio    = c_ratio
        self.p_ratio    = p_ratio
        self.accuracy   = accuracy

    def __str__(self):
        return f'MODELING_INFO(ID={self.id}, ' \
               f'DATE={self.date}, COM_CODE={self.com_code}, ' \
               f'REAL DATA=[OPEN={self.r_open}, CLOSE={self.r_close}], ' \
               f'PREDICT DATA=[OPEN={self.p_open}, CLOSE={self.p_close}], ' \
               f'RATIO=[OPEN={self.o_ratio}, CLOSE={self.c_ratio}, CLOSE/OPEN={self.p_ratio}], ' \
               f'ACCURACY={self.accuracy})'


class ModelInfo(models.Model):

    model_name          = models.CharField('Model Name', max_length=100, null=False)
    com_code            = models.CharField('Company Code', max_length=7, default='000000')
    date                = models.DateField('Training Date', null=False, db_index=True)
    info                = models.JSONField('Model Create Info')
    model_path          = models.CharField('Model File Path', max_length=300, null=False)
    max_price           = models.FloatField('Max Value', null=True)
    max_volume          = models.FloatField('Max Volume', null=True)
    accuracy            = models.FloatField('Model Accuracy', null=True)

    class Meta:
        db_table        = 'trading_stock_modelinfo'
        ordering        = ['model_name', '-date']

    def __init__(self,
                 id, model_name, com_code, date, info, model_path,
                 max_price=0., max_volume=0., accuracy=0.,
                 *args, **kwargs):
        super(ModelInfo, self).__init__(*args, **kwargs)

        self.id         = id
        self.model_name = model_name
        self.com_code   = com_code
        self.date       = date
        self.info       = info
        self.model_path = model_path
        self.max_price  = max_price
        self.max_volume = max_volume
        self.accuracy   = accuracy

    def __str__(self):
        return f'MODEL_INFO(ID={self.id}, ' \
               f'MODEL_NAME={self.model_name}, COM_CODE={self.com_code}, ' \
               f'DATE={self.date}, INFO=[{self.info}], ' \
               f'MODEL_PATH={self.model_path}, ' \
               f'MAX_PRICE/VOLUME={self.max_price}/{self.max_volume}, ACCURACY={self.accuracy})'


class MyTrading(models.Model):

    date                = models.DateField('Trading Date', null=False, db_index=True)
    com_code            = models.CharField('Company Code', max_length=7, null=False, db_index=True)
    t_type              = models.CharField('Trading Type', max_length=4, null=False)
    t_count             = models.IntegerField('Trading Count', null=False)
    p_close             = models.FloatField('Predict Close Price', null=True)
    buy_price           = models.FloatField('Buy Price')
    sell_price          = models.FloatField('Sell Price')
    ratio               = models.FloatField('Ratio')
    volume              = models.FloatField('Trading Volume')
    profit              = models.FloatField('Trading Profit')

    class Meta:
        db_table        = 'trading_stock_mytrading'
        ordering        = ['-date', 'com_code']

    def __init__(self,
                 id, date, com_code, t_type, t_count, p_close=0.,
                 buy_price=0, sell_price=0, ratio=.0,
                 volume=0, profit=.0,
                 *args, **kwargs):
        super(MyTrading, self).__init__(*args, **kwargs)

        self.id         = id
        self.date       = date
        self.com_code   = com_code
        self.t_type     = t_type
        self.t_count    = t_count
        self.p_close    = int(p_close)
        self.buy_price  = buy_price
        self.sell_price = sell_price
        self.ratio      = ratio
        self.volume     = volume
        self.profit     = profit

    def __str__(self):
        return f'MY_TRADING(ID={self.id}, ' \
               f'DATE={self.date}, COM_CODE={self.com_code}, ' \
               f'TRADING_TYPE/COUNT=[{self.t_type}/{self.t_count}], ' \
               f'PREDICT_CLOSE={self.p_close}, ' \
               f'PRICE=[BUY={self.buy_price}, SELL={self.sell_price}], ' \
               f'RATIO={self.ratio}, VOLUME={self.volume}, PROFIT={self.profit})'


class Account(models.Model):

    acc_name            = models.CharField('Account Name', max_length=20, null=False, unique=True)
    t_type              = models.CharField('Trading Type', max_length=4, null=False)
    t_count             = models.IntegerField('Trading Count', null=False)
    base_money          = models.FloatField('Base Money', null=False)
    balance             = models.FloatField('Current Balance', null=True)
    ratio               = models.FloatField('Ratio', null=True)
    first_date          = models.DateField('First Trading Date', auto_now_add=True) # 레코드 생성시 한번 갱신
    last_date           = models.DateField('Last Trading Date', auto_now=True)      # 레코드 변경시 자동 갱신

    class Meta:
        db_table        = 'trading_stock_account'
        ordering        = ['t_type', 't_count']

    def __init__(self,
                 id, acc_name, t_type, t_count, base_money,
                 balance=.0, ratio=.0, first_date=None, last_date=None,
                 *args, **kwargs):
        super(Account, self).__init__(*args, **kwargs)

        self.id         = id
        self.acc_name   = acc_name
        self.t_type     = t_type
        self.t_count    = t_count
        self.base_money = base_money
        self.balance    = balance
        self.ratio      = ratio
        self.first_date = first_date
        self.last_date  = last_date

    def __str__(self):
        return f'ACCOUNT(ID={self.id}, ' \
               f'ACC_NAME={self.acc_name}, ' \
               f'TRADING_INFO=[TYPE={self.t_type}, COUNT={self.t_count}], ' \
               f'BASE_MONEY={self.base_money}, ' \
               f'BALANCE={self.balance:,.0}, RATIO={self.ratio:.0}, ' \
               f'FIRST_DATE={self.first_date}, LAST_DATE={self.last_date})'