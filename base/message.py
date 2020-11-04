# -*- coding: utf-8 -*-
"""
@author: Marcos F. Caetano (mfcaetano@unb.br) 11/03/2020

@description: PyDash Project
"""

from enum import Enum


class MessageKind(Enum):
    SELF = 1
    SEGMENT_REQUEST = 2
    SEGMENT_RESPONSE = 3
    XML_REQUEST = 4
    XML_RESPONSE = 5


class Message:
    def __init__(self, kind, payload):
        self.payload = payload
        self.kind = kind
        self.bit_length = 0

    def get_payload(self):
        return self.payload

    def set_kind(self, kind):
        self.kind = kind

    def get_kind(self):
        return self.kind

    def add_bit_length(self, bit_length):
        self.bit_length = bit_length

    def get_bit_length(self):
        return self.bit_length


# Segment Size Message
class SSMessage(Message):

    def __init__(self, kind, payload=None):

        Message.__init__(self, kind, payload)

        self.path_name = ''
        self.media_mpd = ''
        self.host_name = ''
        self.quality_id = 0
        self.segment_id = 0
        self.__found = True

    def __str__(self):
        return f'{self.segment_id}, {self.quality_id}, {self.bit_length}, {self.__found}, {self.path_name}, {self.media_mpd}, {self.host_name}'

    def add_path_name(self, path_name):
        self.path_name = path_name

    def add_host_name(self, host_name):
        self.host_name = host_name

    def get_host_name(self):
        return self.host_name

    def add_segment_id(self, segment_id):
        self.segment_id = segment_id

    def get_segment_id(self):
        return self.segment_id

    def get_segment_size(self):
        for i in self.path_name.split('/'):
            if 'sec' in i:
                return int(i.split('sec')[0])

    def add_media_mpd(self, media_mpd):
        self.media_mpd = media_mpd

    def add_quality_id(self, quality_id):
        self.quality_id = quality_id

    def get_quality_id(self):
        return self.quality_id

    def set_found(self, status=True):
        self.__found = status

    def found(self):
        return bool(self.bit_length > 0 and self.__found)

    def get_url(self):
        self.media_mpd = self.media_mpd.replace('$Bandwidth$', str(self.quality_id))
        self.media_mpd = self.media_mpd.replace('$Number$', str(self.segment_id))
        return self.path_name + '/' + self.media_mpd
