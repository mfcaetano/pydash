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

    def linear_function(self,x0,x1, diff = False):
        a  = 1 / (x1 - x0)
        b = - (a * x0)
        if diff:
            return a * self.diff + b
        return a * self.buffer_time + b

    def output_controller(self, buffer):
        T = 35
        TWO_THIRDS_T = (2 * T) /3
        FOUR_T = 4 * T
        self.buffer_time = buffer[-1][1]
        try:
            previous_buffer_time = self.buffers[-1]
        except:
            previous_buffer_time = self.buffer_time
        self.buffers.append(self.buffer_time)
        FACTORS = {'N2':0.25,'N1':0.5, 'Z':1, 'P1':1.5, 'P2':2}
        short, close, long, falling, steady, rising = 0,0,0,0,0,0

        if(self.buffer_time <= TWO_THIRDS_T):
            short = 1
        elif(self.buffer_time >= T):
            short = 0
        else:
            short = self.linear_function(T, TWO_THIRDS_T)
        
        if(self.buffer_time <= TWO_THIRDS_T or self.buffer_time >= FOUR_T):
            close = 0
        elif(self.buffer_time <= T):
            close = self.linear_function(TWO_THIRDS_T, T)
        else:
            close = self.linear_function(FOUR_T, T)

        if(self.buffer_time <= T):
            long = 0
        elif(self.buffer_time >= 4*T):
            long = 1
        else:
            long = self.linear_function(T, FOUR_T)

        self.diff = self.buffer_time - previous_buffer_time

        if self.diff <= -(TWO_THIRDS_T):
            falling = 1
        elif self.diff >= 0:
            falling = 0
        else:
            falling = self.linear_function(0, - TWO_THIRDS_T, True)

        if self.diff <= -(TWO_THIRDS_T) or self.diff >= FOUR_T:
            steady = 0
        elif self.diff <= 0:
            steady = self.linear_function(-TWO_THIRDS_T, 0, True)
        else:
            steady = self.linear_function(FOUR_T, 0, True)

        if self.diff <= 0:
            rising = 0
        elif self.diff >= FOUR_T:
            rising = 1
        else:
            rising = self.linear_function(0, FOUR_T, True)

        print(f"*******************{previous_buffer_time, self.buffer_time}")
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

