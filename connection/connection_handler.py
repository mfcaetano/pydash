
from base.simple_module import Simple_Module

"""
The Connection_Handler is a Singleton class implementation
"""
class Connection_Handler(Simple_Module):

    def __init__(self, id):
        Simple_Module.__init__(self, id)


    def initialize(self):
        pass

    def finalization(self):
        pass

    def handle_message(self, msg):
        print(f'Connection_Handler recebi uma msg {msg.get_payload()}')
        pass