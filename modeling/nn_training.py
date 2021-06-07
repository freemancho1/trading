from django_pandas.io import read_frame
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

from config.sysfiles.parameters import *
from modeling.nn_models import lstm
from modeling.utils import ModelingUtils as mu
from stock.wrapper import ModelInfoWrapper as smw
from stock.wrapper import ModelingDataWrapper as smow
from stock.wrapper import ModelingInfoWrapper as smiw


class LstmTraining(object):

    def __init__(self, com_code, kwargs):
        self.modeling_info = {
            'com_code'  : com_code,
            'date'      : smow.get_last_date()
        }
        self.model_info = {
            'model_name': kwargs['model_name'],
            'com_code'  : com_code,
            'date'      : self.modeling_info['date'],
        }
        self.etc_info   = {}
        self.kwargs     = kwargs
        self.kwargs['modeling_info']['window_size'] = self.kwargs['window_size']
        self.is_skip    = {
            'trend'     : False,
            'accuracy'  : False
        }

    def preprocessing(self):
        modeling_data_df = read_frame(smow.get_modeling_datas(self.modeling_info['com_code']))

        self.modeling_info['r_open'] = float(modeling_data_df[-1:]['open'])
        self.modeling_info['r_close'] = float(modeling_data_df[-1:]['close'])
        self.etc_info['max_price'] = mu.get_max_value(modeling_data_df[PRICE_COLUMNS])
        self.etc_info['max_volume'] = mu.get_max_value(modeling_data_df['volume'])
        self.etc_info['data_size'] = len(modeling_data_df)

        modeling_data_df[PRICE_COLUMNS] = mu.normalization_nega1_to_posi1(modeling_data_df[PRICE_COLUMNS])
        modeling_data_df['volume'] = mu.normalization_nega1_to_posi1(modeling_data_df['volume'])

        puri_data = {
            'soc_x' : modeling_data_df[MODELING_COLUMNS].values.tolist(),
            'soc_yo': modeling_data_df['open'].values.tolist(),
            'soc_yc': modeling_data_df['close'].values.tolist(),
            'win_x' : [],
            'win_yo': [],
            'win_yc': []
        }

        loop_cnt = (self.etc_info['data_size'] - self.kwargs['window_size']) - 1
        for i in range(loop_cnt):
            puri_data['win_x'].append(puri_data['soc_x'][i:i+self.kwargs['window_size']])
            puri_data['win_yo'].append(puri_data['soc_yo'][i+self.kwargs['window_size']])
            puri_data['win_yc'].append(puri_data['soc_yc'][i+self.kwargs['window_size']])

        train, test = {}, {}
        train['x'], test['x'], train['yo'], test['yo'], train['yc'], test['yc'] = \
            train_test_split(puri_data['win_x'], puri_data['win_yo'], puri_data['win_yc'],
                             test_size=self.kwargs['test_ratio'], shuffle=False)
        return train, test

    def collbacks(self, monitor):
        early_stopping = EarlyStopping(monitor=monitor, patience=10)

        curr_model_save_path = os.path.join(self.kwargs['model_save_path'],
                                            self.kwargs['model_name'],
                                            str(datetime.now().date()))
        if not os.path.exists(curr_model_save_path):
            os.makedirs(curr_model_save_path, exist_ok=True)
        self.etc_info['model_file_name'] = \
            os.path.join(curr_model_save_path, f'{self.modeling_info["com_code"]}_model.ckpt')
        check_point = ModelCheckpoint(self.etc_info['model_file_name'],
                                      save_best_only=True, save_weights_only=True,
                                      monitor=monitor, verbose=1)
        self.model_info['model_path'] = self.etc_info['model_file_name']

        return early_stopping, check_point

    def training(self, train_x, train_y):
        model = lstm(self.kwargs['modeling_info'])
        self.model_info['info'] = self.kwargs['modeling_info']
        model.fit(train_x, train_y,
                  epochs=self.kwargs['modeling_info']['epochs'],
                  batch_size=self.kwargs['modeling_info']['batch_size'],
                  callbacks=[self.collbacks(monitor='loss')])
        return model

    def modeling(self):
        train, test = self.preprocessing()
        model = self.training(train['x'], train['yc'])
        model.load_weights(self.etc_info['model_file_name'])

        pred_yc = model.predict(test['x'])

        self.modeling_info['accuracy'] = mu.accuracy_trend(test['yc'], pred_yc)
        self.modeling_info['p_close'] = float(pred_yc[-1] * self.etc_info['max_price'])
        self.modeling_info['p_ratio'] = self.modeling_info['p_close'] / self.modeling_info['r_close']
        self.model_info['max_price'] = self.etc_info['max_price']
        self.model_info['max_volume'] = self.etc_info['max_volume']
        self.model_info['accuracy'] = self.modeling_info['accuracy']

        # if self.modeling_info['accuracy'] < MODEL_SKIP_RATIO:
        #     self.is_skip['accuracy'] = True
        # elif self.modeling_info['p_close'] < self.modeling_info['r_close']:
        #     self.is_skip['trend'] = True
        # else:
        #     smiw.save(self.modeling_info)    # 예측결과에 대한 정보는 저장할 필요 없음
        #     smw.save(self.model_info)

        # smiw.save(self.modeling_info)   # 예측결과에 대한 정보는 저장할 필요 없음
        smw.save(self.model_info)

        return self.is_skip