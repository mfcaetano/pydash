# -*- coding: utf-8 -*-
"""
@author: Marcos F. Caetano (mfcaetano@unb.br) 11/03/2020

@description: PyDash Project

The ConnectionHandler is a Singleton class implementation

The class responsible to retrieve segments in the web server.
Also it implements a traffic shaping approach.
"""

from base.simple_module import SimpleModule
from base.message import Message, MessageKind, SSMessage
from base.configuration_parser import ConfigurationParser
from player.parser import *
import http.client
import time
from scipy.stats import expon
from base.timer import Timer
import seaborn as sns
import matplotlib.pyplot as plt


class ConnectionHandler(SimpleModule):

    def __init__(self, id):
        SimpleModule.__init__(self, id)
        self.initial_time = 0
        self.qi = []

        # for traffic shaping
        config_parser = ConfigurationParser.get_instance()
        self.traffic_shaping_interval = int(config_parser.get_parameter('traffic_shaping_profile_interval'))
        self.traffic_shaping_seed = int(config_parser.get_parameter('traffic_shaping_seed'))
        self.traffic_shaping_values = []

        # mark the current traffic shapping interval
        self.current_traffic_shaping_interval = 0

        self.traffic_shaping_sequence = []
        # traffic shaping sequence position
        self.tss_position = 0
        # traffic shaping values position
        self.tsv_position = 0

        token = config_parser.get_parameter('traffic_shaping_profile_sequence')
        for i in range(len(token)):
            if token[i] == 'L':
                self.traffic_shaping_sequence.append(0)
            elif token[i] == 'M':
                self.traffic_shaping_sequence.append(1)
            elif token[i] == 'H':
                self.traffic_shaping_sequence.append(2)

        self.timer = Timer.get_instance()

    def get_traffic_shaping_positions(self):
        current_tsi = self.timer.get_current_time() // self.traffic_shaping_interval

        if current_tsi > self.current_traffic_shaping_interval:
            self.current_traffic_shaping_interval = current_tsi
            self.tss_position = (self.tss_position + 1) % len(self.traffic_shaping_sequence)

        self.tsv_position = (self.tsv_position + 1) % len(self.traffic_shaping_values[0])

        return (self.tss_position, self.tsv_position)

    def initialize(self):
        # self.send_down(Message(MessageKind.SEGMENT_REQUEST, 'Olá Mundo'))

        pass

    def bandwidth_limitation(self, package_size=0):
        if package_size == 0:
            return

        tsp = self.get_traffic_shaping_positions()
        target_throughput = self.traffic_shaping_values[self.traffic_shaping_sequence[tsp[0]]][tsp[1]]

        print(f'Execution Time {self.timer.get_current_time()} > target throughput: {target_throughput} - profile: ({self.traffic_shaping_sequence[tsp[0]]}, {tsp[1]})')

        rtt = time.perf_counter() - self.initial_time
        throughput = package_size / rtt

        # we didn't pass our throughput go
        if target_throughput >= throughput:
            return

        waiting_time = (package_size - (target_throughput * rtt)) / target_throughput
        time.sleep(waiting_time)

    def finalization(self):
        pass


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

        parsed_mpd = parse_mpd(msg.get_payload())
        self.qi = parsed_mpd.get_qi()

        increase_factor = 1
        low = round(self.qi[len(self.qi) - 1] * increase_factor)
        medium = round(self.qi[(len(self.qi) // 2) - 1] * increase_factor)
        high = round(self.qi[0] * increase_factor)

        self.traffic_shaping_values.append(
            expon.rvs(scale=1, loc=low, size=1000, random_state=self.traffic_shaping_seed))
        self.traffic_shaping_values.append(
            expon.rvs(scale=1, loc=medium, size=1000, random_state=self.traffic_shaping_seed))
        self.traffic_shaping_values.append(
            expon.rvs(scale=1, loc=high, size=1000, random_state=self.traffic_shaping_seed))

        self.send_up(msg)

    def handle_segment_size_request(self, msg):
        port = '80'
        host_name = msg.get_host_name()
        path_name = msg.get_url()
        ss_file = ''
        self.initial_time = time.perf_counter()

        print(f'Execution Time {self.timer.get_current_time()} > selected QI: {self.qi.index(msg.get_quality_id())}')

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
            msg.add_bit_length(8 * len(ss_file))
            self.bandwidth_limitation(msg.get_bit_length())
            decoded = True

        if not decoded and '404 Not Found' in ss_file:
            msg.set_found(False)

        self.send_up(msg)

    def handle_segment_size_response(self, msg):
        pass

    def handle_xml_response(self, msg):
        pass
