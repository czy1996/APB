from OilTemp import OilTemp
from AnnularTemp import AnnularTemp

from sympy import init_printing, latex, pprint
import json


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


if __name__ == '__main__':
    main()
