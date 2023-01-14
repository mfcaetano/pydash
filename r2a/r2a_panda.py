from r2a.ir2a import IR2A
from player.parser import *
import time
from statistics import mean


class R2A_PANDA(IR2A):

    def __init__(self, id):
        IR2A.__init__(self, id)
        self.vazoes = [] #vazões estimadas
        self.vazoes_alvo = [] #vazões alvo obtidas a partir do calculo do algoritmo PANDA
        self.vazoes_suavizadas = [] #vazões alvo obtidas a partir do calculo do algoritmo PANDA
        self.tempo_requisicao = 0
        self.historico_rtt = [] #historico de RTT para cálculos do algoritmo
        self.qualidades = []
        self.id_qualidade_selecionada = 0
        self.tempo_ate_pedido = 0 #tempo entre pedidos no servdor

    def retorna_tamanho_buffer(self):
        lista_buffers = self.whiteboard.get_playback_buffer_size()

        #
        if len(lista_buffers) > 0:
            return lista_buffers[-1][1]
        else:
            return 0

    def estimar_vazao_alvo(self):
        k = 0.9 #taxa de convergência de sondagem
        w = 30000#taxa de aumento aditivo
        T_anterior = self.historico_rtt[-1]
        
        if len(self.vazoes_alvo) > 0:
            vazao_estimada_anterior = self.vazoes_alvo[-1]
        else:
            vazao_estimada_anterior = self.vazoes[-1] #Analisar ainda o que devo botar aqui

        if len(self.vazoes_suavizadas) > 0:
            vazao_calculada_anterior = self.vazoes_suavizadas[-1]
        else:
            vazao_calculada_anterior = self.vazoes[-1] -1000 #Analisar ainda o que devo botar aqui

        vazao_estimada = ((k * (w - max(0,vazao_estimada_anterior - vazao_calculada_anterior + w))) * T_anterior) + vazao_estimada_anterior
        self.vazoes_alvo.append(vazao_estimada)
        
        return vazao_estimada

    def suavizar_estimativa(self,estimativa):
        while len(self.vazoes_alvo) > 5:
            self.vazoes_alvo.pop(0)

        if len(self.vazoes_alvo) < 1:
            self.vazoes_alvo.append(self.vazoes[-1])

        #lista_vazoes = self.vazoes_alvo
        #media_vazoes = sum(lista_vazoes) / len(lista_vazoes)

        estimativa_suavizada = ( mean(self.vazoes_alvo) + estimativa) / 2

        self.vazoes_suavizadas.append(estimativa_suavizada)
        return estimativa_suavizada

    def corresponder_qualidade(self, estimativa_suavizada):

        qi_selecionada = self.qualidades[0]
        for x in self.qualidades:
            if estimativa_suavizada > x:
                qi_selecionada = x

        return qi_selecionada

    #Relacionado ao traffic_shapping_interval
    def planejar_intervalo_download(self,qualidade_selecionada,estimativa_suavizada):
        beta = 0.2 #taxa de convergência
        ultimo_buffer = self.retorna_tamanho_buffer()
        buffer_minimo = 2
        t_segmento = 1 # 1 segundo de duração do segmento de vídeo

        tempo_estimado = ((qualidade_selecionada * t_segmento)/estimativa_suavizada) + ( beta * (ultimo_buffer - buffer_minimo))

        if tempo_estimado > 0:
            return tempo_estimado
        else:
            return 0

    def handle_xml_request(self, msg):
        self.tempo_requisicao = time.perf_counter()
        #time.sleep(self.tempo_ate_pedido)
        self.send_down(msg)

    def handle_xml_response(self, msg):

        parsed_mpd = parse_mpd(msg.get_payload())
        self.qualidades = parsed_mpd.get_qi()
        #self.id_qualidade_selecionada = (len(self.qualidades) // 3)

        rtt = time.perf_counter() - self.tempo_requisicao #Cálculo do Round Trip Time
        self.historico_rtt.append(rtt) #adição do RTT calculado à lista
        self.vazoes.append(msg.get_bit_length() / rtt)


        time.sleep(self.tempo_ate_pedido)
        self.send_up(msg)

    def handle_segment_size_request(self, msg):

        print("\n\n==================================")
        print("===== Vazao Anterior: ",self.vazoes[-1])
        #1) estimar a alocação de banda a se pedir na requisição
        vazao_estimada = self.estimar_vazao_alvo()
        print("===== Vazao estimada: ",vazao_estimada)
        #2) Suavizar a estimativa de banda
        vazao_suavizada = self.suavizar_estimativa(vazao_estimada)
        print("===== Vazao suavizada: ",vazao_suavizada)
        #3) Quantificar taxa de bits discreta pedida
        qualidade_selecionada = self.corresponder_qualidade(vazao_suavizada)
        print("===== Qualidade Selecionada: ", qualidade_selecionada)
        #4) Planejar tempo até enviar a próxima requisição
        self.tempo_ate_pedido = self.planejar_intervalo_download(qualidade_selecionada,vazao_suavizada)
        print("===== Tempo ate pedido: ", self.tempo_ate_pedido)
        print("==================================\n\n")

        self.tempo_requisicao = time.perf_counter()
        buffer_atual = self.retorna_tamanho_buffer()

        msg.add_quality_id(qualidade_selecionada)
        #time.sleep(tempo_ate_pedido)
        self.send_down(msg)

    def handle_segment_size_response(self, msg):
        rtt = time.perf_counter() - self.tempo_requisicao
        self.vazoes.append(msg.get_bit_length() / rtt)
        self.send_up(msg)


    def initialize(self):
        pass

    def finalization(self):
        pass
