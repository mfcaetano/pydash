

'''
The Scheduler is a Singleton class implementation
'''


class Scheduler:
    __instance = None

    def __init__(self):
        self.events = []

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def add_event(self, event):
        self.events.append(event)

    def get_event(self):
        return self.events.pop(0)
