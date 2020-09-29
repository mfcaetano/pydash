from player.player import Player
from base.scheduler import Scheduler
from r2a.r2a_fixed import R2A_Fixed
from base.simple_module import Simple_Module

player = Player(0)

player.send_up("teste")

'''
print(player.get_amount_of_video_to_play())

s1 = Scheduler.get_instance()
s2 = Scheduler.get_instance()

for i in range(10):
    s1.add_event(i)

for i in range(10):
    print(s2.get_event())


if id(s1) == id(s2):
    print("Singleton works, both variables contain the same instance.")
else:
    print("Singleton failed, variables contain different instances.")

#r2a = R2A_Fixed()

#r2a.handle_xml_request()

'''