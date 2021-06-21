from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout


class lstm:

    @staticmethod
    def model(kwargs):
        model = Sequential([
            LSTM(units=kwargs['input_units'],
                 activation=kwargs['activation_fn'],
                 return_sequences=True,
                 input_shape=(kwargs['window_size'], kwargs['feature_size'])),
            Dropout(kwargs['dropout']),
            LSTM(units=kwargs['middle_units'],
                 activation=kwargs['activation_fn']),
            Dropout(kwargs['dropout']),
            Dense(kwargs['output_units'])
        ])
        model.compile(optimizer=kwargs['optimizer'], loss=kwargs['loss'],
                      metrics=kwargs['metrics'])
        return model