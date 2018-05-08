import sympy as sp

from common.SymbolsOilTemp import Symbols


class TD(Symbols):
    """
    本模块用来返回 TD 的表达式
    表达式为一个分段函数 (Piecewise) , 与井深结构相关
    """

    def __init__(self, temp):
        """

        :param temp: OilTemperature Class
        本函数注释同 Ufe
        """
        self.temp = temp
        self.params = temp.params
        self.depth = self.params['well']['casing1']['depth'] - self.temp.Z

    def rules(self):
        depth_of_casing2 = self.params['well']['casing2']['depth']
        TD_1 = (
            self.rc2i,
            self.depth >= depth_of_casing2,
        )

        depth_of_casing3 = self.params['well']['casing3']['depth']
        TD_2 = (
            self.rc3i,
            self.depth >= depth_of_casing3,
        )

        TD_3 = (
            self.rc3o + self.tcem,
            self.depth >= 0,
        )

        return [
            TD_1,
            TD_2,
            TD_3,
        ]

    def expr(self):
        rules = self.rules()

        rw = sp.Piecewise(
            *rules,
        )
        td = self.t * self.ae / rw ** 2
        TD = sp.ln(sp.exp(-0.2 * td) +
                   (1.5 - 0.3719 * sp.exp(-td)) * sp.sqrt(td))

        return TD
