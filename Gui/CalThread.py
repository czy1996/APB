from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import matplotlib as mpl

from Params import Params
from OilTemp import OilTemp
from AnnularTemp import AnnularTemp
from AnnularPressure import Pressure
from common import plot


class CalThread(QThread):
    show_status_message = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        self.init_canvas()

    def show_message(self, message):
        self.show_status_message.emit(message)

    def _run_temp(self):
        self.show_message('正在计算温度')
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

        self.show_message('温度计算完成')
        self.plot_with_canvas()
        # self.parent().ui.label_message.setText('温度计算完成')

    def _draw_temp_plot(self):
        plot(self.oil_temp, self.annular_temp)
        self._load_image()

    def plot_with_canvas(self):
        # set_ch()
        oil_temp, annular_temp = self.oil_temp, self.annular_temp
        depth = oil_temp.params['well']['casing1']['depth']

        axes = self.axes

        axes.set_ylim(top=0, bottom=depth)
        axes.xaxis.tick_top()  # 将 x 坐标移到上方
        axes.grid()

        oil_temp.plot(axes)
        annular_temp.plot(axes)

        axes.legend(loc='best', fontsize='x-small')
        self.canvas.draw()

    def init_canvas(self):
        # 防止 pylab 画出来的图里汉字是方块
        mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
        mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
        label = self._parent.ui.label_temp_image
        layout = QVBoxLayout()
        label.setLayout(layout)
        w, h = label.width(), label.height()
        canvas = FigureCanvas(Figure())
        axes = canvas.figure.add_axes([0.15, 0.1, 0.7, 0.8])
        axes.set_xlabel('温度 ℃')
        axes.set_ylabel('深度 m')
        canvas.setParent(label)
        layout.addWidget(canvas)
        self.canvas = canvas
        self.axes = axes

    def _run_pressure(self):
        self.show_message('正在计算压力')

        pressure_c = Pressure(self.params,
                              self.annular_temp.temps_C_in_C,
                              self.annular_temp.zindex_C)

        pressure_b = Pressure(self.params,
                              self.annular_temp.temps_B_in_C,
                              self.annular_temp.zindex_B)

        self.parent().ui.label_d_pressure_C.setText(str(pressure_c.pressure_delta) + 'MPa')

        self.parent().ui.label_d_pressure_B.setText(str(pressure_b.pressure_delta) + 'MPa')

        self.show_message('压力计算完成')

    def _load_image(self):
        """
        废弃
        :return:
        """
        p = QPixmap('temp.png')
        label = self._parent.ui.label_temp_image
        print(label.width(), label.height())
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
