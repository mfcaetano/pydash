# -*- coding: utf-8 -*-
"""
@author: Marcos F. Caetano (mfcaetano@unb.br) 11/03/2020

@description: PyDash Project

OutVector class stores all simulation statistics to be plot later.
"""

import datetime


class OutVector:

    def __init__(self):
        self.items = []

    def add(self, t, item):
        self.items.append([t, item])

    def __len__(self):
        return len(self.items)

    def __str__(self):
        return self.items.__str__()

    def get_items(self):
        return self.items

    #def __getitem__(self, key):
    #    if len(self.items) == 0:
    #        return []

    #    return self.items[key]
