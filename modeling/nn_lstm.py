from config.sysfiles.parameters import *
from modeling.utils import ModelingUtils as mu

from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout


class Lstm(object):

    def __init__(self, kwargs):
        self.kwargs = kwargs

    def get_model(self):
        model = Sequential([
            LSTM(units=self.kwargs['input_units'],
                 activation=self.kwargs['activation_fn'],
                 return_sequences=True,
                 input_shape=(self.kwargs['window_size'], self.kwargs['feature_size'])),
            Dropout(self.kwargs['dropout']),
            LSTM(units=self.kwargs['middle_units'],
                 activation=self.kwargs['activation_fn']),
            Dropout(self.kwargs['dropout']),
            Dense(self.kwargs['output_units'])
        ])
        model.compile(optimizer=self.kwargs['optimizer'], loss=self.kwargs['loss'],
                      metrics=self.kwargs['metrics'])
        return model

    @staticmethod
    def train_preprocessing(data_df):
        data_info = {
            'last_data': {
                'open': float(data_df[-1:]['open']),
                'close': float(data_df[-1:]['close'])
            },
            'max_price': mu.get_max_value(data_df[PRICE_COLUMNS]),
            'max_volume': mu.get_max_value(data_df['volume']),
            'data_size': len(data_df)
        }

        data_df[PRICE_COLUMNS] = mu.normalization_nega1_to_posi1(data_df[PRICE_COLUMNS])
        data_df['volume'] = mu.normalization_nega1_to_posi1(data_df['volume'])

        soc_data = {
            'x': data_df[MODELING_COLUMNS].values.tolist(),
            'yo': data_df['open'].values.tolist(),
            'yc': data_df['close'].values.tolist(),
        }