from PyQt5.QtCore import QThread


class OilTempThread(QThread):
    def __init__(self, parent=None):
        super().__init__()
        self._parent = parent

    def run(self):
        self._parent._read_params()
        self._parent._save_params()
        self._parent._run_temp()
