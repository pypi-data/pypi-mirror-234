import tensorflow as tf

from pidgan.players.discriminators import BaseDiscriminator


class SkipDiscriminator(BaseDiscriminator):
    def __init__(self, name=None, dtype=None) -> None:
        super().__init__(name=name, dtype=dtype)
