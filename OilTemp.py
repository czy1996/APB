from sympy import *
import json


class OilTemperature:
    def __init__(self, params):
        # 所有参数符号
        self.init_symbols()

        # 地层温度表达式
        self.init_main_expr()

        # 替换计算参数 LR
        self.subs_symbol_LR()

        self.subs_symbol_Ufe()
        self.subs_symbol_TD()

    def init_symbols(self):
        # depth starting from bottom
        self.Z = Symbol('Z')
        # 井底处流体温度
        self.T0 = Symbol('T0')
        # 油层中部温度 摄氏度
        self.Tr = Symbol('Tr')
        # kg/m3
        self.density_of_oil = Symbol('ρ')
        # 定压比热容 J/(kg*K)
        self.Cp = Symbol('Cp')
        # 质量流量 kg/s
        self.W = Symbol('W')
        # 半稳态法得到的计算参数
        self.LR = Symbol('LR')
        # 地温梯度
        self.m = Symbol('m')
        # 重力加速度 m/s^2
        self.g = Symbol('g')
        # 包含了动能项和焦耳-汤姆逊系数（J--T）的计算参数
        self.fi = Symbol('∅')

        # 油管内径
        self.rti = Symbol('rti')

        # 导热系数
        self.Ke = Symbol('Ke')

        # 该微元段传热系数
        self.Ufe = Symbol('Ufe')

        # 无因此地层温度
        self.TD = Symbol('TD')
        # 油管内壁对流换热系数
        self.h = Symbol('h')

        # K 导热系数，下标 t-油管，a-环空，c-套管 cem-水泥环

        self.rto = Symbol('rto')

        self.Kt = Symbol('Kt')

        self.Ka = Symbol('Ka')
        self.rc1i = Symbol('rc1i')
        self.Kc = Symbol('Kc')
        self.rc1o = Symbol('rc1o')
        self.rc2i = Symbol('rc2i')
        self.rc2o = Symbol('rc2o')
        self.rc3i = Symbol('rc3i')
        self.rc3o = Symbol('rc3o')
        self.Kcem = Symbol('Kcem')
        self.rcem = Symbol('rcem')

        self.t = Symbol('t')

        # 地层热扩散系数
        self.ae = Symbol('ae')

        # 井筒尺寸
        self.rw = Symbol('rw')

    def init_main_expr(self):
        self.power_of_exp = -self.LR / (self.W * self.Cp) * self.Z
        # Tz
        self.expr = (self.T0 - self.Tr) * exp(self.power_of_exp) \
                    + (1 - exp(self.power_of_exp)) * (self.m - self.g / self.Cp + self.fi) * self.W * self.Cp / self.LR \
                    + self.Tr - self.m * self.Z

    def subs_symbol_LR(self):
        # 替换计算参数 LR

        # rti?
        LR = 2 * pi * self.rti * self.Ufe * self.Ke / (self.Ke + self.rti * self.Ufe * self.TD)

        self.expr = self.expr.subs(self.LR, LR)

    def subs_symbol_Ufe(self):
        Ufe = 1 / \
              (1 / self.h
               + self.rti / self.Kt * ln(self.rto / self.rti)
               + self.rti / self.Ka * ln(self.rc1i / self.rto)
               + self.rti / self.Kc * ln(self.rc1o / self.rc1i)
               + self.rti / self.Ka * ln(self.rc2i / self.rc1o)
               + self.rti / self.Kc * ln(self.rc2o / self.rc2i)
               + self.rti / self.Ka * ln(self.rc3i / self.rc2o)
               + self.rti / self.Kc * ln(self.rc3o / self.rc3i)
               + self.rti / self.Kcem * ln(self.rcem / self.rc3o)
               )
        self.expr = self.expr.subs(self.Ufe, Ufe)

    def subs_symbol_TD(self):
        td = self.t * self.ae / self.rw ** 2

        TD = ln(exp(-0.2 * td) +
                (1.5 - 0.3719 * exp(-td)) * sqrt(td))

        self.expr = self.expr.subs(self.TD, TD)

    def Ufe_by_depth(self, depth):
        """

        :param depth:
        :return: 该深度处的 Ufe
        """
        pass


if __name__ == '__main__':
    init_printing(use_unicode=True)

    with open('data.json', 'r') as f:
        params = f.read()

    oil_temp = OilTemperature(params)

    pprint(oil_temp.expr, use_unicode=True)
