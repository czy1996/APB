import sys
from PyQt5 import QtWidgets

from Gui.app import MainWindow, qt_debug

if __name__ == '__main__':
    qt_debug()
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
