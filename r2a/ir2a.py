# -*- coding: utf-8 -*-
"""
@author: Marcos F. Caetano (mfcaetano@unb.br) 03/11/2020

@description: PyDash Project

Abstract Class for R2A (Rate Adaptation Algorithms) implementations

It is necessary to implement all the @abstractmethod methods to generate a new R2A Algorithm implementation

"""

from base.simple_module import SimpleModule
from abc import ABCMeta, abstractmethod
from base.message import Message, MessageKind
from base.whiteboard import Whiteboard


class IR2A(SimpleModule):

    def __init__(self, id):
        SimpleModule.__init__(self, id)

        # Whiteboard object to change statistical information between Player and R2A algorithm
        self.whiteboard = Whiteboard.get_instance()

    @abstractmethod
    def handle_xml_request(self, msg):
        pass

    @abstractmethod
    def handle_xml_response(self, msg):
        pass

    @abstractmethod
    def handle_segment_size_request(self, msg):
        pass

    @abstractmethod
    def handle_segment_size_response(self, msg):
        pass

    @abstractmethod
    def initialize(self):
        SimpleModule.initialize(self)
        pass

    @abstractmethod
    def finalization(self):
        SimpleModule.finalization(self)
        pass
