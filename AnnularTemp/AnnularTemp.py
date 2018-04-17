import sympy as sp
import numpy as np

from AnnularTemp.Symbols import Symbols
from AnnularTemp.Ut import Ut
from AnnularTemp.Ue import Ue


class AnnularTemp(Symbols):
    def __init__(self, params, oil_temps: np.ndarray, z: np.ndarray):
        # 初始化符号
        super().__init__()
        # 结构参数
        self.params = params

        self.init_main_expr()

    def init_main_expr(self):
        """
        本模块的复杂性在于，要计算三个环空，每个环空的井身结构都与深度有关
        分别使用三个方法，来各自环空，在各自方法中要用相对应的计算参数
        :return:
        """
        self.expr = self.A / self.B - (self.A / self.B - self.T0) * sp.exp(-self.B * self.t)

    def init_annular_1(self):
        self.Ut = Ut(self).UtA()
        self.Ue = Ue(self).exprA()
        self.A = (2 * sp.pi * self.rto * self.Ut * self.Tf + self.LR * self.Te) / self.M / self.CpA

        self.init_main_expr()
