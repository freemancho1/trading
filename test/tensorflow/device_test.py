import os

import sys
import tensorflow as tf

from tensorflow import keras

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


print(f'Python version : {sys.version}')
print(f'Tensorflow version : {tf.__version__}{"-gpu" if tf.config.list_physical_devices("GPU") else ""}')
print(f'Keras version : {keras.__version__}')

print(f'\n사용 가능한 GPU Device: {tf.test.gpu_device_name()}')
