
from enum import Enum

class Message_Kind(Enum):
    SELF = 1
    SEGMENT_REQUEST = 2
    SEGMENT_RESPONSE = 3
    XML_REQUEST = 4
    XML_RESPONSE = 5


class Message:
    def __init__(self, kind, payload):
        self.payload = payload
        self.kind    = kind

    def get_payload(self):
        return self.payload

    def get_kind(self):
        return self.kind