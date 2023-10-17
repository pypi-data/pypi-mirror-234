import os
import tensorflow as tf
from tensorflow import keras


def use_gpu(use_gpu=True):
    # os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
    # os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'
    # os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    physical_devices = tf.config.list_physical_devices('GPU')
    if use_gpu and len(physical_devices):
        print(f"TF version: {tf.__version__}")
        # print(f"keras version: {keras.__version__}")

        for gpu in physical_devices:
            print(f"Found GPU: {gpu}")
            try:
                tf.config.experimental.set_memory_growth(gpu, True)
            except RuntimeError:
                pass

    else:
        print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
        assert not use_gpu
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
