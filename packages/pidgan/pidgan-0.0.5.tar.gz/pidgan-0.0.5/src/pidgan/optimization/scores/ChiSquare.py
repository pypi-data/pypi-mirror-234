import numpy as np

from pidgan.optimization.scores.BaseScore import BaseScore


class ChiSquare(BaseScore):
    def __init__(self, name="chi2_score", dtype=None) -> None:
        super().__init__(name, dtype)
