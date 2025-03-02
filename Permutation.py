import numpy as np
import metrics
from main import loss


class Permutation:

    def __init__(self, perm):

        self._perm = perm
        self._loss = loss(self._perm)

    def __ne__(self, other):
        return np.sum(np.array(self._perm) != np.array(other.perm))

    def __str__(self):
        return f"perm - {self.perm} loss - {self._loss}"

    @property
    def perm(self):
        return self._perm

    @perm.setter
    def perm(self,permut):
        self._perm=permut
        self._loss=metrics.loss(self._perm)

    @property
    def loss(self):
        return self._loss
