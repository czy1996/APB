import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from Params import Params
from OilTemp import OilTemp
from AnnularTemp import AnnularTemp
from AnnularPressure import Pressure


def temp_dis_vary_time():
    params = Params()
    depth = params.params['well']['casing1']['depth']

    p = params.params
    # params.set_production_rate(200)
    oil_temp = OilTemp(p)
    oil_temp.load_params()
    oil_temp.run()
    # oil_temp.plot()
    print(oil_temp.params['etc']['t'], oil_temp.temps_in_C[-1])
    annular_temp = AnnularTemp(p, oil_temp.temps_in_K, oil_temp.zindex)
    annular_temp.run()
    # annular_temp.plot()

    t = np.concatenate((np.arange(0, 100, 10), np.arange(100, 600, 50)))
    # t = np.arange(0, 100, 1 / 24)
    t = [0, 1, 5, 20, 100, 200]
    r = []
    zindex = None
    for i in t:
        params.set_time_day(i)
        ot = OilTemp(params.params)
        # print(params.params['thermal']['W'])
        ot.load_params()
        ot.run()
        at = AnnularTemp(params.params, ot.temps_in_K, ot.zindex)
        at.run()
        # r
        r.append(ot.temps_in_C)
        zindex = ot.zindex
    # fig, ax = plt.subplots(1, 1)
    # # ax.set_yticks(np.arange(50, 100, 10))
    # ax.plot(t, r)
    # fig.show()
    #
    export_to_excel_time(depth - zindex, r)


def pressure_vary_time():
    params = Params()
    depth = params.params['well']['casing1']['depth']

    p = params.params
    # params.set_production_rate(200)
    oil_temp = OilTemp(p)
    oil_temp.load_params()
    oil_temp.run()
    # oil_temp.plot()
    print(oil_temp.params['etc']['t'], oil_temp.temps_in_C[-1])
    annular_temp = AnnularTemp(p, oil_temp.temps_in_K, oil_temp.zindex)
    annular_temp.run()
    # annular_temp.plot()

    t = np.concatenate((np.arange(0, 100, 10), np.arange(100, 600, 50)))
    # t = np.arange(0, 100, 1 / 24)
    t = [0, 1, 5, 20, 100, 200]
    t = np.arange(0, 25, 1)
    r_c = []
    r_b = []
    for i in t:
        params.set_time_day(i / 24)
        ot = OilTemp(params.params)
        # print(params.params['thermal']['W'])
        ot.load_params()
        ot.run()
        at = AnnularTemp(params.params, ot.temps_in_K, ot.zindex)
        at.run()
        p_b = Pressure(params.params, at.temps_B_in_C, at.zindex_B)
        p_c = Pressure(params.params, at.temps_C_in_C, at.zindex_C)

        # r
        r_b.append(p_b.pressure_delta)
        r_c.append(p_c.pressure_delta)
    # fig, ax = plt.subplots(1, 1)
    # # ax.set_yticks(np.arange(50, 100, 10))
    # ax.plot(t, r)
    # fig.show()
    #
    export_to_excel(t, r_b, r_c)


def pressure_vary_production():
    params = Params()
    depth = params.params['well']['casing1']['depth']

    p = params.params
    # params.set_production_rate(200)
    oil_temp = OilTemp(p)
    oil_temp.load_params()
    oil_temp.run()
    # oil_temp.plot()
    print(oil_temp.params['etc']['t'], oil_temp.temps_in_C[-1])
    annular_temp = AnnularTemp(p, oil_temp.temps_in_K, oil_temp.zindex)
    annular_temp.run()
    # annular_temp.plot()

    w = [10, 50, 100, 200, 400]
    r_c = []
    r_b = []
    for i in w:
        params.set_production_rate(i)
        ot = OilTemp(params.params)
        # print(params.params['thermal']['W'])
        ot.load_params()
        ot.run()
        at = AnnularTemp(params.params, ot.temps_in_K, ot.zindex)
        at.run()
        p_b = Pressure(params.params, at.temps_B_in_C, at.zindex_B)
        p_c = Pressure(params.params, at.temps_C_in_C, at.zindex_C)

        # r
        r_b.append(p_b.pressure_delta)
        r_c.append(p_c.pressure_delta)
    # fig, ax = plt.subplots(1, 1)
    # # ax.set_yticks(np.arange(50, 100, 10))
    # ax.plot(t, r)
    # fig.show()
    #
    export_to_excel_rate_pressure(w, r_b, r_c)


def surface_temp_vary_production():
    params = Params()
    depth = params.params['well']['casing1']['depth']

    p = params.params
    # params.set_production_rate(200)
    oil_temp = OilTemp(p)
    oil_temp.load_params()
    oil_temp.run()
    # oil_temp.plot()
    print(oil_temp.params['etc']['t'], oil_temp.temps_in_C[-1])
    annular_temp = AnnularTemp(p, oil_temp.temps_in_K, oil_temp.zindex)
    annular_temp.run()
    # annular_temp.plot()

    w = np.arange(0, 500, 25)
    t_c = []
    t_b = []
    r_p_c = []
    r_p_b = []
    for i in w:
        params.set_production_rate(i)
        ot = OilTemp(params.params)
        # print(params.params['thermal']['W'])
        ot.load_params()
        ot.run()
        at = AnnularTemp(params.params, ot.temps_in_K, ot.zindex)
        at.run()
        p_b = Pressure(params.params, at.temps_B_in_C, at.zindex_B)
        p_c = Pressure(params.params, at.temps_C_in_C, at.zindex_C)

        # r
        t_b.append(at.temps_B_in_C[-1])
        t_c.append(at.temps_C_in_C[-1])
        r_p_b.append(p_b.pressure_delta)
        r_p_c.append(p_c.pressure_delta)
    # fig, ax = plt.subplots(1, 1)
    # # ax.set_yticks(np.arange(50, 100, 10))
    # ax.plot(t, r)
    # fig.show()
    #
    export_to_excel_pressure_temp(w, t_b, t_c, r_p_b, r_p_c)


def export_to_excel_pressure_temp(w, t_b, t_c, r_p_b, r_p_c):
    writer = pd.ExcelWriter('井口温度随产量变化.xlsx', engine='openpyxl')
    df = pd.DataFrame({
        '产量': w,
        '环空B压力': r_p_b,
        '环空C压力': r_p_c,
        '环空B温度': t_b,
        '环空C温度': t_c,

    })
    df.to_excel(writer,
                index=False)
    writer.save()


def export_to_excel_rate_temp(w, r_b, r_c):
    writer = pd.ExcelWriter('井口温度随产量变化.xlsx', engine='openpyxl')
    df = pd.DataFrame({
        '产量': w,
        '环空B': r_b,
        '环空C': r_c,
    })
    df.to_excel(writer,
                index=False)
    writer.save()


def export_to_excel_rate_pressure(w, r_b, r_c):
    writer = pd.ExcelWriter('环空压力随产量变化.xlsx', engine='openpyxl')
    df = pd.DataFrame({
        '产量': w,
        'b': r_b,
        'c': r_c,
    })
    df.to_excel(writer,
                index=False)
    writer.save()


def export_to_excel(t, r_b, r_c):
    writer = pd.ExcelWriter('环空压力随时间变化.xlsx', engine='openpyxl')
    df = pd.DataFrame({
        '时间': t,
        'b': r_b,
        'c': r_c,
    })
    df.to_excel(writer,
                index=False)
    writer.save()


def export_to_excel_time(depth, results):
    writer = pd.ExcelWriter('油管温度随时间变化.xlsx', engine='openpyxl')
    df = pd.DataFrame({
        'depth': depth,
        '0': results[0],
        '1': results[1],
        '5': results[2],
        '20': results[3],
        '100': results[4],
        '200': results[5],

    })
    df.to_excel(writer,
                index=False)
    writer.save()


def main():
    surface_temp_vary_production()


if __name__ == '__main__':
    main()
