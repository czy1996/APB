import sympy as sp
import numpy as np
import json
import matplotlib.pyplot as plt

from OilTemp.Ufe import Ufe
from common.SymbolsOilTemp import Symbols
from common.TD import TD
from common import init_fig_axes


class OilTemperature(Symbols):
    def __init__(self, params):
        # 结构参数
        self.params = params

        # 地层温度表达式
        self.init_main_expr()

    def init_main_expr(self):
        # 三个个随井身变化的计算参数，顺序不能乱
        self.TD = TD(self).expr()
        self.Ufe = Ufe(self).expr()
        self.LR = self.init_expr_LR()

        self.power_of_exp = -self.LR / (self.W * self.Cp) * self.step
        # Tz
        self.expr = (self.To - self.Tr) * sp.exp(self.power_of_exp) + (1 - sp.exp(self.power_of_exp)) * (
                self.m - self.g / self.Cp + 0) * self.W * self.Cp / self.LR + self.Tr - self.m * self.step

        # 这里为了方便把动能项直接设 0

    def init_expr_LR(self):
        # 替换计算参数 LR

        # rti?
        LR = 2 * sp.pi * self.rti * self.Ufe * self.Ke / (self.Ke + self.rti * self.Ufe * self.TD)

        return LR

    def convert_params(self):
        """
        单位转换
        :return:
        """
        self.params['well']['casing1']['ro'] *= 0.001
        self.params['well']['casing1']['ri'] *= 0.001
        self.params['well']['casing2']['ro'] *= 0.001
        self.params['well']['casing2']['ri'] *= 0.001
        self.params['well']['casing3']['ro'] *= 0.001
        self.params['well']['casing3']['ri'] *= 0.001
        self.params['well']['tubing']['ro'] *= 0.001
        self.params['well']['tubing']['ri'] *= 0.001
        self.params['well']['etc']['tcem'] *= 0.001

        self.params['thermal']['W'] = self.params['thermal']['W'] * 1000 / 24 / 3600

        self.params['etc']['t'] *= 24 * 3600

        self.params['thermal']['temp_surface'] -= 273.15

    def load_params(self):
        """
        将 sympy 符号替换为数值参数
        :return:
        """
        # 从井口开始的深度

        # self.convert_params()

        self.depth = self.params['well']['casing1']['depth'] - self.Z

        replacements = [
            (self.Tr, self.depth * self.m + self.Thead),  # 地层温度
            (self.Thead, self.params['thermal']['temp_surface']),  # 井口温度
            (self.density_of_oil, self.params['thermal']['density_oil']),  # 产
            (self.Cp, self.params['thermal']['Cp_oil']),  # 产液比热容
            (self.W, self.params['thermal']['W']),  # 质量流量，
            (self.m, self.params['thermal']['m']),  # 地温梯度
            (self.g, 9.8),  # 重力加速度
            (self.fi, 0),  # 忽略动能项
            (self.Ke, self.params['thermal']['Ke']),  # 地层导热系数
            (self.h, self.params['thermal']['h']),  # 对流换热系数
            (self.rti, self.params['well']['tubing']['ri']),  # 油管内径
            (self.rto, self.params['well']['tubing']['ro']),  # 油管外径
            (self.rc1i, self.params['well']['casing1']['ri']),
            (self.rc1o, self.params['well']['casing1']['ro']),
            (self.rc2i, self.params['well']['casing2']['ri']),
            (self.rc2o, self.params['well']['casing2']['ro']),
            (self.rc3i, self.params['well']['casing3']['ri']),
            (self.rc3o, self.params['well']['casing3']['ro']),
            (self.Kt, self.params['thermal']['Kt']),
            (self.Ka, self.params['thermal']['Ka']),
            (self.Kc, self.params['thermal']['Kc']),
            (self.Kcem, self.params['thermal']['Kcem']),
            (self.tcem, self.params['well']['etc']['tcem']),
            (self.ae, self.params['thermal']['ae']),
            (self.t, self.params['etc']['t']),
        ]

        self.Tr = self.Tr.subs(replacements)
        self.expr = self.expr.subs(replacements)

    def run(self):
        # 将表达式转换为 numpy 能够计算的函数
        self.f = sp.lambdify((self.To, self.Z, self.step), self.expr, ["numpy"])

        To0 = self.params['thermal']['temp_surface'] + self.params['thermal']['m'] * self.params['well']['casing1'][
            'depth']

        depth = self.params['well']['casing1']['depth']  # 井的总深度
        zindex = np.arange(0, int(depth), 1, dtype=float)  # 计算点坐标
        temps = np.zeros_like(zindex, dtype=float)
        temps[0] = To0

        f_temps_earth = sp.lambdify(self.Z, self.Tr, "numpy")
        self._temps_earth = f_temps_earth(zindex)
        self.loop(temps, zindex)

    def loop(self, temps, zindex):
        n = temps.shape[0]
        for i in range(1, n):
            # print(_temps[i - 1], zindex[i])
            temps[i] = self.f(temps[i - 1], zindex[i], 1)
            # print(i, _temps[i])

        self._temps = temps
        self.zindex = zindex

        return temps

    @property
    def temps_in_K(self):
        return self._temps

    @property
    def temps_in_C(self):
        return self._temps + 273.15

    @property
    def temps_earth_in_C(self):
        return self._temps_earth + 273.15

    def _plot_new_fig(self):
        depth = self.params['well']['casing1']['depth']  # 井的总深度

        fig, axes = init_fig_axes(depth)
        self._plot_with_axes(axes)
        # axes.plot(_temps, depth - Z, 'y')
        fig.show()

    def _plot_with_axes(self, axes):
        depth = self.params['well']['casing1']['depth']  # 井的总深度

        temps = self.temps_in_C
        Z = self.zindex
        axes.plot(temps, depth - Z, 'g', label='产液温度')
        axes.plot(self.temps_earth_in_C, depth - Z, 'y', label='地层温度')

    def plot(self, axes=None):
        if axes is None:
            self._plot_new_fig()
        else:
            self._plot_with_axes(axes)


if __name__ == '__main__':
    # 以下代码只有在本文件执行时才会执行
    # 在本文件作为模块引入时不会执行
    sp.init_printing(use_unicode=True)

    with open('data.json', 'r') as f:
        params = json.load(f)

    oil_temp = OilTemperature(params)

    oil_temp.load_params()

    # pprint(params)

    print(sp.latex(oil_temp.expr))
