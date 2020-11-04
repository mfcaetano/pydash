# -*- coding: utf-8 -*-
"""
@author: Marcos F. Caetano (mfcaetano@unb.br) 11/03/2020

@description: PyDash Project
"""


class SchedulerEvent:

    def __init__(self, msg, src, dst):
        self.origin = src
        self.destination = dst
        self.msg = msg

    def get_src(self):
        return self.origin

    def get_dst(self):
        return self.destination

    def get_msg(self):
        return self.msg
