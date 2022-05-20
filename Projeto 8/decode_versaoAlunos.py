#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
from curses.ascii import FS
from tempfile import TemporaryDirectory
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
import peakutils
import funcoes_LPF as fc

#funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():
    #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    bola = signalMeu()

    sd.default.samplerate = 44100 #taxa de amostragem
    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa
    duration = 5 #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic
   
   #faca um print informando que a gravacao foi inicializada
    # print("-"*50)
    # print("Gravação iniciada")
    # print("-"*50)

    freqAmos    = 44100
    numAmostras = freqAmos*duration
    freqCorte   = 2500
    freq        = 13000

    input("Quer comecar ? ")
    audio = sd.rec(int(numAmostras), freqAmos, channels=1)
    sd.wait()

    sd.play(audio, freqAmos)
    sd.wait()

    bola.plotFFT(audio[:,0], freqAmos)
    plt.title("audio Capitado")
    # plt.show()

    x, s = bola.generateSin(freq, 1, 5, freqAmos)

    tone = audio[:,0]*s
    print (max(tone), min(tone))
    bola.plotFFT(tone, freqAmos)
    plt.title("audio com o seno")
    # plt.show()

    filter = fc.LPF(tone, freqCorte, freqAmos)
    bola.plotFFT(filter, freqAmos)
    plt.title("audio filtrado")
    plt.show()

    sd.play(filter, freqAmos)
    sd.wait()

if __name__ == "__main__":
    main()