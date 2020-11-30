# -*- coding: utf-8 -*-
"""
@author: Hevelyn Sthefany L. Carvalho 
@author: Giordano Suffert Monteiro 
@author: Abel Augustu Alves Moreira
@date: 30/11/2020
@description: PyDash Project

An implementation example of a PANDAS Algorithm.

"""

from player.parser import *
from r2a.ir2a import IR2A


class r2aPandas(IR2A):

    def __init__(self, id):
        IR2A.__init__(self, id)
        self.parsed_mpd = ''

    def handle_xml_request(self, msg):
        self.pandas.b(self.whiteboard.get_playback_buffer_size())
        self.send_down(msg)

    def handle_xml_response(self, msg):
        # getting qi list
        self.parsed_mpd = parse_mpd(msg.get_payload())
        self.pandas.qi = self.parsed_mpd.get_qi()
        self.send_up(msg)

    def handle_segment_size_request(self, msg):
        # time to define the segment quality choose to make the request
        msg.add_quality_id(self.pandas.estimate_rn())
        self.pandas.put_trequest()
        self.send_down(msg)

    def handle_segment_size_response(self, msg):
        self.pandas.put_trequest()
        self.pandas.get_rate()
        self.send_up(msg)

    def initialize(self):
        self.pandas = Pandas()

    def finalization(self):
        pass


class Pandas:
    def __init__(self, w=0.3, k=0.14, beta=0.2, alfa=0.2, e=0.15, t=0, b=0, 
                 bmin=26, r=0, deltaup=0, deltadown=0, n=0):
        self.trequest = 0
        self.tresponse = 0
        self.n     = n
        self.w     = w     # taxa de bits de aumento aditivo de sondagem
        self.k     = k     # taxa de convergência de sondagem
        self.beta  = beta  # taxa de convergência do buffer do cliente
        self.alfa  = alfa  # Taxa de convergência de suavização
        self.e     = e     # margem de segurança multiplicativa
        self.t     = t     # duração do segmento de vídeo
        self.b     = b     # duração do buffer do cliente
        self.bmin  = bmin  # duração mínima do buffer do cliente
        self.tr    = []    # tempo real entre as solicitações
        self.ta    = []    # tempo alvo entre as solicitações
        self.x     = []    # taxa média de dados alvo (ou compartilhamento de largura de banda)
        self.y     = []    # versão suavizada de x
        self.z     = []    # taxa de tranferência de TCP medida z=rt/T'
        self.qi    = []    # Conjunto de taxas de bits de video
        self.r     = r     # taxa de bits de video disponível em R
        self.deltaup   = deltaup     # margem de segurança para cima 
        self.deltadown = deltadown   # margem de segurança para baixo

    def estimate_xn(self):
        pass
    
    def estimate_rn(self):
        pass

    def S(self):
        pass
    
    def Q(self):
        pass

    def get_rup(self):
        pass
    
    def get_rdown(self):
        pass

    def put_trequest(self):
        pass

    def put_tresponse(self):
        pass

    def get_rate(self):
        pass

    def get_buffersize(self, b):
        self.b = b
        pass
    