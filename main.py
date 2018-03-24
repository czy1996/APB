from OilTemp import OilTemp

from sympy import init_printing, latex
import json


def main():
    init_printing(use_unicode=True)

    with open('data.json', 'r') as f:
        params = json.load(f)

    oil_temp = OilTemp(params)

    # pprint(params)

    print(latex(oil_temp.expr))


if __name__ == '__main__':
    main()
