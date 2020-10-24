from base.simple_module import SimpleModule
from base.message import Message, MessageKind
from base.configuration_parser import ConfigurationParser
from player.parser import *
import http.client
import time
from scipy.stats import expon
import seaborn as sns

"""
The ConnectionHandler is a Singleton class implementation
"""


class ConnectionHandler(SimpleModule):

    def __init__(self, id):
        SimpleModule.__init__(self, id)
        self.rtt_length = []
        self.initial_time = 0

        #for traffic shaping
        config_parser = ConfigurationParser.get_instance()
        self.traffic_shaping_interval = int(config_parser.get_parameter('traffic_shaping_profile_interval'))
        self.traffic_shaping_seed     = int(config_parser.get_parameter('traffic_shaping_seed'))
        self.traffic_shaping_values   = []
        self.traffic_shaping_sequence = []

        token = config_parser.get_parameter('traffic_shaping_profile_sequence')
        for i in range(len(token)):

            if token[i] == 'L':
                self.traffic_shaping_sequence.append(0)
            elif token[i] == 'M':
                self.traffic_shaping_sequence.append(1)
            elif token[i] == 'H':
                self.traffic_shaping_sequence.append(2)


    def initialize(self):
        # self.send_down(Message(MessageKind.SEGMENT_REQUEST, 'Olá Mundo'))

        pass

    def bandwidth_limitation(self, package_size=0):
        if package_size == 0:
            return

        target_throughput = 10000
        spent_time = time.perf_counter() - self.initial_time
        throughput = package_size / spent_time

        #we didn't pass our throughput go
        if target_throughput >= throughput:
            return

        waiting_time = (package_size - target_throughput * spent_time) /  target_throughput
        time.sleep(waiting_time)

    def finalization(self):
        pass
#        print("Measurements at Connection Handler Level: ")
#        print(self.rtt_length)
#        print("Measured throughput")
#        for i in self.rtt_length:
#            print(f'{round(i[1]/i[0]):>10} bps')

    def handle_xml_request(self, msg):
        if not 'http://' in msg.get_payload():
            raise ValueError('url_mpd parameter should starts with http://')

        self.initial_time = time.perf_counter()

        url_tokens = msg.get_payload().split('/')[2:]
        port = '80'
        host_name = url_tokens[0]
        path_name = '/' + '/'.join(url_tokens[1:])
        mdp_file = ''

        try:
            connection = http.client.HTTPConnection(host_name, port)
            connection.request('GET', path_name)
            mdp_file = connection.getresponse().read().decode()
            connection.close()
        except Exception as err:
            print('> Houston, we have a problem!')
            print(f'> trying to connecto to: {msg.get_payload()}')
            print(err)
            exit(-1)

        msg = Message(MessageKind.XML_RESPONSE, mdp_file)
        msg.add_bit_length(8 * len(mdp_file))

        self.rtt_length.append([round(time.perf_counter() - self.initial_time, 6), msg.get_bit_length()])

        parsed_mpd = parse_mpd(msg.get_payload())
        qi = parsed_mpd.get_qi()

        increase_factor = 1
        low    = round(qi[len(qi)-1] * increase_factor)
        medium = round(qi[(len(qi)//2)-1] * increase_factor)
        high   = round(qi[0] * increase_factor)

        self.traffic_shaping_values.append([round(x) for x in expon.rvs(scale=1,loc=low,size=10,random_state=self.traffic_shaping_seed)])
        self.traffic_shaping_values.append([round(x) for x in expon.rvs(scale=1,loc=medium,size=10,random_state=self.traffic_shaping_seed)])
        self.traffic_shaping_values.append([round(x) for x in expon.rvs(scale=1,loc=high,size=10,random_state=self.traffic_shaping_seed)])

        self.send_up(msg)

    def handle_segment_size_request(self, msg):
        port = '80'
        host_name = msg.get_host_name()
        path_name = msg.get_url()
        ss_file = ''
        self.initial_time = time.perf_counter()

        try:
            connection = http.client.HTTPConnection(host_name, port)
            connection.request('GET', path_name)
            ss_file = connection.getresponse().read()
            connection.close()
        except Exception as err:
            print('> Houston, we have a problem!')
            print(f'> trying to connecto to: {msg.get_payload()}')
            print(err)
            exit(-1)

        msg.set_kind(MessageKind.SEGMENT_RESPONSE)

        decoded = False

        try:
            ss_file = ss_file.decode()
        except UnicodeDecodeError:
            # if wasn't possible to decode() is a ss
            msg.add_bit_length(8*len(ss_file))
            self.bandwidth_limitation(msg.get_bit_length())
            decoded = True

        if not decoded and '404 Not Found' in ss_file:
            msg.set_found(False)

        self.rtt_length.append([round(time.perf_counter() - self.initial_time, 6), msg.get_bit_length()])

        self.send_up(msg)

    def handle_segment_size_response(self, msg):
        pass

    def handle_xml_response(self, msg):
        pass
