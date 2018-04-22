import sympy as sp

from AnnularTemp.Symbols import Symbols
from .UeA import UeAMixin
from .UeB import UeBMixin
from .UeC import UeCMixin

ln = sp.ln


class Ue(Symbols, UeAMixin, UeBMixin, UeCMixin):
    def __init__(self, temp):
        super().__init__()

        self.temp = temp

        self.params = temp.params

        self.depth = self.params['well']['casing1']['depth'] - self.temp.Z
