# -*- coding: utf-8 -*-
"""
@author: Marcos F. Caetano (mfcaetano@unb.br) 11/03/2020

@description: PyDash Project

A Global timer reference used by all classes.
"""
import time


class Timer():
    __instance = None

    @staticmethod
    def get_instance():
        if Timer.__instance is None:
            Timer()
        return Timer.__instance

    def __init__(self):
        if Timer.__instance is not None:
            raise Exception('This class is a singleton!')
        else:
            # for the statistics purpose
            self.started_time = time.perf_counter()
            Timer.__instance = self

    def get_current_time(self):
        return round(time.perf_counter() - self.started_time, 6)

    def get_started_time(self):
        return self.started_time
