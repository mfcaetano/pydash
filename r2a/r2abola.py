from r2a.ir2a import IR2A
from player.parser import *
import numpy as np
import time

# Esta classe pretende representar o algoritimo ABR usando a implementação BOLA.


class R2ABola(IR2A):

    def __init__(self, id):
        IR2A.__init__(self, id)
        self.qi = []
        self.throughput = 0
        self.request_time = 0
        self.vM = 0

    def handle_xml_request(self, msg):
        self.send_down(msg)

    def handle_xml_response(self, msg):
        # executar o parser do arquivo
        parsed_mpd = parse_mpd(msg.get_payload())
        self.qi = parsed_mpd.get_qi()
        # enviar a resposta
        self.send_up(msg)

    def handle_segment_size_request(self, msg):
        print('Enter in ABR algorithm')
        # O video foi segmentado de 6 maneiras diferentes e codificado em 20 formatos distintos
        QTD_FORMAT = 20

        #  Tamanho maximo do buffer
        Q_MAX = self.whiteboard.get_max_buffer_size()

        # Implementacao dinamica
        # T_MIN = min(t_in, t_out)
        # T_RES = max((T_MIN/2), 3)
        # Q_MAX = min(Q_MAX, T_RES)

        #  GAMMA_PARAMETER corresponde à intensidade com que queremos evitar o rebuffering.
        #  TODO -  Deveria ser um valor dinamico, mas por simplicidade esta sendo inicializado manualmente
        GAMMA_PARAMETER = 5

        # time.perf_counter() retorna o tempo em que a mensagem será encaminhada para o singletton ConnectionHandler
        # request_time será usada posteriormente para calcular o valor de throughput
        self.request_time = time.perf_counter()

        # Um desafio de implantação envolve a escolha do BOLA parâmetros γ(GAMMA_PARAMETER) e V(PARAM).
        # Parâmetro de controle definido pelo Bola para possibilitar troca entre o tamanho do buffer e desempenho
        PARAM = ((Q_MAX - 1) / self.vM) + GAMMA_PARAMETER

        # Salva em buffers = A lista de tamanho dos buffers
        buffers = self.whiteboard.get_playback_buffer_size()

        # salva em playback_qi = A lista com o índice de qualidade do vídeo
        playback_qi = self.whiteboard.get_playback_qi()

        # Ennquanto o video não tem inicio o buffer é definido como 0
        if not buffers:
            buffers = ([0, 0], [0, 0])

        m = 0
        # Seleciona o valor mais atual para o nível do buffer
        current_buffer = buffers[-1]

        # Escolhe o indice de qualidade
        for i in range(QTD_FORMAT):
            utility = np.log(self.qi[i] / self.qi[0])
            m_candidate = (PARAM * utility + PARAM * 5 -
                           current_buffer[1]) / self.qi[i]

            # Define o maior valor para a variavel m_candidate
            if m < m_candidate:
                m = m_candidate
                selected_qi = i

            # Verifica a lista com o índice de qualidade do vídeo
            if playback_qi:
                # Verifica se indice de qualidade definido é maior que o indice do segmento anterior,
                if selected_qi > playback_qi[-1][1]:
                    m1 = 0
                    max = self.qi[0]
                    if (self.throughput >= self.qi[0]):
                        max = self.throughput
                    for j in range(20):
                        if (m1 <= j and self.qi[j] <= max):
                            m1 = j
                    # O indice é setado com um novo valor caso ele esteja incluido nos  indices antigos
                    # Pro caso contrário o indice é setado com o valor do indice antigo
                    if (m1 < playback_qi[-1][1]):
                        m1 = playback_qi[-1][1]
                    elif (m1 >= m):
                        m1 = selected_qi
                    else:
                        m1 += 1

                    selected_qi = m1
            # Possivel abandono
            # TODO - Implementar metodo de pausa
            else:
                m1 = selected_qi
                selected_qi = m1
                # selected_qi = max((Q_MAX + 1), 0)

        msg.add_quality_id(self.qi[selected_qi])
        self.send_down(msg)

    def handle_segment_size_response(self, msg):
        self.vM = np.log(msg.get_quality_id() / self.qi[0])

        # tempDuracao = tempo de duração entre a ida e a volta da mensagem ao ConnectionHandler
        tempDuracao = time.perf_counter() - self.request_time

        # Determina o throughput sobre a requisição do segmento de vídeo
        self.throughput = msg.get_bit_length() / tempDuracao

        self.send_up(msg)

    def initialize(self):
        pass

    def finalization(self):
        pass
