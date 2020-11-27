# -*- coding: utf-8 -*-
"""
@author: Marcos F. Caetano (mfcaetano@unb.br) 11/03/2020

@description: PyDash Project

This is the player representation. It has the buffer and submit
segments requests to the lower layers. The Payer stores
the received segments in the buffer to be consumed later.
Also "watches" the movie and compute the statistics.
"""
import glob
import os
import threading
import time
from matplotlib import pyplot as plt

from base.configuration_parser import ConfigurationParser
from base.message import *
from base.simple_module import SimpleModule
from base.timer import Timer
from player.out_vector import OutVector
from player.parser import *
from base.whiteboard import Whiteboard

'''
quality_id - Taxa em que o video foi codificado (46980bps, ..., 4726737bps) 
qi         - indice de qualidade normalizado
segment_id - número de sequência do arquivo de video

Player is a Singleton class implementation

'''


class Player(SimpleModule):

    def __init__(self, id):
        SimpleModule.__init__(self, id)

        config_parser = ConfigurationParser.get_instance()

        self.buffering_until = int(config_parser.get_parameter('buffering_until'))
        self.max_buffer_size = int(config_parser.get_parameter('max_buffer_size'))
        self.playback_step = int(config_parser.get_parameter('playbak_step'))
        self.url_mpd = config_parser.get_parameter('url_mpd')

        # last pause started at time
        self.pause_started_at = None
        self.pauses_number = 0

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

        # initialize with the first segment sequence number to download
        self.segment_id = 1

        self.parsed_mpd = ''
        self.qi = []

        self.timer = Timer.get_instance()

        # threading playback
        self.playback_thread = threading.Thread(target=self.handle_video_playback)
        self.player_thread_events = threading.Event()
        self.lock = threading.Lock()
        self.kill_playback_thread = False

        self.request_time = 0

        self.playback_segment_size_time_at_buffer = []
        self.playback_qi = OutVector()
        self.playback_quality_qi = OutVector()
        self.playback_pauses = OutVector()
        self.playback = OutVector()
        self.playback_buffer_size = OutVector()
        self.throughput = OutVector()

        self.whiteboard = Whiteboard.get_instance()
        self.whiteboard.add_playback_history(self.playback.get_items())
        self.whiteboard.add_playback_qi(self.playback_qi.get_items())
        self.whiteboard.add_playback_pauses(self.playback_pauses.get_items())
        self.whiteboard.add_playback_buffer_size(self.playback_buffer_size.get_items())
        self.whiteboard.add_buffer(self.buffer)
        self.whiteboard.add_playback_segment_size_time_at_buffer(self.playback_segment_size_time_at_buffer)
        self.whiteboard.add_max_buffer_size(self.max_buffer_size)

    def get_qi(self, quality_qi):
        return self.qi.index(quality_qi)

    def get_amount_of_video_to_play_without_lock(self):
        video_data = len(self.buffer) - self.buffer_played
        self.whiteboard.add_amount_video_to_play(video_data)
        return video_data

    def get_amount_of_video_to_play(self):
        self.lock.acquire()
        video_data = len(self.buffer) - self.buffer_played
        self.lock.release()
        self.whiteboard.add_amount_video_to_play(video_data)
        return video_data

    def is_there_something_to_play(self):
        return bool(self.get_amount_of_video_to_play() > 0)

    def get_current_playtime_position(self):
        self.lock.acquire()
        player_position = self.buffer_played
        self.lock.release()

        return player_position

    def get_buffer_size(self):
        self.lock.acquire()
        bs = len(self.buffer)
        self.lock.release()
        return bs

    # called function every time a segment was played
    def handle_video_playback(self):
        while True:
            self.lock.acquire()
            current_time = self.timer.get_current_time()
            buffer_size = self.get_amount_of_video_to_play_without_lock()
            # print(f'{current_time} player acordou')

            # there is something to play
            if buffer_size > 0:
                # player thread is sleeping.
                if buffer_size >= self.max_buffer_size and not self.already_downloading:
                    print(f'{current_time} Acordar Player Thread!')
                    self.player_thread_events.set()
                    self.player_thread_events.clear()

                for i in range(self.playback_step):
                    qi = self.buffer[self.buffer_played]
                    self.playback_qi.add(current_time, qi)
                    self.playback_quality_qi.add(current_time, self.qi[qi])
                    self.playback.add(current_time, 1)

                    # compute the difference time from writing to read the segment in the buffer
                    #self.playback_segment_size_time_at_buffer[self.buffer_played] -= current_time
                    self.playback_segment_size_time_at_buffer[self.buffer_played][1] = current_time

                    self.buffer_played += 1

                buffer_size = self.get_amount_of_video_to_play_without_lock()
                self.playback_buffer_size.add(current_time, buffer_size)
                print(f'Execution Time {current_time} > buffer size: {buffer_size}')

                if self.pause_started_at is not None:
                    # pause_time = (time.time_ns() - self.pause_started_at) * 1e-9
                    pause_time = current_time - self.pause_started_at
                    self.playback_pauses.add(current_time, pause_time)
                    self.pause_started_at = None
            else:
                # self.pause_started_at = time.time_ns()
                self.playback.add(current_time, 0)

                if self.pause_started_at is None:
                    self.pauses_number += 1
                    self.pause_started_at = current_time

            # update buffer_size
            buffer_size = self.get_amount_of_video_to_play_without_lock()
            self.lock.release()

            if (not threading.main_thread().is_alive() or self.kill_playback_thread) and buffer_size <= 0:
                print(f'Execution Time {current_time}  thread {threading.get_ident()} will be killed.')
                break

            # playback steps
            # print(f'{current_time} player vai dormir')
            time.sleep(self.playback_step)

    def buffering_video_segment(self, msg):
        # buffer already stored the segment id
        buffer_size = self.get_buffer_size()
        if buffer_size >= ((msg.get_segment_id() - 1) * msg.get_segment_size() + 1):
            raise ValueError(f'buffer: {buffer_size}, {msg}')

        # adding the segment in the buffer
        self.store_in_buffer(self.get_qi(msg.get_quality_id()), msg.get_segment_size())

        # statistical purpose
        current_time = self.timer.get_current_time()
        buffer_size = self.get_amount_of_video_to_play()
        self.playback_buffer_size.add(current_time, buffer_size)
        print(f'Execution Time {current_time} > buffer size: {buffer_size}')

        if self.buffer_initialization and self.get_amount_of_video_to_play() >= self.buffering_until:
            self.buffer_initialization = False
            print(f'Execution Time {self.timer.get_current_time()} buffering process is concluded')
            self.playback_thread.start()

    def store_in_buffer(self, qi, segment_size):
        self.lock.acquire()
        current_time = self.timer.get_current_time()

        for i in range(segment_size):
            self.buffer.append(qi)

            # logging the time the segment size was written in the buffer
            self.playback_segment_size_time_at_buffer.append([current_time, -1])
        self.lock.release()

    def request_next_segment(self):
        if self.already_downloading:
            raise ValueError('Something doesn\'t look right, a segment is already being downloaded!')

        self.request_time = time.perf_counter()
        # self.request_time = self.timer.get_current_time()
        segment_request = SSMessage(MessageKind.SEGMENT_REQUEST)

        url_tokens = self.url_mpd.split('/')

        segment_request.add_host_name(url_tokens[2])
        segment_request.add_path_name('/'.join(url_tokens[:len(url_tokens) - 1]))
        segment_request.add_media_mpd(navigate_mpd(self.parsed_mpd, 'media')[1])
        segment_request.add_segment_id(self.segment_id)

        self.segment_id += 1

        # set status to downloading a segment
        self.already_downloading = True

        print(f'Execution Time {self.timer.get_current_time()} > request: {segment_request}')

        self.send_down(segment_request)

    def initialize(self):
        # starting the application downloading mdp file
        xml_request = Message(MessageKind.XML_REQUEST, self.url_mpd)
        self.send_down(xml_request)

    def finalization(self):

        print(f'Pauses number: {self.pauses_number}')

        [os.remove(f) for f in glob.glob('./results/*.png')]

        self.logging_all_statistics()

    def handle_xml_response(self, msg):
        self.parsed_mpd = parse_mpd(msg.get_payload())
        self.qi = self.parsed_mpd.get_qi()
        self.request_next_segment()

    def handle_segment_size_response(self, msg):

        # set status to not downloading a segment
        self.already_downloading = False

        current_time = self.timer.get_current_time()
        print(f'Execution Time {current_time} > received: {msg}')

        if msg.found():
            measured_throughput = msg.get_bit_length() / (time.perf_counter() - self.request_time)
            self.throughput.add(current_time, measured_throughput)

            print(f'Execution Time {self.timer.get_current_time()} > measured throughput: {measured_throughput}')

            # self.throughput.add(current_time, msg.get_bit_length() /(current_time - self.request_time))
            self.buffering_video_segment(msg)

            # still have space in buffer to download next ss
            if self.get_amount_of_video_to_play() >= self.max_buffer_size:
                print(
                    f'Execution Time {current_time} Maximum buffer size is achieved... the principal process will sleep now.')
                self.player_thread_events.wait()

            self.request_next_segment()

            '''
            if not self.is_buffer_achieve_max_size():
                self.request_next_segment()
            else:
                print('terminou o download... vamos encerrar')
                self.kill_playback_thread = True
                self.playback_thread.join()
            '''
        else:
            print(f'Execution Time {current_time} All video\'s segments was downloaded')
            self.kill_playback_thread = True
            if self.playback_thread.is_alive():
                self.playback_thread.join()

    def logging_all_statistics(self):
        self.log(self.playback_quality_qi, 'playback_quality_qi', 'Quality QI', 'bps')
        self.log(self.playback_pauses, 'playback_pauses', 'Pauses Size', 'Pauses Size')
        self.log(self.playback, 'playback', 'Playback History', 'on/off')
        self.log(self.playback_qi, 'playback_qi', 'Quality Index', 'QI')
        self.log(self.playback_buffer_size, 'playback_buffer_size', 'Buffer Size', 'seconds')
        self.log(self.throughput, 'throughput', 'Throughput Variation', 'bps')

    def log(self, log, file_name, title, y_axis, x_axis='execution time (s)'):
        items = log.items

        if len(items) == 0:
            return

        x = []
        y = []
        for i in range(len(items)):
            x.append(items[i][0])
            y.append(items[i][1])

        plt.plot(x, y, label=file_name)
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title(title)

        plt.savefig(f'./results/{file_name}.png')
        plt.clf()
        plt.cla()
        plt.close()

    def handle_xml_request(self, msg):
        # not applied
        pass

    def handle_segment_size_request(self, msg):
        # not applied
        pass
