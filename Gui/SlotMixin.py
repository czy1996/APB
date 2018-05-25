from PyQt5 import QtCore, QtWidgets

from OilTemp import OilTemp
from AnnularPressure import Pressure
from AnnularTemp import AnnularTemp


class SlotMixin:
    """
    只用于响应 signal 的槽函数
    """
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

    @QtCore.pyqtSlot()
    def result_save(self):
        self.ui.buttonResultSave.setDisabled(True)
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
            self.err_message('无法保存结果：未计算')
        except PermissionError:
            self.err_message('无法保存结果：文件可能被占用')
        finally:
            self.ui.buttonResultSave.setDisabled(False)
