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
import numpy as np
import time

class r2aPandas(IR2A):

    def __init__(self, id):
        IR2A.__init__(self, id)
        self.parsed_mpd = ''

    def handle_xml_request(self, msg):
        self.pandas.update_request(time.perf_counter())
        self.send_down(msg)

    def handle_xml_response(self, msg):
        # getting qi list
        self.parsed_mpd = parse_mpd(msg.get_payload())
        self.pandas.qi = np.array(self.parsed_mpd.get_qi())
        if(self.n==0): self.initpandas()
        self.send_up(msg)

    def handle_segment_size_request(self, msg):
        msg.add_quality_id(self.pandas.get_quality())
        self.send_down(msg)

    def handle_segment_size_response(self, msg):
        self.pandas.update_response(time.perf_counter())
        self.send_up(msg)

    def initialize(self):
        self.pandas = Pandas()

    def finalization(self):
        pass


class Pandas:
    def __init__(self, w=0.3, k=0.14, beta=0.2, alfa=0.2, e=0.15, t=0, b=0, 
                 bmin=26, r=0, deltaup=0, deltadown=0, trequest=0, tresponse=0, 
                 n=-1, tnd=[0], tr=[], td=[0], x=[]):
        self.trequest = trequest
        self.tresponse = tresponse
        self.n     = n
        self.w     = w     # taxa de bits de aumento aditivo de sondagem
        self.k     = k     # taxa de convergência de sondagem
        self.beta  = beta  # taxa de convergência do buffer do cliente
        self.alfa  = alfa  # Taxa de convergência de suavização
        self.e     = e     # margem de segurança multiplicativa
        self.t     = t     # duração do segmento de vídeo
        self.b     = b     # duração do buffer do cliente
        self.bmin  = bmin  # duração mínima do buffer do cliente
        self.r     = r     # taxa de bits de video disponível em qui
        self.tnd   = tnd   # tempo alvo entre as solicitações
        self.tr    = tr    # tempo real entre as solicitações
        self.td    = td    # duração do download
        self.x     = x     # taxa média de dados alvo (ou compartilhamento de largura de banda)
        self.y     = []    # versão suavizada de x
        self.z     = []    # taxa de tranferência de TCP medida z=rt/T'
        self.qi    = np.array([])    # Conjunto de taxas de bits de video
        self.deltaup   = deltaup     # margem de segurança para cima 
        self.deltadown = deltadown   # margem de segurança para baixo

    def initpandas(self):
        idx_x0 = self.qi.size/2
        x0 = self.qi[int(idx_x0)]
        self.x.append(x0)
        self.y.append(x0)
        self.z.append(x0)    


    def estimate_xn(self):
        self.tr.append(max(self.tnd[-1], self.td[-1]))
        m = max(0, self.x[-1]-self.z[-1]+self.w)
        xn = self.x[-1] + self.k*self.tnd[-1]*(self.w - m)
        self.x.append(xn)
    
    def get_quality(self):
        self.estimate_xn()
        self.S()
        self.Q()
        tTarget_inter_request()
        return self.r[-1]

    def S(self):
        self.y.append(self.y[-1] - self.tr[-1] * self.alfa * (self.y[-1] - self.x[-1]))
    
    def Q(self):
        self.deltaup = self.e * self.y[-1]
        rup = self.get_rup()
        rdown = self.get_rdown()
        rn = 0
        if(self.r[-1] < rup): rn = rup
        elif(rup <= self.r[-1] and self.r[-1] <= rdown): rn = self.r[-1]
        else: rn = rdown
        self.r.append(rn)
    
    def get_rup(self):
        y = self.y[-1] - self.deltaup
        qi2 = self.qi[self.qi <= y]
        return qi2[-1]
    
    def get_rdown(self):
        y = self.y[-1] - self.deltadown
        qi2 = self.qi[self.qi <= y]
        return qi2[-1]

    def tTarget_inter_request(self):
        if(self.n==0): self.b = (1-self.r[-1]/self.y[-1])*self.t/self.beta + self.bmin
        tnd = self.r[-1]*self.t/self.y[-1] + self.beta*(self.b[-1] - self.bmin)
        self.tnd.append(tnd)

    def put_tresponse(self):
        pass

    def get_rate(self):
        pass

    def get_buffersize(self, b):
        self.b = b
        pass
    
    def update_response(self, actual_tresponse):
        self.tresponse = actual_tresponse
        self.td = self.tresponse - self.trequest 
        self.z.append((self.r[-1]*self.t)/self.td[-1])
    
    def update_request(self, actual_trequest):
        self.n += 1
        self.trequest = actual_trequest
        self.pandas.b(self.whiteboard.get_playback_buffer_size())


