from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QPixmap

from Params import Params
from OilTemp import OilTemp
from AnnularTemp import AnnularTemp
from common import plot


class OilTempThread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent

    def _run_temp(self):
        self.parent().ui.label_message.setText('正在计算温度')
        params = Params('temp.json').params

        oil_temp = OilTemp(params)
        oil_temp.load_params()

        oil_temp.run()
        annular_temp = AnnularTemp(params,
                                   oil_temp.temps_in_K,
                                   oil_temp.zindex)
        annular_temp.run()
        plot(oil_temp, annular_temp)
        self._load_image()
        self.parent().ui.label_message.setText('温度计算完成')


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
        self.exit()
