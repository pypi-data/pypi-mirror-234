import numpy as np

from pidgan.optimization.scores.BaseScore import BaseScore


class JSDivergence(BaseScore):
    def __init__(self, name="jsd_score", dtype=None) -> None:
        super().__init__(name, dtype)
