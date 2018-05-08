from sympy import Symbol


class Symbols:
    """
    本模块包含了所有计算温度曲线时所用到的符号
    用于给 _OilTemp 继承，单独没有用处
    """

    # 从井底开始的高度， 用来计算井身结构
    Z = Symbol('Z')
    # 分段计算的步长， 含义为计算点到该段井底(上一个计算点)的高度
    step = Symbol('step')
    # 该段井底温度
    To = Symbol('To')
    # 井口温度
    Thead = Symbol('Thead')
    # 该段井底地层温度
    Tr = Symbol('Tr')
    # kg/m3
    density_of_oil = Symbol('ρ')
    # 定压比热容 J/(kg*K)
    Cp = Symbol('Cp')
    # 质量流量 kg/s
    W = Symbol('W')
    # 半稳态法得到的计算参数
    LR = Symbol('LR')
    # 地温梯度
    m = Symbol('m')
    # 重力加速度 m/s^2
    g = Symbol('g')
    # 包含了动能项和焦耳-汤姆逊系数（J--T）的计算参数
    fi = Symbol('∅')

    # 油管内径
    rti = Symbol('rti')

    # 导热系数
    Ke = Symbol('Ke')

    # 该微元段传热系数
    Ufe = Symbol('Ufe')

    # 无因此地层温度
    TD = Symbol('TD')
    # 油管内壁对流换热系数
    h = Symbol('h')

    # K 导热系数，下标 t-油管，a-环空，c-套管 cem-水泥环

    rto = Symbol('rto')

    Kt = Symbol('Kt')

    Ka = Symbol('Ka')
    rc1i = Symbol('rc1i')
    Kc = Symbol('Kc')
    rc1o = Symbol('rc1o')
    rc2i = Symbol('rc2i')
    rc2o = Symbol('rc2o')
    rc3i = Symbol('rc3i')
    rc3o = Symbol('rc3o')
    Kcem = Symbol('Kcem')
    tcem = Symbol('tcem')

    t = Symbol('t')

    # 地层热扩散系数
    ae = Symbol('ae')
