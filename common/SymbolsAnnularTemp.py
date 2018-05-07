from sympy import Symbol


class Symbols:
    """
    计算环空温度需要用到的符号
    """

    def __init__(self):
        # 从井底开始的高度， 用来计算井身结构
        self.Z = Symbol('Z')

        self.A = Symbol('A')  # 计算参数
        self.B = Symbol('B')  # 计算参数

        self.T0 = Symbol('T0')  # 初始温度
        self.Tf = Symbol('Tf')  # 油管液体温度

        self.M = Symbol('M')  # 该段环空液体质量
        self.CpA = Symbol('CpA')  # 环空液体比热容

        self.Te = Symbol('Te')  # 该深度地层温度
        self.Ut = Symbol('Ut')  # 从油管流体到该微段环空的传热系数
        self.LR = Symbol('LR')  # 计算参数
        self.Ue = Symbol('Ue')  # 从环空到水泥环边界的传热系数
        self.density_annular = Symbol('density')

        self.step = Symbol('step')

        # 地温梯度
        self.m = Symbol('m')

        self.Thead = Symbol('Thead')

        # 油管内径
        self.rti = Symbol('rti')

        # 导热系数
        self.Ke = Symbol('Ke')

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
        self.tcem = Symbol('tcem')

        self.t = Symbol('t')

        # 地层热扩散系数
        self.ae = Symbol('ae')

        # 无因此地层温度
        self.TD = Symbol('TD')
