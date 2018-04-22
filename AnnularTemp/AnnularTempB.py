import sympy as sp
import numpy as np

from matplotlib import pyplot as plt

from AnnularTemp.Symbols import Symbols
from AnnularTemp.Ut import Ut
from AnnularTemp.Ue import Ue
from common.TD import TD


class AnnularTempBMixin:

    def init_annular_2(self):
        self.Ut = Ut(self).UtB()
        self.Ue = Ue(self).exprB()
        self.TD = TD(self).expr()

        self.M = sp.pi * (self.rc1i ** 2 - self.rto ** 2) * self.step * self.density_annular

        self.LR = 2 * sp.pi * (self.rc2i * self.Ue * self.Ke) / (self.Ke + self.rc2i * self.Ue * self.TD)
        self.A = (2 * sp.pi * self.rto * self.Ut * self.Tf + self.LR * self.Te) / self.M / self.CpA
        self.B = (2 * sp.pi * self.rto * self.Ut + self.LR) / self.M / self.CpA

        self.init_main_expr()

    def cal_temp_B(self):
        # 环空 B 表达式
        self.init_annular_2()

        # 替换计算参数
        self.load_params()

        # 生成以 油温，高度，步长为参数的函数
        self.f = sp.lambdify((self.Tf, self.Z, self.step), self.expr, ['numpy'])

        # 选择环空的计算点，对于环空 B，就是所有高于油层套管的点
        mask = self.Z_index >= self.params['well']['casing1']['depth'] - self.params['well']['casing1']['toc']
        self.temps_B_zindex = self.Z_index[mask]

        self.temps_B = self.f(self.oil_temps[mask], self.temps_B_zindex, 1)  # 步长暂时设置为 1 ，貌似没有影响
