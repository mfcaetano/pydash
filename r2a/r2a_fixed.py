
from r2a.ir2a import IR2A
from base.message import Message, Message_Kind
from player.parser import *

class R2A_Fixed(IR2A):

    def __init__(self, id):
        IR2A.__init__(self, id)
        self.parsed_mpd = ''
        self.qi         = []

    def handle_xml_request(self, msg):
        print('R2A_Fixed().handle_xml_request())')

        self.send_down(msg)

    def handle_xml_response(self, msg):
        print('R2A_Fixed().handle_xml_response()')

        #getting qi list
        self.parsed_mpd = parse_mpd(msg.get_payload())
        self.qi = self.parsed_mpd.get_qi()

        self.send_up(msg)

    def handle_segment_size_request(self, msg):
        print('R2A_Fixed().handle_segment_size_request()')

    def handle_segment_size_response(self, msg):
        print(f"R2A_Fixed().handle_segment_size_response - {msg.get_payload()}")

    def initialize(self):
        #self.send_up(Message(Message_Kind.SEGMENT_REQUEST, 'Olá Mundo'))
        pass

    def finalization(self):
        pass

