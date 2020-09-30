from base.simple_module import Simple_Module
from abc import ABCMeta, abstractmethod
'''
Abstract Class for R2A Implementations
Rate Adaptation Algorithms
'''
class IR2A(Simple_Module):

    def __init__(self, id):
        Simple_Module.__init__(self, id)

    @abstractmethod
    def handle_xml_request(self):
        pass

    @abstractmethod
    def handle_xml_respose(self):
        pass

    @abstractmethod
    def handle_segment_size_request(self):
        pass

    @abstractmethod
    def handle_segment_size_respose(self):
        pass

    @abstractmethod
    def initialize(self):
        Simple_Module.initialize(self)
        pass

    @abstractmethod
    def finalization(self):
        Simple_Module.finalization(self)
        pass

    @abstractmethod
    def handle_message(self, msg):
        print(f'IR2A recebi uma msg {msg.get_payload()}')
        pass
