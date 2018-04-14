from OilTemp import OilTemp

from sympy import init_printing, latex, pprint
import json


def main():
    init_printing(use_unicode=True)

    with open('data.json', 'r') as f:
        params = json.load(f)

    oil_temp = OilTemp(params)
    oil_temp.load_params()
    oil_temp.run()

    # pprint(params)

    # pprint(oil_temp.expr)


if __name__ == '__main__':
    main()
