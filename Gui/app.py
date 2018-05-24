import sys
import traceback

from Gui.mainWindow import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore

from AnnularTemp import AnnularTemp
from OilTemp import OilTemp
from common import plot
from Params import Params
from .ParamsMixin import ParamsMixin


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
        self.setFixedSize(920, 600)
        self.setup()

    def setup(self):
        self.ui.buttonRun.clicked.connect(self.buttonRun_cb)
        self._load_params()

    def buttonRun_cb(self):
        # self.ui.label_message.setText('button clicked')
        from .CalThread import CalThread
        self.worker = CalThread(self)
        self.worker.finished.connect(self.watch_thread)
        self.worker.show_status_message.connect(self.show_message)
        self.worker.start()

    def watch_thread(self):
        print('thread terminated')
        print(self.worker, 'is running', self.worker.isRunning())

    def show_message(self, message):
        """
        在状态栏输出消息
        :return:
        """
        self.statusBar().showMessage(message)
