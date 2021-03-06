import sympy as sp

from common.SymbolsAnnularTemp import Symbols


class Ut(Symbols):
    """
    Ut 只与环空有关，某一个环空的 Ut 不随深度变化
    """

    def __init__(self, temp):
        self.temp = temp

        self.params = temp.params

        self.depth = self.params['well']['casing1']['depth'] - self.temp.Z

    def UtA(self):
        expr = 1 / (
                self.rto / self.h / self.rti +
                self.rto / self.Kt * sp.ln(self.rto / self.rti)
        )

        return expr

    def UtB(self):
        expr_rc1o = 1 / (
                self.rc1o / self.h / self.rti +
                self.rc1o / self.Kt * sp.ln(self.rto / self.rti) +
                self.rc1o / self.Ka * sp.ln(self.rc1i / self.rto) +
                self.rc1o / self.Kc * sp.ln(self.rc1o / self.rc1i)
        )

        expr_rto = 1 / (
                self.rto / self.h / self.rti +
                self.rto / self.Kt * sp.ln(self.rto / self.rti) +
                self.rto / self.Ka * sp.ln(self.rc1i / self.rto) +
                self.rto / self.Kc * sp.ln(self.rc1o / self.rc1i)
        )

        return expr_rto

    def UtC(self):
        expr = 1 / (
                self.rc2o / self.h / self.rti +
                self.rc2o / self.Kt * sp.ln(self.rto / self.rti) +
                self.rc2o / self.Ka * sp.ln(self.rc1i / self.rto) +
                self.rc2o / self.Kc * sp.ln(self.rc1o / self.rc1i) +
                self.rc2o / self.Ka * sp.ln(self.rc2i / self.rc1o) +
                self.rc2o / self.Kc * sp.ln(self.rc2o / self.rc2i)
        )

        expr = 1 / (
                self.rto / self.h / self.rti +
                self.rto / self.Kt * sp.ln(self.rto / self.rti) +
                self.rto / self.Ka * sp.ln(self.rc1i / self.rto) +
                self.rto / self.Kc * sp.ln(self.rc1o / self.rc1i) +
                self.rto / self.Ka * sp.ln(self.rc2i / self.rc1o) +
                self.rto / self.Kc * sp.ln(self.rc2o / self.rc2i)
        )
        return expr
