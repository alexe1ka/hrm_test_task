import numpy as np


class ProbabilitiesArray:

    def __init__(self, probs) -> None:
        super().__init__()
        self._probs = np.array(probs)

    @property
    def probabilities_np(self):
        return self._probs

    def __repr__(self) -> str:
        return f"probabilities list: {self._probs}"
