import sys
import json
import traceback

from mainWindow import Ui_MainWindow
from PyQt5 import QtWidgets

from AnnularTemp import AnnularTemp
from OilTemp import OilTemp
from common import plot
from Params import Params

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


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup()

    def setup(self):
        self.ui.buttonRun.clicked.connect(self.buttonRun_cb)

    def buttonRun_cb(self):
        self.ui.label_message.setText('button clicked')
        self._read_params()
        self._save_params()
        self._run_temp()

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

    def _read_params(self):
        ui = self.ui
        params = {
            'well': {
                'number_of_casing': 3,
                'casing1': {
                    'depth': ui.input_depth1.text(),
                    'do': ui.input_dc1o.text(),
                    'di': ui.input_dc1i.text(),
                    'toc': ui.input_toc1.text(),
                },
                'casing2': {
                    'depth': ui.input_depth2.text(),
                    'do': ui.input_dc2o.text(),
                    'di': ui.input_dc2i.text(),
                    'toc': ui.input_toc2.text(),
                },
                'casing3': {
                    'depth': ui.input_depth3.text(),
                    'do': ui.input_dc3o.text(),
                    'di': ui.input_dc3i.text(),
                    'toc': ui.input_toc3.text(),
                },
                'tubing': {
                    'do': ui.input_dto.text(),
                    'di': ui.input_dti.text(),
                },
                'etc': {
                    'tcem': ui.input_tcem.text(),
                }
            },
            'thermal': {
                'm': ui.input_m.text(),
                'W': ui.input_W.text(),
                'Cp_oil': ui.input_cp_oil.text(),
                'Cp_annular': ui.input_cp_annular.text(),
                'h': ui.input_h.text(),
                'Kc': ui.input_Kc.text(),
                'Ka': ui.input_Ka.text(),
                'Kcem': ui.input_Kcem.text(),
                'Kt': ui.input_Kt.text(),
                'Ke': ui.input_Ke.text(),
                'density_oil': ui.input_density_oil.text(),
                'density_annular': ui.input_density_annular.text(),
                'ae': ui.input_ae.text(),
                'temp_surface': ui.input_temp_surface.text(),
            },
            'etc': {
                't': ui.input_t.text(),
            }
        }

        _convert_to_digit(params)

        self.params = params

    def _save_params(self, filename='temp.json'):
        with open(filename, 'w') as f:
            json.dump(self.params, f, indent=4)


def _convert_to_digit(d: dict):
    for k, v in d.items():
        if isinstance(v, dict):
            _convert_to_digit(v)
        elif isinstance(v, str):
            # print('v', v)
            d[k] = float(v)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
