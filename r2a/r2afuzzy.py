from base.whiteboard import Whiteboard
from player.parser import *
from r2a.ir2a import IR2A


class R2AFuzzy(IR2A):

    def __init__(self, id):
        IR2A.__init__(self, id)

        self.vazao = []
        self.qi = []

        self.whiteboard = Whiteboard.get_instance()

    def handle_xml_request(self, msg):
        self.send_down(msg)

    def handle_xml_response(self, msg):
        parsed_mpd = parse_mpd(msg.get_payload())
        self.qi = parsed_mpd.get_qi()
        print(self.qi)

        self.send_up(msg)

    def handle_segment_size_request(self, msg):
        msg.add_quality_id(self.qi[0])

        self.send_down(msg)

    def handle_segment_size_response(self, msg):
        self.send_up(msg)

    def initialize(self):
        pass

    def finalization(self):
        pass
