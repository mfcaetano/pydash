from r2a.ir2a import IR2A
from player.parser import *
import time
from statistics import mean


class R2A_Tentativa(IR2A):

    def __init__(self, id):
        IR2A.__init__(self, id)
        self.vazoes = [] #vazões estimadas
        self.vazoes_alvo = [] #vazões alvo obtidas a partir do calculo do algoritmo PANDA
        self.tempo_requisicao = 0
        self.historico_rtt = [] #historico de RTT para cálculos do algoritmo
        self.qualidades = []
        self.id_qualidade_selecionada = 0

    def retorna_tamanho_buffer(self):
        lista_buffers = self.whiteboard.get_playback_buffer_size()

        #
        if len(lista_buffers) > 0:
            return lista_buffers[-1][1]
        else:
            return 0

    def estimar_vazao_alvo():
        k = 3 #taxa de convergência de sondagem
        w = 5 #taxa de aumento aditivo
        T_anterior = self.historico_rtt[-1]
        vazao_calculada_anterior = self.vazoes[-1]
        
        if len(self.vazoes_alvo):
            vazao_estimada_anterior = self.vazoes_alvo[-1]
        else:
            vazao_estimada_anterior = self.vazoes[-1] #Analisar ainda o que devo botar aqui

        vazao_estimada = ((k * (w - max(0,vazao_estimada_anterior - vazao_calculada_anterior + w))) * T) + vazao_estimada_anterior
        self.vazoes_alvo.append(vazao_estimada)
        
        return vazao_estimada

    def suavizar_estimativa():
        while len(self.vazoes_alvo) > 5:
            self.vazoes_alvo.pop(0)

        estimativa_suavizada = mean(self.vazoes_alvo)

        return estimativa_suavizada

    def corresponder_qualidade(estimativa_suavizada):
        for x in self.qualidades:
            if estimativa_suavizada > x:
                qualidade_selecionada = x

        return qualidade_selecionada

    def planejar_intervalo_download(qualidade_selecionada,estimativa_suavizada):
        beta = 2 #taxa de convergência
        ultimo_buffer = self.retorna_tamanho_buffer()
        buffer_minimo = 3

        tempo_estimado = ((qualidade_selecionada * t_segmento)/estimativa_suavizada) + beta * (ultimo_buffer - buffer_minimo)

        return tempo_estimado

    def handle_xml_request(self, msg):
        self.tempo_requisicao = time.perf_counter()
        self.send_down(msg)

    def handle_xml_response(self, msg):

        parsed_mpd = parse_mpd(msg.get_payload())
        self.qualidades = parsed_mpd.get_qi()
        self.id_qualidade_selecionada = (len(self.qualidades) // 3)

        rtt = time.perf_counter() - self.tempo_requisicao #Cálculo do Round Trip Time
        self.historico_rtt.append(rtt) #adição do RTT calculado à lista
        self.vazoes.append(msg.get_bit_length() / rtt)


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


    def initialize(self):
        pass

    def finalization(self):
        pass
