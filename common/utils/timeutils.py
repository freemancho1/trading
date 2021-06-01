class DateTime:

    @staticmethod
    def get_days(period):
        try:
            days = (period['end'] - period['start']).days + 1
        except Exception as e:
            raise Exception(e)
        return days