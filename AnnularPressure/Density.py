import numpy as np


class Density:
    def __init__(self):
        self._density = None
        self.default_filename = 'density.npy'

        # 温度和压力取值范围
        self.max_temp = 200
        self.max_pressure = 200

    def _run(self):
        len_temp = self.max_temp + 1
        len_pressure = self.max_pressure + 1
        self._density = np.empty((len_temp, len_pressure), dtype=float)
        for i in range(len_temp):
            for j in range(len_pressure):
                self._density[i, j] = self._density_of_water(i, j)

    def _save(self):
        np.save(self.default_filename, self._density)

    def _load(self):
        try:
            self._density = np.load(self.default_filename)
        except FileNotFoundError:
            print("Density File Not Found, Cal Now")
            self._density = None

    def _cached_get(self, temp, pressure):
        self._load()

        if self._density is None:
            self._run()
            self._save()
        if isinstance(temp, np.ndarray):
            pass
        # print(temp)
        # print(pressure)
        # print('temp < 201', (temp < 201).all(), (temp < 201).any())
        return self._density[temp, pressure]

    def _real_time_get(self, temp, pressure):
        r = np.empty_like(temp)
        if isinstance(temp, np.ndarray) and isinstance(pressure, np.ndarray):
            for i, t in np.ndenumerate(temp):
                r[i] = self._density_of_water(t, pressure[i])
            return r
        else:
            return self._density_of_water(temp, pressure)

    def get(self, temp, pressure):
        # print('density', temp, pressure)
        d = self._cached_get(temp, pressure)
        # d = self._real_time_get(temp, pressure)
        return d

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

    @property
    def _temp_data_array(self):
        return np.ma.array([
            7, 27, 47, 67, 87, 127, 177,
        ])

    @property
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
        temp = self._temp_data_array
        ti = temp[i]
        temp[i] = np.ma.masked  # 第 i 个 不参与计算
        _prod_ele = (T - temp) / (ti - temp)
        return np.prod(_prod_ele)

    def _li_T_array(self, T):
        a = np.empty_like(self._temp_data_array)
        for i in range(len(a)):
            a[i] = self._li_T(i, T)
        return a

    def _lj_P(self, j, P):
        """
        lj(P)
        :param j: 公式上从 1 开始，这里为了方便从 0 开始
        :param P:
        :return:
        TODO 利用广播提高效率？
        """
        pressure = self._pressure_array
        pj = pressure[j]
        pressure[j] = np.ma.masked
        _prod_ele = (P - pressure) / (pj - pressure)
        return np.prod(_prod_ele)

    def _density_of_water(self, temp, pressure):
        print('_density of water', temp, pressure)
        _density = self._density_data_points()
        _temp = self._temp_data_array
        _pressure = self._pressure_array
        r = 0
        # for i in range(len(_temp)):
        #     for j in range(len(_pressure)):
        #         r += _density[i][j] * self._li_T(i, temp) * self._lj_P(j, pressure)

        for (i, j), d in np.ndenumerate(_density):
            r += d * self._li_T(i, temp) * self._lj_P(j, pressure)

        return r

    def _der_density_over_der_temp(self, temp, pressure):
        dt = 1
        if (temp + 1 <= self.max_temp).any():
            # print('in _der temp', temp + 1)
            return self.get(temp + 1, pressure) - self.get(temp, pressure)
        else:
            return self.get(temp, pressure) - self.get(temp - 1, pressure)

    def _der_density_over_der_pressure(self, temp, pressure):
        if (pressure + 1 <= self.max_temp).any():
            return self.get(temp, pressure + 1) - self.get(temp, pressure)
        else:
            return self.get(temp, pressure) - self.get(temp, pressure - 1)

    def alpha(self, temp, pressure):
        return -(1 / self.get(temp, pressure)) * self._der_density_over_der_temp(temp, pressure)

    def k(self, temp, pressure):
        return 1 / self.get(temp, pressure) * self._der_density_over_der_pressure(temp, pressure)


def test():
    density = Density()
    t = density._density_of_water(177, 10)
    t = density.get(150, 10)
    print(t)
    print(density._der_density_over_der_pressure(156, 10))
    print(density._der_density_over_der_temp(156, 10))
