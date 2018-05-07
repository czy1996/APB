import sympy as sp
import numpy as np

from matplotlib.axes import Axes

from common.SymbolsAnnularTemp import Symbols
from AnnularTemp.AnnularTempA import AnnularTempAMixin
from AnnularTemp.AnnularTempB import AnnularTempBMixin
from AnnularTemp.AnnularTempC import AnnularTempCMixin
from common import init_fig_axes


class AnnularTemp(Symbols,
                  AnnularTempAMixin,
                  AnnularTempBMixin,
                  AnnularTempCMixin,
                  ):
    def __init__(self, params, oil_temps: np.ndarray, zindex: np.ndarray):
        # 初始化符号
        super().__init__()
        # 结构参数
        self.params = params

        self.init_main_expr()

        self.oil_temps = oil_temps
        self.zindex = zindex

    def init_main_expr(self):
        """
        本模块的复杂性在于，要计算三个环空，每个环空的井身结构都与深度有关
        分别使用三个方法，来各自环空，在各自方法中要用相对应的计算参数
        :return:
        """
        self.expr = self.A / self.B - (self.A / self.B - self.T0) * sp.exp(-self.B * self.t)

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
        self.cal_temp_A()
        self.cal_temp_B()
        self.cal_temp_C()
        # self.plot()

    def plot(self, axes=None):

        if axes is None:
            return self._plot_new_fig()
        else:
            self._plot_with_axes(axes)

    def _plot_with_axes(self, axes: Axes):
        depth = self.params['well']['casing1']['depth']  # 井的总深度

        axes.plot(self.temps_A_in_C, depth - self.zindex_A, 'r')
        axes.plot(self.temps_B_in_C, depth - self.zindex_B, 'b')
        axes.plot(self.temps_C_in_C, depth - self.zindex_C, 'c')

    def _plot_new_fig(self):
        depth = self.params['well']['casing1']['depth']  # 井的总深度

        fig, axes = init_fig_axes(depth)

        self._plot_with_axes(axes)
        fig.show()
        return fig
