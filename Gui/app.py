import sys
import traceback

from Gui.mainWindow import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap

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
        self.setup()

    def setup(self):

        self.ui.buttonRun.clicked.connect(self.buttonRun_cb)
        self._load_params()

    def buttonRun_cb(self):
        self.ui.label_message.setText('button clicked')
        from .OilTempThread import OilTempThread
        self.worder = OilTempThread(self)
        self.worder.start()

    def _run_temp(self):
        params = Params('temp.json').params

        oil_temp = OilTemp(params)
        try:
            oil_temp.load_params()
        except Exception as e:
            traceback.print_exc(e)
            raise e

        oil_temp.run()
        annular_temp = AnnularTemp(params,
                                   oil_temp.temps_in_K,
                                   oil_temp.zindex)
        annular_temp.run()
        plot(oil_temp, annular_temp)
        self._load_image()

    def _load_image(self):
        p = QPixmap('temp.png')
        label = self.ui.label_temp_image
        label.setPixmap(p.scaled(
            label.width(),
            label.height(),
            QtCore.Qt.KeepAspectRatio,
        ))
