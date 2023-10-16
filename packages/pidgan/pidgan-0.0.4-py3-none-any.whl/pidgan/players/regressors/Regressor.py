import tensorflow as tf
from tensorflow import keras


class Regressor(keras.Model):
    def __init__(self, name=None, dtype=None) -> None:
        super().__init__(name=name, dtype=dtype)
