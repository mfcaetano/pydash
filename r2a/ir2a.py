from base.simple_module import SimpleModule
from abc import ABCMeta, abstractmethod
from base.message import Message, MessageKind
'''
Abstract Class for R2A Implementations
Rate Adaptation Algorithms
'''
class IR2A(SimpleModule):

    def __init__(self, id):
        SimpleModule.__init__(self, id)

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
        SimpleModule.initialize(self)
        pass

    @abstractmethod
    def finalization(self):
        SimpleModule.finalization(self)
        pass

