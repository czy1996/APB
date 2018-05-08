import sympy as sp

from AnnularTemp.Ut import Ut
from AnnularTemp.Ue import Ue
from common.TD import TD


class AnnularTempCMixin:
    def init_annular_3(self):
        self.Ut = Ut(self).UtC()
        self.Ue = Ue(self).exprC()
        self.TD = TD(self).expr()

        self.M = sp.pi * (self.rc1i ** 2 - self.rto ** 2) * self.step * self.density_annular

        self.LR = 2 * sp.pi * (self.rc3i * self.Ue * self.Ke) / (self.Ke + self.rc3i * self.Ue * self.TD)
        self.A = (2 * sp.pi * self.rto * self.Ut * self.Tf + self.LR * self.Te) / self.M / self.CpA
        self.B = (2 * sp.pi * self.rto * self.Ut + self.LR) / self.M / self.CpA

        self.init_main_expr()

    def cal_temp_C(self):
        # 环空 C 表达式
        self.init_annular_3()

        # 替换计算参数
        self.load_params()

        # 生成以 油温，高度，步长为参数的函数
        self.f = sp.lambdify((self.Tf, self.Z, self.step), self.expr, ['numpy'])

        # 选择环空的计算点，对于环空 C，就是所有高于技术套管 toc 的点
        # mask 是 numpy 的特殊语法，用来选择这些点
        mask = self.zindex >= self.params['well']['casing1']['depth'] - self.params['well']['casing2']['toc']
        self._temps_C_zindex = self.zindex[mask]

        self._temps_C = self.f(self.oil_temps[mask], self._temps_C_zindex, 1)  # 步长暂时设置为 1 ，貌似没有影响

    @property
    def temps_C_in_C(self):
        return self._temps_C + 273.15

    @property
    def temps_C_in_K(self):
        return self._temps_C

    @property
    def zindex_C(self):
        """
        计算点 z 坐标
        :return:
        """
        return self._temps_C_zindex
