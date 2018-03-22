from sympy import *

from _Symbols import _Symbols


class Ufe(_Symbols):
    def __init__(self, temp):
        super().__init__()
        self.temp = temp
        self.params = temp.params
        self.depth = self.params['well']['casing1']['depth'] - self.temp.Z

    def rules(self):
        """
        井身结构变化规则
        :return: list
        """
        depth_of_casing2 = self.params['well']['casing2']['depth']
        Ufe_1 = (
            self.Ufe_1(),
            self.depth > depth_of_casing2,
        )

        toc_of_casing1 = self.params['well']['casing1']['toc']
        Ufe_2 = (
            self.Ufe_2(),
            self.depth > toc_of_casing1,
        )

        depth_of_casing3 = self.params['well']['casing3']['depth']
        Ufe_3 = (
            self.Ufe_3(),
            self.depth > depth_of_casing3,
        )

        toc_of_casing2 = self.params['well']['casing2']['toc']
        Ufe_4 = (
            self.Ufe_4(),
            self.depth > toc_of_casing2,
        )

        Ufe_5 = (
            self.Ufe_5(),
            self.depth > 0,
        )

        return [
            Ufe_1,
            Ufe_2,
            Ufe_3,
            Ufe_4,
            Ufe_5,
        ]

    def expr(self):
        rules = self.rules()

        _expr = Piecewise(
            *rules,
        )

        return _expr

    def Ufe_1(self):
        """
        从井底到第二层套管鞋
        :return:
        """
        Ufe = 1 / \
              (1 / self.h
               + self.rti / self.Kt * ln(self.rto / self.rti)
               + self.rti / self.Ka * ln(self.rc1i / self.rto)
               + self.rti / self.Kc * ln(self.rc1o / self.rc1i)
               + self.rti / self.Kcem * ln(self.rc2i / self.rc1o)
               )

        return Ufe

    def Ufe_2(self):
        """
        从第二层套管鞋到第一层 toc (油层套管 toc)
        :return:
        """
        Ufe = 1 / \
              (1 / self.h
               + self.rti / self.Kt * ln(self.rto / self.rti)
               + self.rti / self.Ka * ln(self.rc1i / self.rto)
               + self.rti / self.Kc * ln(self.rc1o / self.rc1i)
               + self.rti / self.Kcem * ln(self.rc2i / self.rc1o)
               + self.rti / self.Kc * ln(self.rc2o / self.rc2i)
               + self.rti / self.Kcem * ln(self.rc3i / self.rc2o)
               )

        return Ufe

    def Ufe_3(self):
        """
        从第一层 toc (油层套管 toc) 到表层套管鞋
        :return:
        """
        Ufe = 1 / \
              (1 / self.h
               + self.rti / self.Kt * ln(self.rto / self.rti)
               + self.rti / self.Ka * ln(self.rc1i / self.rto)
               + self.rti / self.Kc * ln(self.rc1o / self.rc1i)
               + self.rti / self.Ka * ln(self.rc2i / self.rc1o)
               + self.rti / self.Kc * ln(self.rc2o / self.rc2i)
               + self.rti / self.Kcem * ln(self.rc3i / self.rc2o)
               )

        return Ufe

    def Ufe_4(self):
        """
        从表层套管鞋到第二层 toc
        :return:
        """
        Ufe = 1 / \
              (1 / self.h
               + self.rti / self.Kt * ln(self.rto / self.rti)
               + self.rti / self.Ka * ln(self.rc1i / self.rto)
               + self.rti / self.Kc * ln(self.rc1o / self.rc1i)
               + self.rti / self.Ka * ln(self.rc2i / self.rc1o)
               + self.rti / self.Kc * ln(self.rc2o / self.rc2i)
               + self.rti / self.Kcem * ln(self.rc3i / self.rc2o)
               + self.rti / self.Kc * ln(self.rc3o / self.rc3i)
               + self.rti / self.Kcem * ln(self.rcem / self.rc3o)
               )

        return Ufe

    def Ufe_5(self):
        """
        从第二层他 toc 到井口
        :return:
        """
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

        return Ufe

    def __Ufe_full(self):
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

        return Ufe
