import numpy as np

from pidgan.optimization.scores.BaseScore import BaseScore


class KLDivergence(BaseScore):
    def __init__(self, name="kld_score", dtype=None) -> None:
        super().__init__(name, dtype)
