
from player.out_vector import Out_Vector
from base.simple_module import Simple_Module
from base.message import *
from base.configuration_parser import Configuration_Parser
from player.parser import *

'''
quality_id - Taxa em que o video foi codificado (46980bps, ..., 4726737bps) 
qi         - indice de qualidade normalizado
segment_id - número de sequência do arquivo de video

Player is a Singleton class implementation

'''


class Player(Simple_Module):

    def __init__(self, id):
        Simple_Module.__init__(self, id)

        config_parser = Configuration_Parser.get_instance()

        self.buffer_size = int(config_parser.get_parameter('buffer_size'))
        self.buffering_until = int(config_parser.get_parameter('buffering_until'))
        self.max_buffer_size = int(config_parser.get_parameter('max_buffer_size'))
        self.playback_step = int(config_parser.get_parameter('playbak_step'))
        self.url_mpd = config_parser.get_parameter('url_mpd')

        # last pause started at time
        self.pause_started_at = 0

        # tag to verify if buffer has an minimal amount of data
        self.buffer_initialization = True

        # Does the player already started to download a segment?
        self.already_downloading = False

        # buffer itself
        self.buffer = []

        # the buffer played position
        self.buffer_played = 0

        # history of what was played in buffer
        self.playback_history = []

        #initialize with the first segment sequence number to download
        self.segment_id = 1

        self.parsed_mpd = ''
        self.qi         = []

        # for the statistics purpose
        self.playback_qi = Out_Vector()
        self.playback_pauses = Out_Vector()
        self.playback = Out_Vector()
        self.playback_buffer_size = Out_Vector()

    # data for r2a algorithms
    def get_playback_history(self):
        return self.playback_history

    def get_amount_of_video_to_play(self):
        return len(self.buffer) - self.buffer_played

    def is_there_something_to_play(self):
        return bool(len(self.buffer) - self.buffer_played > 0)

    def is_buffer_full(self):
        return bool((len(self.buffer) - self.buffer_played) >= self.buffer_size)

    def get_current_playtime_position(self):
        return self.buffer_played

    # called function every time a segment was played
    def handle_video_playback(self):
        return False

    def buffering_video_segment(self, video_segment):

        # buffer already stored the segment id
        if video_segment.get_segment_id() > len(self.buffer):
            print(f'buffer: {self.buffer}')
            print(f'video segment: {video_segment.get_segment_id}')
            exit(-1)

        # adding the segment in the buffer
        self.buffer.append(video_segment.get_qi())

        if self.buffer_initialization and self.get_amount_of_video_to_play() >= self.buffering_until:
            self.buffer_initialization = False
            print('with buffering')
            # start the process to play the video

        elif not self.buffer_initialization and self.get_amount_of_video_to_play() > 0:
            # start the process to play the video
            print('not with buffering')

    def request_segment(self):
        segment_request = SS_Message(Message_Kind.SEGMENT_REQUEST)

        url_tokens = self.url_mpd.split('/')

        segment_request.add_host_name(url_tokens[2])
        segment_request.add_path_name('/'.join(url_tokens[:len(url_tokens)-1]))
        segment_request.add_media_mpd(navigate_mpd(self.parsed_mpd, 'media')[1])
        segment_request.add_segment_id(self.segment_id)

        self.segment_id += 1

        self.send_down(segment_request)


    def initialize(self):
        #starting the application downloading mdp file
        xml_request = Message(Message_Kind.XML_REQUEST, self.url_mpd)
        self.send_down(xml_request)

    def finalization(self):
        pass


    def handle_xml_response(self, msg):
        print('Player().handle_xml_response()')

        self.parsed_mpd = parse_mpd(msg.get_payload())
        self.qi = self.parsed_mpd.get_qi()

        self.request_segment()


    def handle_segment_size_response(self, msg):
        print('Player().handle_segment_size_response()')

        print(msg)

        pass



    def handle_xml_request(self, msg):
        pass

    def handle_segment_size_request(self, msg):
        pass
