import json
from player.out_vector import Out_Vector
from base.simple_module import Simple_Module

'''
quality_id - Taxa em que o video foi codificado (46980bps, ..., 4726737bps) 
qi         - indice de qualidade normalizado
segment_id - número de sequência do arquivo de video

Player is a Singleton class implementation

'''


class Player(Simple_Module):


    def __init__(self, id):

        Simple_Module.__init__(self, id)

        with open('player/player.json') as f:
            player_parameters = json.load(f)

        self.buffer_size = int(player_parameters['buffer_size'])
        self.buffering_until = int(player_parameters['buffering_until'])
        self.max_buffer_size = int(player_parameters['max_buffer_size'])
        self.playback_step = int(player_parameters['playbak_step'])
        self.url_mpd = player_parameters['url_mpd']

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

    def initialize(self):
        pass

    def finalization(self):
        pass

    def handle_message(self, msg):
        print(f'Player recebi uma msg {msg.get_payload()}')
        pass
