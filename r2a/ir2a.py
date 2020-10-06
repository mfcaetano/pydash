from base.simple_module import Simple_Module
from abc import ABCMeta, abstractmethod
from base.message import Message, Message_Kind
'''
Abstract Class for R2A Implementations
Rate Adaptation Algorithms
'''
class IR2A(Simple_Module):

    def __init__(self, id):
        Simple_Module.__init__(self, id)

    @abstractmethod
    def handle_xml_request(self, msg):
        pass

    @abstractmethod
    def handle_xml_response(self, msg):
        pass

    @abstractmethod
    def handle_segment_size_request(self, msg):
        pass

    @abstractmethod
    def handle_segment_size_response(self, msg):
        pass

    @abstractmethod
    def initialize(self):
        Simple_Module.initialize(self)
        pass

    @abstractmethod
    def finalization(self):
        Simple_Module.finalization(self)
        pass

