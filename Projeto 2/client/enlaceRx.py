#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time

# Threads
import threading
import enlaceTx as tx
import aplicacao as ap

import time

# Class
class RX(object):
  
    def __init__(self, fisica):
        self.fisica      = fisica
        self.buffer      = bytes(bytearray())
        self.threadStop  = False
        self.threadMutex = True
        self.READLEN     = 1024

    def thread(self): 
        while not self.threadStop:
            if(self.threadMutex):
                rxTemp, nRx = self.fisica.read(self.READLEN)
                if (nRx > 0):
                    self.buffer += rxTemp
                time.sleep(0.01)

    def threadStart(self):       
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        self.threadStop = True

    def threadPause(self):
        self.threadMutex = False

    def threadResume(self):
        self.threadMutex = True

    def getIsEmpty(self):
        if(self.getBufferLen() == 0):
            return(True)
        else:
            return(False)

    def getBufferLen(self):
        return(len(self.buffer))

    def getAllBuffer(self, len):
        self.threadPause()
        b = self.buffer[:]
        self.clearBuffer()
        self.threadResume()
        return(b)

    def getBuffer(self):
        # Pausa o thread
        self.threadPause()
        b           = self.buffer # Salva os dados do buffer na variavel b
        # self.clearBuffer() # Zera o buffer
        self.threadResume()
        return(b)

    def getNData(self, size):
        time_i= time.ctime()
        while self.getBufferLen() < size:
            time_f= time.ctime()
            tempo_total= ap.calcula_tempo(time_i, time_f)
            ap.tempo_decorrido(tempo_total)
            if tempo_total == "00:00:10":
                print("-" * 50)
                print ("Time Out", "\U0001F615")
                break
            time.sleep(0.9)
        return(self.getBuffer())

    def clearBuffer(self):
        self.buffer = b""
