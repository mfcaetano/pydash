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

        self.scheduler = Scheduler.get_instance()

        self.modules = []

        # adding modules to manage
        self.player = Player.get_instance(0)

        # automatic loading class by the name
        r2a_class = getattr(importlib.import_module('r2a.' + r2a_algorithm.lower()), r2a_algorithm)
        self.r2a = r2a_class.get_instance(1)

        self.connection_handler = Connection_Handler.get_instance(2)

        self.modules.append(self.player)
        self.modules.append(self.r2a)
        self.modules.append(self.connection_handler)


    def run_application(self):
        self.modules_initialization()




        self.modules_finalization()


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