from base.whiteboard import Whiteboard
from player.parser import *
from r2a.ir2a import IR2A
from player.player import *
from math import sqrt

class R2AFuzzy(IR2A):

    def __init__(self, id):
        IR2A.__init__(self, id)

        self.vazao = []
        self.qi = []
        self.buffers = []

    def handle_xml_request(self, msg):
        self.send_down(msg)

    def handle_xml_response(self, msg):
        parsed_mpd = parse_mpd(msg.get_payload())
        self.qi = parsed_mpd.get_qi()

        self.send_up(msg)

    def handle_segment_size_request(self, msg):
        self.buffer = self.whiteboard.get_playback_buffer_size()
        if len(self.buffer)>1:
            print(f"!!!!!!!!!!!!!!!!!!!!!!!!!{self.output_controller(self.buffer)}")
        msg.add_quality_id(self.qi[0])
        self.send_down(msg)

    def output_controller(self, buffer):
        T = 35
        TWO_THIRDS_T = (2 * T) /3
        FOUR_T = 4 * T
        buffer_time = buffer[-1][1]
        previous_buffer_time = buffer[-2][1]
        self.buffers.append(buffer_time)
        FACTORS = {'N2':0.25,'N1':0.5, 'Z':1, 'P1':1.5, 'P2':2}
        short, close, long, falling, steady, rising = 0,0,0,0,0,0

        if(buffer_time <= TWO_THIRDS_T):
            short = 1
        elif(buffer_time >= T):
            short = 0
        else:
            short = ((-3) * buffer_time) / T + 3
        
        if(buffer_time <= TWO_THIRDS_T or buffer_time >= FOUR_T):
            close = 0
        elif(buffer_time <= T):
            close = (3 / T) * buffer_time - 2
        else:
            close = (-buffer_time) / (3 * T) + 4 / 3

        if(buffer_time <= T):
            long = 0
        elif(buffer_time >= 4*T):
            long = 1
        else:
            long = buffer_time / (3*T) - 1 / 3

        diff = buffer_time - previous_buffer_time

        if diff <= -(TWO_THIRDS_T):
            falling = 1
        elif diff >= 0:
            falling = 0
        else:
            falling = (-3 * diff) / (2 * T)

        if diff <= -(TWO_THIRDS_T) or diff >= FOUR_T:
            steady = 0
        elif diff <= 0:
            steady = (3 / (2 * T)) * diff + 1
        else:
            steady = - diff / (FOUR_T) + 1

        if diff <= 0:
            rising = 0
        elif diff >= FOUR_T:
            rising = 1
        else:
            rising = diff / FOUR_T

        print(f"*******************{previous_buffer_time, buffer_time}")
        print(f'>>>>>>>>>>>>>>>>>>>>.{short, close, long}')
        print(f'>>>>>>>>>>>>>>>>>>>>.{falling, steady, rising}')
        
        rules = []

        rules.append(min(short, falling)) 
        rules.append(min(close, falling)) 
        rules.append(min(long, falling)) 
        rules.append(min(short, steady)) 
        rules.append(min(close, steady)) 
        rules.append(min(long, steady)) 
        rules.append(min(short, rising)) 
        rules.append(min(close, rising)) 
        rules.append(min(long, rising))

        I =  sqrt(rules[8]**2)
        SI = sqrt(rules[5]**2 + rules[7]**2)        
        NC = sqrt(rules[2]**2 + rules[4]**2 + rules[6]**2)        
        SR = sqrt(rules[1]**2 + rules[3]**2)        
        R = sqrt(rules[0]**2)        

        f_num = FACTORS['N2'] * R + FACTORS['N1'] * SR + FACTORS['Z'] * NC + FACTORS['P1'] * SI + FACTORS['P2'] * I  
        f_den = SR + R + NC + SI + I

        return f_num / f_den

    def handle_segment_size_response(self, msg):
        self.send_up(msg)

    def initialize(self):
        pass

    def finalization(self):
        pass

