
from r2a.ir2a import IR2A
from base.message import Message, Message_Kind

class R2A_Fixed(IR2A):

    def __init__(self, id):
        IR2A.__init__(self, id)

    def handle_xml_request(self, msg):
        print(f'handle_xml_request - {msg.get_payload()}')

    def handle_xml_respose(self, msg):
        print(f'handle_xml_respose - {msg.get_payload()}')

    def handle_segment_size_request(self, msg):
        print(f'handle_segment_size_request - {msg.get_payload()}')

    def handle_segment_size_respose(self, msg):
        print(f"handle_segment_size_respose - {msg.get_payload()}")

    def initialize(self):
        self.send_up(Message(Message_Kind.SEGMENT_REQUEST, 'Olá Mundo'))
        pass

    def finalization(self):
        pass

