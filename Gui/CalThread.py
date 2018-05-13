from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap

from Params import Params
from OilTemp import OilTemp
from AnnularTemp import AnnularTemp
from AnnularPressure import Pressure
from common import plot


class CalThread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent

    def _run_temp(self):
        self.parent().ui.label_message.setText('正在计算温度')
        params = Params('temp.json').params
        self.params = params

        oil_temp = OilTemp(params)
        oil_temp.load_params()

        oil_temp.run()
        annular_temp = AnnularTemp(params,
                                   oil_temp.temps_in_K,
                                   oil_temp.zindex)
        annular_temp.run()
        plot(oil_temp, annular_temp)
        self._load_image()

        self.oil_temp = oil_temp
        self.annular_temp = annular_temp
        self.parent().ui.label_message.setText('温度计算完成')

    def _run_pressure(self):
        self.parent().ui.label_message.setText('正在计算压力')

        pressure_c = Pressure(self.params,
                              self.annular_temp.temps_C_in_C,
                              self.annular_temp.zindex_C)
        print('delta p c', pressure_c.delta_p())
        self.parent().ui.label_pressure_C.setText(str(pressure_c.delta_p()) + 'MPa')

        pressure_b = Pressure(self.params,
                              self.annular_temp.temps_B_in_C,
                              self.annular_temp.zindex_B)
        self.parent().ui.label_pressure_B.setText(str(pressure_b.delta_p()) + 'MPa')

        self.parent().ui.label_message.setText('压力计算完成')


    def _load_image(self):
        p = QPixmap('temp.png')
        label = self._parent.ui.label_temp_image
        label.setPixmap(p.scaled(
            label.width(),
            label.height(),
            QtCore.Qt.KeepAspectRatio,
        ))

    def run(self):
        self._parent._read_params()
        self._parent._save_params()
        self._run_temp()
        self._run_pressure()
        self.exit()
