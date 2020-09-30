

class Scheduler_Event:

    def __init__(self, message, origin, destination):
        self.origin = origin
        self.destination = destination
        self.message = message


    def get_origin(self):
        return self.origin

    def get_destination(self):
        return self.destination

    def get_message(self):
        return self.message
