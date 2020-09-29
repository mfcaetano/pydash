
from player.player import Player
from base.scheduler import Scheduler


class Dash_Client:

    def __init__(self):
        self.player = Player()
        self.scheduler = Scheduler.get_instance()