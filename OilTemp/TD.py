from sympy import Piecewise, ln, exp, sqrt

from OilTemp._Symbols import _Symbols


class TD(_Symbols):
    def __init__(self, temp):
        super().__init__()
        self.temp = temp
        self.params = temp.params
        self.depth = self.params['well']['casing1']['depth'] - self.temp.Z

    def rules(self):
        depth_of_casing2 = self.params['well']['casing2']['depth']
        TD_1 = (
            self.rc2i,
            self.depth > depth_of_casing2,
        )

        depth_of_casing3 = self.params['well']['casing3']['depth']
        TD_2 = (
            self.rc3i,
            self.depth > depth_of_casing3,
        )

        TD_3 = (
            self.rc3o + self.tcem,
            self.depth > 0,
        )

        return [
            TD_1,
            TD_2,
            TD_3,
        ]

    def expr(self):
        rules = self.rules()

        rw = Piecewise(
            *rules,
        )
        td = self.t * self.ae / rw ** 2

        TD = ln(exp(-0.2 * td) +
                (1.5 - 0.3719 * exp(-td)) * sqrt(td))

        return TD
