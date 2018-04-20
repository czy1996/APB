import sympy as sp

from AnnularTemp.Symbols import Symbols
from .UeA import UeAMixin

ln = sp.ln


class Ue(Symbols, UeAMixin):
    def __init__(self, temp):
        super().__init__()

        self.temp = temp

        self.params = temp.params

        self.depth = self.params['well']['casing1']['depth'] - self.temp.Z
