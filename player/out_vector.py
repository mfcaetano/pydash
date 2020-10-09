import time

class Out_Vector:

    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append((time.time(), item))