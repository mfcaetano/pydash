from player.player import Player
from base.scheduler import Scheduler


class Dash_Client:

    def __init__(self):
        self.scheduler = Scheduler.get_instance()

        self.modules = []

        # adding modules to manage
        self.player = Player()
