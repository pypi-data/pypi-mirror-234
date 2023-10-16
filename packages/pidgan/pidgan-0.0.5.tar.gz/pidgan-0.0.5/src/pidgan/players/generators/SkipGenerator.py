import tensorflow as tf

from pidgan.players.generators import BaseGenerator


class SkipGenerator(BaseGenerator):
    def __init__(self, name=None, dtype=None) -> None:
        super().__init__(name=name, dtype=dtype)
