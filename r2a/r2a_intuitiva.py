from r2a.ir2a import IR2A
from player.parser import *
import time
from statistics import mean


class R2A_Intuitiva(IR2A):

    def __init__(self, id):
        IR2A.__init__(self, id)
        self.vazoes = []
        self.tempo_requisicao = 0
        self.qualidades = []
        self.id_qualidade_selecionada = 0

    def handle_xml_request(self, msg):
        self.tempo_requisicao = time.perf_counter()
        self.send_down(msg)

    def handle_xml_response(self, msg):

        parsed_mpd = parse_mpd(msg.get_payload())
        self.qualidades = parsed_mpd.get_qi()
        self.id_qualidade_selecionada = (len(self.qualidades) // 3)

        rtt = time.perf_counter() - self.tempo_requisicao
        self.vazoes.append(msg.get_bit_length() / rtt)

        while len(self.vazoes) > 5:
            self.vazoes.pop(0)

        self.send_up(msg)

    def handle_segment_size_request(self, msg):
        self.tempo_requisicao = time.perf_counter()
        ultima_vazao = self.vazoes[-1]
        buffer_atual = self.retorna_tamanho_buffer()

        if buffer_atual > 15:
            if ultima_vazao > mean(self.vazoes):
                if self.id_qualidade_selecionada <= (len(self.qualidades) - 5):
                    self.id_qualidade_selecionada += 4
                else:
                    self.id_qualidade_selecionada = len(self.qualidades) - 1
            else:
                if self.id_qualidade_selecionada <= (len(self.qualidades) - 2):
                    self.id_qualidade_selecionada += 1
                else:
                    self.id_qualidade_selecionada = len(self.qualidades) - 1
        elif buffer_atual <= 15 and buffer_atual > 3:
            if ultima_vazao > mean(self.vazoes):
                if self.id_qualidade_selecionada <= (len(self.qualidades) - 3):
                    self.id_qualidade_selecionada += 2
                else:
                    self.id_qualidade_selecionada = len(self.qualidades) - 1
            else:
                if self.id_qualidade_selecionada >= 4:
                    self.id_qualidade_selecionada -= 4
                else:
                    self.id_qualidade_selecionada = 0
        else:
            self.id_qualidade_selecionada = 0

        qualidade_selecionada = self.qualidades[self.id_qualidade_selecionada]

        msg.add_quality_id(qualidade_selecionada)
        self.send_down(msg)

    def handle_segment_size_response(self, msg):
        rtt = time.perf_counter() - self.tempo_requisicao
        self.vazoes.append(msg.get_bit_length() / rtt)
        self.send_up(msg)

    def retorna_tamanho_buffer(self):
        lista_buffers = self.whiteboard.get_playback_buffer_size()

        if len(lista_buffers) > 0:
            return lista_buffers[-1][1]
        else:
            return 0

    def initialize(self):
        pass

    def finalization(self):
        pass
