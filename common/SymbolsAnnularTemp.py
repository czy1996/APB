from sympy import Symbol


class Symbols:
    """
    计算环空温度需要用到的符号
    """

    # 从井底开始的高度， 用来计算井身结构
    Z = Symbol('Z')

    A = Symbol('A')  # 计算参数
    B = Symbol('B')  # 计算参数

    T0 = Symbol('T0')  # 初始温度
    Tf = Symbol('Tf')  # 油管液体温度

    M = Symbol('M')  # 该段环空液体质量
    CpA = Symbol('CpA')  # 环空液体比热容

    Te = Symbol('Te')  # 该深度地层温度
    Ut = Symbol('Ut')  # 从油管流体到该微段环空的传热系数
    LR = Symbol('LR')  # 计算参数
    Ue = Symbol('Ue')  # 从环空到水泥环边界的传热系数
    density_annular = Symbol('density')

    step = Symbol('step')

    # 地温梯度
    m = Symbol('m')

    Thead = Symbol('Thead')

    # 油管内径
    rti = Symbol('rti')

    # 导热系数
    Ke = Symbol('Ke')

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

    # 无因此地层温度
    TD = Symbol('TD')
