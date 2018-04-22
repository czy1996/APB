import sympy as sp

from AnnularTemp.Ut import Ut
from AnnularTemp.Ue import Ue
from common.TD import TD


class AnnularTempAMixin:

    def init_annular_1(self):
        self.Ut = Ut(self).UtA()
        self.Ue = Ue(self).exprA()
        self.TD = TD(self).expr()

        self.M = sp.pi * (self.rc1i ** 2 - self.rto ** 2) * self.step * self.density_annular

        self.LR = 2 * sp.pi * (self.rc1i * self.Ue * self.Ke) / (self.Ke + self.rc2i * self.Ue * self.TD)
        self.A = (2 * sp.pi * self.rto * self.Ut * self.Tf + self.LR * self.Te) / self.M / self.CpA
        self.B = (2 * sp.pi * self.rto * self.Ut + self.LR) / self.M / self.CpA

        self.init_main_expr()

    def cal_temp_A(self):
        # 环空 A 表达式
        self.init_annular_1()

        # 替换计算参数
        self.load_params()

        # 生产以 油温，高度，步长为参数的函数
        self.f = sp.lambdify((self.Tf, self.Z, self.step), self.expr, ['numpy'])

        # 选择环空的计算点，对于环空 A，就是所有大于等于 0 的点
        mask = self.Z_index >= 0
        self.temps_A_zindex = self.Z_index[mask]

        self.temps_A = self.f(self.oil_temps, self.temps_A_zindex, 1)  # 步长暂时设置为 1 ，貌似没有影响
