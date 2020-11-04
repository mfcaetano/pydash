# -*- coding: utf-8 -*-
"""
@author: Marcos F. Caetano (mfcaetano@unb.br) 11/03/2020

@description: PyDash Project
"""
import json


class ConfigurationParser():
    __instance = None

    @staticmethod
    def get_instance():
        if ConfigurationParser.__instance is None:
            ConfigurationParser()
        return ConfigurationParser.__instance

    def __init__(self):
        if ConfigurationParser.__instance is not None:
            raise Exception('This class is a singleton!')
        else:
            with open('dash_client.json') as f:
                self.config_parameters = json.load(f)

            ConfigurationParser.__instance = self

    def get_parameter(self, key):
        return self.config_parameters[key]
