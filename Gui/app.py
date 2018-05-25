import sys

from Gui.mainWindow import Ui_MainWindow

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QMessageBox

import matplotlib as mpl
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from .ParamsMixin import ParamsMixin
from .CalThread import CalThread
from OilTemp import OilTemp
from AnnularTemp import AnnularTemp
from AnnularPressure import Pressure


def qt_debug():
    # qt 接管了 python 的报错，下面的操作是为了接管回来，方便 debug
    # Back up the reference to the exceptionhook
    sys._excepthook = sys.excepthook

    def my_exception_hook(exctype, value, traceback):
        # Print the error and traceback
        print(exctype, value, traceback)
        # Call the normal Exception hook after
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    # Set the exception hook to our wrapping function
    sys.excepthook = my_exception_hook


class APBError(Exception):
    pass


class MainWindow(QtWidgets.QMainWindow, ParamsMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup()

    def init_canvas(self):
        # 防止 pylab 画出来的图里汉字是方块
        mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
        mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
        label = self.ui.label_temp_image
        layout = QVBoxLayout()
        label.setLayout(layout)
        canvas = FigureCanvas(Figure())
        axes = canvas.figure.add_axes([0.15, 0.15, 0.8, 0.7])
        canvas.setParent(label)
        layout.addWidget(canvas)
        self.canvas = canvas
        self.axes = axes

    def setup(self):
        self.setFixedSize(920, 600)

        self.ui.buttonRun.clicked.connect(self.run_cal_thread)
        self.ui.buttonParamsLoad.clicked.connect(self.params_load)
        self.ui.buttonParamsSave.clicked.connect(self.params_save)
        self.ui.buttonResultSave.clicked.connect(self.result_save)
        self.ui.buttonResultSave.setDisabled(True)

        self.init_canvas()

    def run_cal_thread(self):
        # self.ui.label_message.setText('button clicked')
        self.ui.buttonRun.setDisabled(True)
        self.ui.buttonResultSave.setDisabled(True)
        self.worker = CalThread(self)
        self.worker.finished.connect(self.thread_terminated)
        self.worker.signal_show_status_message.connect(self.show_message)
        self.worker.signal_show_err_message.connect(self.err_message)
        self.worker.signal_calc_temp_finished.connect(self.calc_temp_finished)
        self.worker.signal_calc_pressure_finished.connect(self.calc_pressure_finished)
        self.worker.start()

    def thread_terminated(self):
        print('thread terminated')
        self.ui.buttonRun.setDisabled(False)
        print(self.worker, 'is running', self.worker.isRunning())

    def show_message(self, message):
        """
        在状态栏输出消息
        :return:
        """
        self.statusBar().showMessage(message)

    def err_message(self, message):
        print(message, type(message))
        b = QMessageBox.warning(self, '错误', message, QMessageBox.Ok)

    def plot_with_canvas(self):
        # set_ch()
        oil_temp, annular_temp = self.oil_temp, self.annular_temp
        depth = oil_temp.params['well']['casing1']['depth']

        axes = self.axes
        axes.clear()

        axes.set_ylim(top=0, bottom=depth)
        axes.xaxis.tick_top()  # 将 x 坐标移到上方
        axes.grid()

        oil_temp.plot(axes)
        annular_temp.plot(axes)

        axes.set_xlabel('温度 ℃')
        axes.set_ylabel('深度 m')
        axes.legend(loc='best', fontsize='small')
        self.canvas.draw()

    @QtCore.pyqtSlot(OilTemp, AnnularTemp)
    def calc_temp_finished(self, oil_temp, annular_temp):
        self.oil_temp, self.annular_temp = oil_temp, annular_temp
        self.plot_with_canvas()

    @QtCore.pyqtSlot(Pressure, Pressure)
    def calc_pressure_finished(self, pressure_b, pressure_c):
        self.pressure_b, self.pressure_c = pressure_b.pressure_delta, pressure_c.pressure_delta
        self.ui.label_d_pressure_C.setText(str(pressure_c.pressure_delta) + 'MPa')
        self.ui.label_d_pressure_B.setText(str(pressure_b.pressure_delta) + 'MPa')
        self.ui.buttonResultSave.setDisabled(False)

    def result_save(self):
        try:
            (oil_temp,
             annular_temp,
             pressure_b,
             pressure_c,
             ) = (
                self.oil_temp,
                self.annular_temp,
                self.pressure_b,
                self.pressure_c
            )

            file_name = QtWidgets.QFileDialog.getSaveFileName(self,
                                                              '选择保存文件',
                                                              filter='Excel files (*.xlsx)')

            self.export_to_excel(file_name[0])
            self.show_message('已保存计算结果{}'.format(file_name[0]))
        except AttributeError:
            # self.err_message('无法保存结果：未计算')
            raise APBError

    def export_to_excel(self, filename):
        oil_temp, annular_temp = self.oil_temp, self.annular_temp
        data = {
            '地温': oil_temp.temps_earth_in_C,
            '油管流体': oil_temp.temps_in_C,
            '环空A': annular_temp.temps_A_in_C,
            '环空B': annular_temp.temps_B_in_C,
            '环空C': annular_temp.temps_C_in_C,
        }
        zindex = {
            '地温': oil_temp.zindex,
            '油管流体': oil_temp.zindex,
            '环空A': annular_temp.zindex_A,
            '环空B': annular_temp.zindex_B,
            '环空C': annular_temp.zindex_C,
        }
        depth = oil_temp.params['well']['casing1']['depth']

        writer = pd.ExcelWriter(filename, engine='openpyxl')
        for sheet_name, array in data.items():
            df = pd.DataFrame({
                '深度': depth - zindex[sheet_name],
                '地温': oil_temp.temps_earth_in_C[-array.shape[0]:],
                sheet_name: array,
            })
            df.to_excel(writer,
                        sheet_name=sheet_name,
                        index=False)
        df = pd.DataFrame({
            '环空B MPa': [self.pressure_b],
            '环空C MPa': [self.pressure_c],
        }, index=['压力'])
        df.to_excel(writer,
                    sheet_name='压力',
                    )
        writer.save()
