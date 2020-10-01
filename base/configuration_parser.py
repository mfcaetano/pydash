from base.singleton import Singleton
import json

class Configuration_Parser():
    __instance = None

    @staticmethod
    def get_instance():
        if Configuration_Parser.__instance == None:
            Configuration_Parser()
        return Configuration_Parser.__instance

    def __init__(self):
        if Configuration_Parser.__instance != None:
            raise Exception('This class is a singleton!')
        else:
            with open('dash_client.json') as f:
                self.config_parameters = json.load(f)

            Configuration_Parser.__instance = self

    def get_parameter(self, key):
        return self.config_parameters[key]
