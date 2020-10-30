from r2a.ir2a import IR2A
from base.message import Message, MessageKind
from player.parser import *
import random


class R2ARandom(IR2A):

    def __init__(self, id):
        IR2A.__init__(self, id)
        self.parsed_mpd = ''
        self.qi = []

    def handle_xml_request(self, msg):
        self.send_down(msg)

    def handle_xml_response(self, msg):
        # getting qi list
        self.parsed_mpd = parse_mpd(msg.get_payload())
        self.qi = self.parsed_mpd.get_qi()

        self.send_up(msg)

    def handle_segment_size_request(self, msg):

        #random choosing approach
        qi_id = random.randint(0, len(self.qi)-1)

        # Hora de definir qual qualidade será escolhida
        msg.add_quality_id(self.qi[qi_id])

        self.send_down(msg)

    def handle_segment_size_response(self, msg):
        self.send_up(msg)

    def initialize(self):
        # self.send_up(Message(MessageKind.SEGMENT_REQUEST, 'Olá Mundo'))
        pass

    def finalization(self):
        pass
