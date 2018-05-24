import sys

from Gui.mainWindow import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QMessageBox

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import matplotlib as mpl
from .ParamsMixin import ParamsMixin, ParamsError
from .CalThread import CalThread


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


class MainWindow(QtWidgets.QMainWindow, ParamsMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup()

    def init_canvas(self):
        # 防止 pylab 画出来的图里汉字是方块
        mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
        mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
        label = self.ui.label_temp_image
        layout = QVBoxLayout()
        label.setLayout(layout)
        canvas = FigureCanvas(Figure())
        axes = canvas.figure.add_axes([0.15, 0.1, 0.7, 0.8])
        axes.set_xlabel('温度 ℃')
        axes.set_ylabel('深度 m')
        canvas.setParent(label)
        layout.addWidget(canvas)
        self.canvas = canvas
        self.axes = axes

    def setup(self):
        self.setFixedSize(920, 600)

        self.ui.buttonRun.clicked.connect(self.buttonRun_cb)
        self.ui.buttonParamsLoad.clicked.connect(self.load_params_from_file)
        self.ui.buttonParamsSave.clicked.connect(self.save_params_to_file)

        self.init_canvas()

    def buttonRun_cb(self):
        # self.ui.label_message.setText('button clicked')
        self.ui.buttonRun.setDisabled(True)
        self.worker = CalThread(self)
        self.worker.finished.connect(self.thread_terminated)
        self.worker.signal_show_status_message.connect(self.show_message)
        self.worker.signal_show_err_message.connect(self.err_message)
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
