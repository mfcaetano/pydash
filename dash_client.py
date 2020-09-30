import json
import importlib
import r2a
from player.player import Player
from base.scheduler import Scheduler
from connection.connection_handler import Connection_Handler


class Dash_Client:

    def __init__(self):
        with open('dash_client.json') as f:
            dash_client_parameters = json.load(f)

        r2a_algorithm = str(dash_client_parameters['r2a_algorithm'])

        self.scheduler = Scheduler()

        self.modules = []

        # adding modules to manage
        self.player = Player(0)

        # automatic loading class by the name
        r2a_class = getattr(importlib.import_module('r2a.' + r2a_algorithm.lower()), r2a_algorithm)
        self.r2a = r2a_class(1)

        self.connection_handler = Connection_Handler(2)

        self.modules.append(self.player)
        self.modules.append(self.r2a)
        self.modules.append(self.connection_handler)


    def run_application(self):
        self.modules_initialization()

        while not self.scheduler.is_empty():
            event = self.scheduler.get_event()
            self.handle_scheduler_event(event)

        self.modules_finalization()


    def handle_scheduler_event(self, event):

        #checking if the event is inside of the modules position range limits
        if event.get_dst() < 0 or event.get_dst() >= len(self.modules):
            print(f'It is no possible to route a {event.get_msg()} message from {event.get_src()} to {event.get_dst()} module list position.')
            exit(0)

        self.modules[event.get_dst()].handle_message(event.get_msg())



    def modules_initialization(self):
        print('Initialization modules phase.')
        for m in self.modules:
            super(type(m), m).initialize()
            m.initialize()

    def modules_finalization(self):
        print('Finalization modules phase.')
        for m in self.modules:
            super(type(m), m).finalization()
            m.finalization()