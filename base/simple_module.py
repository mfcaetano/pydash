
'''
Abstract Class for Simple Module Implementation.

Class implements basic functionality to be called by the main program.
'''

from base.message import Message
from abc import ABCMeta, abstractmethod

class Simple_Module(metaclass=ABCMeta):

    def send_up(self, msg):
        pass

    def send_down(self, msg):
        pass

    @abstractmethod
    def initialize(self, msg):
        pass

    @abstractmethod
    def handle_message(self, msg):
        pass