from base.simple_module import SimpleModule
from base.message import Message, MessageKind
import http.client
import time

"""
The ConnectionHandler is a Singleton class implementation
"""


class ConnectionHandler(SimpleModule):

    def __init__(self, id):
        SimpleModule.__init__(self, id)
        self.rtt_length = []
        self.initial_time = 0

    def initialize(self):
        # self.send_down(Message(MessageKind.SEGMENT_REQUEST, 'Olá Mundo'))

        pass

    def bandwidth_limitation(self):
        pass

    def finalization(self):
        print("Measurements at Connection Handler Level: ")
        print(self.rtt_length)
        print("Measured throughput")
        for i in self.rtt_length:
            print(f'{round(i[1]/i[0]):>10} bps')
        pass

    #    def handle_message(self, msg):
    #        print(f'ConnectionHandler recebi uma msg {msg.get_payload()}')
    #        pass

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
            decoded = True

        if not decoded and '404 Not Found' in ss_file:
            msg.set_found(False)

        self.bandwidth_limitation()



        self.rtt_length.append([round(time.perf_counter() - self.initial_time, 6), msg.get_bit_length()])

        self.send_up(msg)

    def handle_segment_size_response(self, msg):
        pass

    def handle_xml_response(self, msg):
        pass
