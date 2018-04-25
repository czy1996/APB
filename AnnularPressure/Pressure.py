import numpy as np

from .Density import Density


def float_to_int(array):
    return np.round(array).astype(np.int32)


class Pressure:
    def __init__(self, params, temps, zindex):
        self._density = Density()
        self.params = params
        self.temps = temps
        self.zindex = zindex
        self.depth = self.params['well']['casing1']['depth'] - self.zindex
        self.temps_earth = self._cal_temps_earth()
        self.liquid_pressure = self._cal_liquid_pressure()
        self.number_of_steps = 10

    def _cal_temps_earth(self):
        temp_surface = self.params['thermal']['temp_surface']
        temps_earth = temp_surface + self.params['thermal']['m'] * self.depth + 273.15  # params 中的井口温度单位被转换成了 K
        # print('temps earth float', temps_earth)
        temps_earth = float_to_int(temps_earth)
        # print('zindex', self.zindex)
        # print('depth', self.depth)
        # print('temps earth', temps_earth)
        return temps_earth

    def _cal_liquid_pressure(self):
        """
        静液柱压力，初始压力
        :return:
        """
        liquid_pressure = 1000 * 9.8 * self.depth * 0.000001
        return float_to_int(liquid_pressure)

    def delta_p(self):
        step = 0.01
        coefficient = 0
        dt = (self.temps - self.temps_earth) * step
        # 从地层温度开始算
        _temps = self.temps_earth.copy()
        _pressure_int = self.liquid_pressure.copy()
        _pressure_float = _pressure_int.astype(np.float32)
        while (_temps < self.temps).all():
            # 循环的终止条件是某个微端的温度达到了环空温度
            print('temps', _temps)
            dp = self._delta_p(dt, _temps, _pressure_int)

            # 在地层温度和环空温度之间取值
            _temps = self.temps_earth * (1 - coefficient) + self.temps * coefficient
            _temps = float_to_int(_temps)
            coefficient += step  # 增加 0.01
            _pressure_float += dp
            _pressure_int = float_to_int(_pressure_float)
            print('dp', dp)

        b = _temps < self.temps
        return _pressure_float - self.liquid_pressure

    def _delta_p(self, dt, temp, pressure):
        _p = (np.sum(dt * self._density.alpha(temp, pressure)) /
              np.sum(self._density.k(temp, pressure)))
        return _p
