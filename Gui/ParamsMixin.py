import os
import json


def _convert_to_digit(d: dict):
    for k, v in d.items():
        if isinstance(v, dict):
            _convert_to_digit(v)
        elif isinstance(v, str):
            # print('v', v)
            d[k] = float(v)


class ParamsMixin:
    default_params_file = 'temp.json'

    def _load_params(self):
        if os.path.isfile(self.default_params_file):
            with open(self.default_params_file) as f:
                params = json.load(f)

            ui = self.ui

            ui.input_depth1.setText(str(params['well']['casing1']['depth']))
            ui.input_dc1o.setText(str(params['well']['casing1']['do']))
            ui.input_dc1i.setText(str(params['well']['casing1']['di']))
            ui.input_toc1.setText(str(params['well']['casing1']['toc']))

            ui.input_depth2.setText(str(params['well']['casing2']['depth']))
            ui.input_dc2o.setText(str(params['well']['casing2']['do']))
            ui.input_dc2i.setText(str(params['well']['casing2']['di']))
            ui.input_toc2.setText(str(params['well']['casing2']['toc']))

            ui.input_depth3.setText(str(params['well']['casing3']['depth']))
            ui.input_dc3o.setText(str(params['well']['casing3']['do']))
            ui.input_dc3i.setText(str(params['well']['casing3']['di']))
            ui.input_toc3.setText(str(params['well']['casing3']['toc']))

            ui.input_dto.setText(str(params['well']['tubing']['do']))
            ui.input_dti.setText(str(params['well']['tubing']['di']))

            ui.input_tcem.setText(str(params['well']['etc']['tcem']))
            ui.input_m.setText(str(params['thermal']['m']))
            ui.input_W.setText(str(params['thermal']['W']))
            ui.input_cp_oil.setText(str(params['thermal']['Cp_oil']))
            ui.input_cp_annular.setText(str(params['thermal']['Cp_annular']))
            ui.input_h.setText(str(params['thermal']['h']))
            ui.input_Kc.setText(str(params['thermal']['Kc']))
            ui.input_Ka.setText(str(params['thermal']['Ka']))
            ui.input_Kcem.setText(str(params['thermal']['Kcem']))
            ui.input_Kt.setText(str(params['thermal']['Kt']))
            ui.input_Ke.setText(str(params['thermal']['Ke']))
            ui.input_density_oil.setText(str(params['thermal']['density_oil']))
            ui.input_density_annular.setText(str(params['thermal']['density_annular']))
            ui.input_ae.setText(str(params['thermal']['ae']))
            ui.input_temp_surface.setText(str(params['thermal']['temp_surface']))
            ui.input_t.setText(str(params['etc']['t']))

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
