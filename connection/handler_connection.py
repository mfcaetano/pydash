
from base.simple_module import Simple_Module

"""
The Handler_Connection is a Singleton class implementation
"""
class Handler_Connection(Simple_Module):
    __instance = None

    @classmethod
    def get_instance(cls, id):
        if cls.__instance is None:
            cls.__instance = cls(id)
        return cls.__instance

    def __init__(self, id):
        Simple_Module.__init__(self, id)


    def initialize(self, msg):
        pass

    def handle_message(self, msg):
        pass