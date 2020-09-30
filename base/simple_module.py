
'''
Abstract Class for Simple Module Implementation.

Class implements basic functionality to be called by the main program.
'''

from base.message import Message
from abc import ABCMeta, abstractmethod
from base.scheduler import Scheduler
from base.scheduler_event import Scheduler_Event

class Simple_Module(metaclass=ABCMeta):

    def __init__(self, id):
        self.scheduler = Scheduler.get_instance()
        self.id = id

    def send_up(self, msg):
        self.scheduler.add_event(Scheduler_Event(msg, self.id, self.id-1))

        #if self.id == 0:
        #    print(f'Object {self} with id {self.id} is in the top of the control stack!')
        #    exit(0)


    def send_down(self, msg):
        self.scheduler.add_event(Scheduler_Event(msg, self.id, self.id+1))

    @abstractmethod
    def initialize(self):
        print(f'> Initializing module {self.__class__.__name__}')
        pass

    @abstractmethod
    def finalization(self):
        print(f'> Finalization module {self.__class__.__name__}')
        pass

    @abstractmethod
    def handle_message(self):
        pass