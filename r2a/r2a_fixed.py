
from r2a.ir2a import IR2A

class R2A_Fixed(IR2A):

    def __init__(self, id):
        IR2A.__init__(self, id)

    def handle_xml_request(self):
        print('handle_xml_request')

    def handle_xml_respose(self):
        print('handle_xml_respose')

    def handle_segment_size_request(self):
        print('handle_segment_size_request')

    def handle_segment_size_respose(self):
        print("handle_segment_size_respose")

    def initialize(self, msg):
        pass

    def handle_message(self, msg):
        pass

