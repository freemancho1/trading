class DataConverter:

    @staticmethod
    def other_to_dict(data):
        data_type = str(type(data))
        if 'DataFrame' in data_type:
            if len(data) == 1:
                chg_data = data.to_dict('records')[0]
            else:
                chg_data = data.to_dict('records')
        elif 'Series' in data_type:
            chg_data = data.to_dict()
        elif 'models' in data_type:
            chg_data = data.__dict__
            del chg_data['_state']
        else:
            raise Exception(f'Unsupported data type: type - {data_type}')
        return chg_data