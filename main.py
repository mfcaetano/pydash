from player.player import Player
from connection.connection_handler import Connection_Handler
from base.scheduler import Scheduler
from base.scheduler_event import Scheduler_Event
from r2a.r2a_fixed import R2A_Fixed
from base.simple_module import Simple_Module
from dash_client import Dash_Client

dash_client = Dash_Client()
dash_client.run_application()
#dash_client.handle_scheduler_event(Scheduler_Event('Hello World', 0, 1))


'''
player = Player.get_instance(0)

handler_connection = Connection_Handler.get_instance(1)

player.send_up("teste")

print(player.get_amount_of_video_to_play())

s1 = Scheduler()
s2 = Scheduler()

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