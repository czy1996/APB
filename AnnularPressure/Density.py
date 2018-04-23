import numpy as np


class Density:
    def __init__(self):
        self._density = None

        # 温度和压力取值范围
        self.max_temp = 200
        self.max_pressure = 200

    def _run(self):
        len_temp = self.max_temp + 1
        len_pressure = self.max_pressure + 1
        self._density = np.empty((len_temp, len_pressure), dtype=float)
        for i in range(len_temp):
            for j in range(len_pressure):
                self._density[i][j] = self._density_of_water(i, j)

    def get(self, temp, pressure):
        _density = self._density
        if _density is None:
            self._run()
        return _density[temp][pressure]

    def _density_data_points(self):
        """
        用来插值的数据点
        :return:
        """
        return np.array([
            [1000.3, 1043.6],
            [996.96, 1037.2],
            [989.82, 1028.9],
            [979.93, 1019],
            [967.81, 1007.8],
            [937.87, 981.82],
            [890.39, 943.51],
        ])

    def _temp_data_array(self):
        return np.ma.array([
            7, 27, 47, 67, 87, 127, 177,
        ])

    def _pressure_array(self):
        return np.ma.array([
            1, 100,
        ])

    def _li_T(self, i, T):
        """
        li(T)
        :param i: 公式上从 1 开始，这里为了方便从 0 开始
        :param T:
        :return:
        """
        temp = self._temp_data_array()
        ti = temp[i]
        temp[i] = np.ma.masked  # 第 i 个 不参与计算
        _prod_ele = (T - temp) / (ti - temp)
        return np.prod(_prod_ele)

    def _lj_P(self, j, P):
        """
        lj(P)
        :param j: 公式上从 1 开始，这里为了方便从 0 开始
        :param P:
        :return:
        TODO 利用广播提高效率？
        """
        pressure = self._pressure_array()
        pj = pressure[j]
        pressure[j] = np.ma.masked
        _prod_ele = (P - pressure) / (pj - pressure)
        return np.prod(_prod_ele)

    def _density_of_water(self, temp, pressure):
        print('_density of water', temp, pressure)
        _density = self._density_data_points()
        _temp = self._temp_data_array()
        _pressure = self._pressure_array()
        r = 0
        for i in range(len(_temp)):
            for j in range(len(_pressure)):
                r += _density[i][j] * self._li_T(i, temp) * self._lj_P(j, pressure)

        return r


def test():
    density = Density()
    t = density._density_of_water(177, 10)
    t = density.get(177, 10)
    print(t)
