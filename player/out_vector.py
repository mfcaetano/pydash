import datetime

class Out_Vector:

    def __init__(self):
        self.items = []

    def add(self, t, item):
        self.items.append((t, item))

    def __str__(self):
        return self.items.__str__()