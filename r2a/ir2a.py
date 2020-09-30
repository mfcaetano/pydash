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
    def handle_xml_respose(self, msg):
        pass

    @abstractmethod
    def handle_segment_size_request(self, msg):
        pass

    @abstractmethod
    def handle_segment_size_respose(self, msg):
        pass

    @abstractmethod
    def initialize(self):
        Simple_Module.initialize(self)
        pass

    @abstractmethod
    def finalization(self):
        Simple_Module.finalization(self)
        pass

    def handle_message(self, msg):
        print(f'IR2A recebi uma msg {msg.get_payload()} kind {msg.get_kind()}')

        if msg.get_kind() == Message_Kind.XML_REQUEST:
            self.handle_xml_request(msg)
        elif msg.get_kind() == Message_Kind.XML_RESPONSE:
            self.handle_xml_respose(msg)
        elif msg.get_kind() == Message_Kind.SEGMENT_REQUEST:
            self.handle_segment_size_request(msg)
        elif msg.get_kind() == Message_Kind.SEGMENT_RESPONSE:
            self.handle_segment_size_respose(msg)
        else:
            raise ValueError(f'Invalid Message Kind - {msg}')

        pass
