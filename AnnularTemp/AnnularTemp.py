import sympy as sp
import numpy as np

from matplotlib import pyplot as plt

from AnnularTemp.Symbols import Symbols
from AnnularTemp.Ut import Ut
from AnnularTemp.Ue import Ue
from common.TD import TD


class AnnularTemp(Symbols):
    def __init__(self, params, oil_temps: np.ndarray, Z_index: np.ndarray):
        # 初始化符号
        super().__init__()
        # 结构参数
        self.params = params

        self.init_main_expr()

        self.oil_temps = oil_temps
        self.Z_index = Z_index

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
        self.TD = TD(self).expr()

        self.M = sp.pi * (self.rc1i ** 2 - self.rto ** 2) * self.step * self.density_annular

        self.LR = 2 * sp.pi * (self.rc1i * self.Ue * self.Ke) / (self.Ke + self.rc2i * self.Ue * self.TD)
        self.A = (2 * sp.pi * self.rto * self.Ut * self.Tf + self.LR * self.Te) / self.M / self.CpA
        self.B = (2 * sp.pi * self.rto * self.Ut + self.LR) / self.M / self.CpA

        self.init_main_expr()

    def init_annular_2(self):
        self.Ut = Ut(self).UtB()
        self.Ue = Ue(self).exprB()
        self.TD = TD(self).expr()

        self.M = sp.pi * (self.rc1i ** 2 - self.rto ** 2) * self.step * self.density_annular

        self.LR = 2 * sp.pi * (self.rc2i * self.Ue * self.Ke) / (self.Ke + self.rc2i * self.Ue * self.TD)
        self.A = (2 * sp.pi * self.rto * self.Ut * self.Tf + self.LR * self.Te) / self.M / self.CpA
        self.B = (2 * sp.pi * self.rto * self.Ut + self.LR) / self.M / self.CpA

        self.init_main_expr()

    def init_annular_3(self):
        self.Ut = Ut(self).UtC()
        self.Ue = Ue(self).exprC()
        self.TD = TD(self).expr()

        self.M = sp.pi * (self.rc1i ** 2 - self.rto ** 2) * self.step * self.density_annular

        self.LR = 2 * sp.pi * (self.rc3i * self.Ue * self.Ke) / (self.Ke + self.rc3i * self.Ue * self.TD)
        self.A = (2 * sp.pi * self.rto * self.Ut * self.Tf + self.LR * self.Te) / self.M / self.CpA
        self.B = (2 * sp.pi * self.rto * self.Ut + self.LR) / self.M / self.CpA

        self.init_main_expr()

    def load_params(self):
        """
        将 sympy 符号替换为数值参数
        :return:
        """
        # 从井口开始的深度
        # 计算产液温度的时候已经转换过单位了
        # self.convert_params()

        self.depth = self.params['well']['casing1']['depth'] - self.Z

        replacements = [
            (self.T0, self.depth * self.m + self.Thead),  # 地层温度
            (self.Te, self.depth * self.m + self.Thead),
            (self.Thead, self.params['thermal']['temp_surface']),  # 井口温度
            (self.density_annular, self.params['thermal']['density_annular']),
            (self.m, self.params['thermal']['m']),  # 地温梯度
            (self.CpA, self.params['thermal']['Cp_annular']),
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

        self.expr = self.expr.subs(replacements)

        # 以下是方便 debug
        # self.Ue = self.Ue.subs(replacements)
        # self.Ut = self.Ut.subs(replacements)
        # self.t = self.t.subs(replacements)
        # self.TD = self.TD.subs(replacements)
        # self.LR = self.LR.subs(replacements)
        # self.A = self.A.subs(replacements)
        # self.B = self.B.subs(replacements)
        # self.T0 = self.T0.subs(replacements)
        # self.Te = self.Te.subs(replacements)
        # self.Thead = self.Thead.subs(replacements)

    def run(self):
        # self.cal_temp_A()
        # self.cal_temp_B()
        self.cal_temp_C()
        self.plot()

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

    def cal_temp_C(self):
        # 环空 C 表达式
        self.init_annular_3()

        # 替换计算参数
        self.load_params()

        # 生成以 油温，高度，步长为参数的函数
        self.f = sp.lambdify((self.Tf, self.Z, self.step), self.expr, ['numpy'])

        # 选择环空的计算点，对于环空 C，就是所有高于技术套管的点
        # mask 是 numpy 的特殊语法，用来选择这些点
        mask = self.Z_index >= self.params['well']['casing1']['depth'] - self.params['well']['casing2']['toc']
        self.temps_C_zindex = self.Z_index[mask]

        self.temps_C = self.f(self.oil_temps[mask], self.temps_C_zindex, 1)  # 步长暂时设置为 1 ，貌似没有影响

    def plot(self):
        # temps = self.temps_A
        Z = self.Z_index
        depth = self.params['well']['casing1']['depth']  # 井的总深度

        fig = plt.figure()
        axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
        axes.set_ylim(top=0, bottom=depth)
        axes.xaxis.tick_top()  # 将 x 坐标移到上方
        # axes.plot(temps + 273.15, depth - Z, 'r')
        axes.plot(self.oil_temps + 273.15, depth - Z, 'g')
        axes.plot(self.temps_C + 273.15, depth - self.temps_C_zindex, 'b')
        axes.grid()
        fig.show()
