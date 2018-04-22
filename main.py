from OilTemp import OilTemp
from AnnularTemp import AnnularTemp
from common import init_fig_axes

from sympy import init_printing, latex, pprint
import json


def plot(oil_temp: OilTemp, annular_temp: AnnularTemp):
    fig, axes = init_fig_axes(oil_temp.params['well']['casing1']['depth'])

    oil_temp.plot(axes)
    annular_temp.plot(axes)

    fig.show()


def main():
    init_printing(use_unicode=True)

    with open('data.json', 'r') as f:
        params = json.load(f)

    oil_temp = OilTemp(params)
    oil_temp.load_params()
    oil_temp.run()
    # oil_temp.plot()

    annular_temp = AnnularTemp(params, oil_temp.temps_in_K, oil_temp.Z_index)
    annular_temp.run()

    plot(oil_temp, annular_temp)


if __name__ == '__main__':
    main()
