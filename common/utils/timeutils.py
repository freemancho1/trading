from datetime import datetime


class DateTime:

    @staticmethod
    def get_days(period):
        try:
            days = (period['end'] - period['start']).days + 1
        except Exception as e:
            raise Exception(e)
        return days


    @staticmethod
    def is_business_day(date=datetime.now()):
        day_index = datetime.date(date).weekday()
        # 월(0), 화(1), 수(2), 목(3), 금(4), 토(5), 일(6)
        return True if day_index < 5 else False