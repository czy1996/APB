from PyQt5 import QtCore, QtWidgets
import pandas as pd

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

            self._export_to_excel(file_name[0])
            self.show_message('已保存计算结果{}'.format(file_name[0]))
        except AttributeError:
            self.err_message('无法保存结果：未计算')
        except PermissionError:
            self.err_message('无法保存结果：文件可能被占用')
        finally:
            self.ui.buttonResultSave.setDisabled(False)

    @QtCore.pyqtSlot()
    def thread_terminated(self):
        print('thread terminated')
        self.ui.buttonRun.setDisabled(False)
        print(self.worker, 'is running', self.worker.isRunning())

    def _export_to_excel(self, filename):
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
