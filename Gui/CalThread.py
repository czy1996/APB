from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap

from Params import Params
from OilTemp import OilTemp
from AnnularTemp import AnnularTemp
from AnnularPressure import Pressure
from .ParamsMixin import ParamsError
from common import plot


class CalThread(QThread):
    signal_show_status_message = pyqtSignal(str)
    signal_show_err_message = pyqtSignal(str)
    signal_calc_temp_finished = pyqtSignal(OilTemp, AnnularTemp)
    signal_calc_pressure_finished = pyqtSignal(Pressure, Pressure)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        self.axes = parent.axes
        self.canvas = parent.canvas

    def show_status_message(self, message):
        self.signal_show_status_message.emit(message)

    def show_err_message(self, message):
        self.signal_show_err_message.emit(message)

    def _run_temp(self):
        self.show_status_message('正在计算温度')
        params = Params('temp.json').params
        self.params = params

        oil_temp = OilTemp(params)
        oil_temp.load_params()
        oil_temp.run()

        annular_temp = AnnularTemp(params,
                                   oil_temp.temps_in_K,
                                   oil_temp.zindex)
        annular_temp.run()

        self.oil_temp = oil_temp
        self.annular_temp = annular_temp

        self.show_status_message('温度计算完成')
        self.signal_calc_temp_finished.emit(oil_temp, annular_temp)

    def _run_pressure(self):
        self.show_status_message('正在计算压力')

        pressure_c = Pressure(self.params,
                              self.annular_temp.temps_C_in_C,
                              self.annular_temp.zindex_C)

        pressure_b = Pressure(self.params,
                              self.annular_temp.temps_B_in_C,
                              self.annular_temp.zindex_B)

        self.show_status_message('压力计算完成')

        self.signal_calc_pressure_finished.emit(pressure_b, pressure_c)

    def run(self):
        try:
            self._parent.read_params()
            self._parent.save_params()
            self._run_temp()
            self._run_pressure()
        except ParamsError as e:
            print('params error in thread')
            self.show_err_message(str(e))

        self.exit()
