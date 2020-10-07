
from base.simple_module import Simple_Module
from base.message import Message, Message_Kind
import http.client

"""
The Connection_Handler is a Singleton class implementation
"""
class Connection_Handler(Simple_Module):

    def __init__(self, id):
        Simple_Module.__init__(self, id)


    def initialize(self):
        #self.send_down(Message(Message_Kind.SEGMENT_REQUEST, 'Olá Mundo'))

        pass

    def finalization(self):
        pass

#    def handle_message(self, msg):
#        print(f'Connection_Handler recebi uma msg {msg.get_payload()}')
#        pass

    def handle_xml_request(self, msg):
        if not 'http://' in msg.get_payload():
            raise ValueError('url_mpd parameter should starts with http://')

        url_tokens = msg.get_payload().split('/')[2:]
        port = '80'
        host_name  = url_tokens[0]
        path_name  = '/' + '/'.join(url_tokens[1:])
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

        xml_response = Message(Message_Kind.XML_RESPONSE, mdp_file)

        self.send_up(xml_response)


    def handle_segment_size_request(self, msg):
        port = '80'
        host_name = msg.get_host_name()
        path_name = msg.get_url()
        ss_file = ''

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

        msg.set_kind(Message_Kind.SEGMENT_RESPONSE)

        decoded = False

        try:
            ss_file = ss_file.decode()
        except UnicodeDecodeError:
            #if wasn't possible to decode() is a ss
            msg.add_bit_length(len(ss_file))
            decoded = True

        if not decoded and '404 Not Found' in ss_file:
            msg.set_found(False)

        self.send_up(msg)




    def handle_segment_size_response(self, msg):
        pass

    def handle_xml_response(self, msg):
        pass
