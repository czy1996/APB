from OilTemp import OilTemp
from AnnularTemp import AnnularTemp
from common import init_fig_axes

from sympy import init_printing, latex, pprint
import json
import pandas as pd


def plot(oil_temp: OilTemp, annular_temp: AnnularTemp):
    depth = oil_temp.params['well']['casing1']['depth']
    fig, axes = init_fig_axes(depth)

    oil_temp.plot(axes)
    annular_temp.plot(axes)

    fig.show()


def export_to_excel(oil_temp: OilTemp, annular_temp: AnnularTemp):
    data = {
        '地温': oil_temp.temps_earth_in_C,
        '油管流体': oil_temp.temps_in_C,
        '环空A': annular_temp.temps_A_in_C,
        '环空B': annular_temp.temps_B_in_C,
        '环空C': annular_temp.temps_C_in_C,
    }
    zindex = {
        '地温': oil_temp.zindex,
        '油管流体': oil_temp.zindex,
        '环空A': annular_temp.zindex_A,
        '环空B': annular_temp.zindex_B,
        '环空C': annular_temp.zindex_C,
    }
    depth = oil_temp.params['well']['casing1']['depth']

    writer = pd.ExcelWriter('计算结果.xlsx', engine='openpyxl')
    for sheet_name, array in data.items():
        df = pd.DataFrame({
            '深度': depth - zindex[sheet_name],
            sheet_name: array,
        })
        df.to_excel(writer,
                    sheet_name=sheet_name,
                    index=False)
    writer.save()


def main():
    init_printing(use_unicode=True)

    with open('data.json', 'r') as f:
        params = json.load(f)

    oil_temp = OilTemp(params)
    oil_temp.load_params()
    oil_temp.run()
    # oil_temp.plot()

    annular_temp = AnnularTemp(params, oil_temp.temps_in_K, oil_temp.zindex)
    annular_temp.run()

    # plot(oil_temp, annular_temp)
    export_to_excel(oil_temp, annular_temp)


if __name__ == '__main__':
    main()
