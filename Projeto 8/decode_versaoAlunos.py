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

#funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():

    DTMF = {"1": [697,1206], "2": [697,1339], "3": [697,1477], "A": [697, 1633],
            "4": [770,1206], "5": [770,1339], "6": [770,1477], "B": [770, 1633],
            "7": [852,1206], "8": [852,1339], "9": [852,1477], "C": [852, 1633],
            "X": [941,1206], "0": [941,1339], "#": [941,1477], "D": [941, 1633]} 


    #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    bola = signalMeu()
 
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    sd.default.samplerate = 44100 #taxa de amostragem
    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa
    duration = 3 #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic
    # faca um printo na tela dizendo que a captacao comecará em n segundos. e entao 
    print(f"Captação de som irar começar em {duration} segundos....")
    time.sleep(duration)
    #use um time.sleep para a espera
   
   #faca um print informando que a gravacao foi inicializada
    print("-"*50)
    print("Gravação iniciada")
    print("-"*50)

   
    #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 

    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
    freqAmos    = 44100
    numAmostras = freqAmos*duration

    audio = sd.rec(int(numAmostras), freqAmos, channels=1)
    sd.wait()
    print("FIM!!!!")
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    #grave uma variavel com apenas a parte que interessa (dados)
    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    tempo = np.linspace(0, duration, duration*freqAmos)

    # plot do gravico  áudio vs tempo!
    plt.plot(tempo, audio[:,0])
    plt.xlabel("Tempo")
    plt.ylabel("Audio")
    
    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    x, y = bola.calcFFT(audio[:,0], freqAmos)

    plt.figure("F(y)")
    plt.plot(x,y)
    plt.grid()
    plt.title('Fourier audio')
   
    index = peakutils.indexes(y, thres = 0.3 , min_dist = 100)
    
    #printe os picos encontrados!  
    print(f"Os picos são: {index}")
    valoresPico=[]
    for freq in x[index]:
        valoresPico.append(freq)

    tolerancia = 50
    freqMin = [697, 770, 852, 941]; freqMax = [1206, 1339, 1477, 1633]
    linha = 0; coluna = 0
    for pico in valoresPico:
        for value in freqMin:
            if value-tolerancia < pico < value+tolerancia:
                linha = value
        for value2 in freqMax:
            if value2-tolerancia < pico < value2+tolerancia:
                coluna = value2

    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    
    print(f"A frequencia encontrados foram de: {coluna}")
    # print(linha)
    
    key_list = list(DTMF.keys())
    val_list = list(DTMF.values())

    posicao = val_list.index([linha,coluna])
    print(f"tecla: {key_list[posicao]}")

    ## Exibe gráficos
    plt.show()

if __name__ == "__main__":
    main()