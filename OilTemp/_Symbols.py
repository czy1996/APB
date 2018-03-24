from sympy import Symbol


class _Symbols:
    def __init__(self):
        self.init_symbols()

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
        self.tcem = Symbol('tcem')

        self.t = Symbol('t')

        # 地层热扩散系数
        self.ae = Symbol('ae')

        # 井筒尺寸
        self.rw = Symbol('rw')
