
from base.simple_module import Simple_Module

"""
The Connection_Handler is a Singleton class implementation
"""
class Connection_Handler(Simple_Module):
    __instance = None

    @classmethod
    def get_instance(cls, id):
        if cls.__instance is None:
            cls.__instance = cls(id)
        return cls.__instance

    def __init__(self, id):
        Simple_Module.__init__(self, id)


    def initialize(self):
        pass

    def finalization(self):
        pass

    def handle_message(self, msg):
        pass