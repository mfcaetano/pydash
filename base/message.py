
from enum import Enum

class Message(Enum):
    SELF = 1
    SEGMENT_REQUEST = 2
    SEGMENT_RESPONSE = 3
    XML_REQUEST = 4
    XML_RESPONSE = 5


    def __init__(self, payload):
        self.payload = payload