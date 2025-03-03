import numpy as np



class Permutation:
    my_loss=None
    def __init__(self, perm,loss):

        self._perm = perm
        Permutation.my_loss = loss
        self._loss = Permutation.my_loss(self._perm)

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
        self._loss= Permutation.my_loss(self._perm)

    @property
    def loss(self):
        return self._loss
