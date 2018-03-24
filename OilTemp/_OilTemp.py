from sympy import *
import json

from OilTemp.Ufe import Ufe
from OilTemp.TD import TD
from OilTemp._Symbols import _Symbols


class OilTemperature(_Symbols):
    def __init__(self, params):
        # 初始化符号
        super().__init__()
        # 结构参数
        self.params = params

        self._Ufe = Ufe(self)
        self._TD = TD(self)

        # 替换计算参数 LR
        self.TD = self._TD.expr()

        self.Ufe = self._Ufe.expr()

        # pprint(self.Ufe)

        self.LR = self.init_expr_LR()

        # 地层温度表达式
        self.init_main_expr()

    def init_main_expr(self):
        self.power_of_exp = -self.LR / (self.W * self.Cp) * self.Z
        # Tz
        self.expr = (self.T0 - self.Tr) * exp(self.power_of_exp) \
                    + (1 - exp(self.power_of_exp)) * (self.m - self.g / self.Cp + self.fi) * self.W * self.Cp / self.LR \
                    + self.Tr - self.m * self.Z

    def init_expr_LR(self):
        # 替换计算参数 LR

        # rti?
        LR = 2 * pi * self.rti * self.Ufe * self.Ke / (self.Ke + self.rti * self.Ufe * self.TD)

        return LR


if __name__ == '__main__':
    init_printing(use_unicode=True)

    with open('data.json', 'r') as f:
        params = json.load(f)

    oil_temp = OilTemperature(params)

    # pprint(params)

    print(latex(oil_temp.expr))
