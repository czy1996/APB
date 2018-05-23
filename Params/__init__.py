"""
处理参数的类
"""
import json


class Params:
    def __init__(self, params_file='data.json', params_dict=None):
        self.params_file = params_file

        # print('params dict', params_dict)
        if params_dict is None:
            self.read_params_from_file()

            self.params_map = {
                'depth1': self.params['well']['casing1']['depth'],
                'depth2': self.params['well']['casing2']['depth'],
                'depth3': self.params['well']['casing3']['depth'],
                'Thead': self.params['thermal']['temp_surface'],
                'density_of_oil': self.params['thermal']['density_oil'],
                'Cp_oil': self.params['thermal']['Cp_oil'],
                'W': self.params['thermal']['W'],
                'm': self.params['thermal']['m'],
                'Ke': self.params['thermal']['Ke'],

            }

        else:
            self.params = params_dict

        self.convert_params()

    def read_params_from_file(self):
        with open(self.params_file) as f:
            self.params = json.load(f)

    def inch_to_meter(self):
        pass

    def convert_params(self):
        self.params['well']['etc']['tcem'] *= 0.001

        self.params['well']['casing1']['ro'] = self.params['well']['casing1']['do'] * 0.001 / 2
        self.params['well']['casing1']['ri'] = self.params['well']['casing1']['di'] * 0.001 / 2
        self.params['well']['casing2']['ro'] = self.params['well']['casing2']['do'] * 0.001 / 2
        self.params['well']['casing2']['ri'] = self.params['well']['casing2']['di'] * 0.001 / 2
        self.params['well']['casing3']['ro'] = self.params['well']['casing3']['do'] * 0.001 / 2
        self.params['well']['casing3']['ri'] = self.params['well']['casing3']['di'] * 0.001 / 2
        self.params['well']['tubing']['ro'] = self.params['well']['tubing']['do'] * 0.001 / 2
        self.params['well']['tubing']['ri'] = self.params['well']['tubing']['di'] * 0.001 / 2

        self.params['thermal']['W'] = self.params['thermal']['W'] * 1000 / 24 / 3600

        self.params['etc']['t'] *= 24 * 3600

        self.params['thermal']['temp_surface'] -= 273.15

    def __getattr__(self, item):
        """
        这块没有做完也没有用处，重构不是目前的首要任务
        :param item:
        :return:
        """
        if item not in self.params:
            raise AttributeError('No such params: {}'.format(item))

    def set_time_day(self, time):
        self.params['etc']['t'] = 24 * 3600 * time

    def set_production_rate(self, w):
        self.params['thermal']['W'] = w * 1000 / 24 / 3600
