#importe as bibliotecas
from pyrsistent import plist
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import soundfile as sf
import funcoes_LPF as fc

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
    bola    = signalMeu()
    musica  = 'queen.wav'

    fs      = 44100
    fsCorte = 2500
    freq    = 13000
    som, f  = sf.read(musica, dtype= "float32")

    filter= fc.LPF(som[:220500], fsCorte, fs)

    x, s = bola.generateSin(freq, 1, int(len(som[:220500])/fs), fs)

    tone = filter*s
    print(max(tone), min(tone))

    input("Quer comecar o audio ? ")
    sd.play(tone, fs)
    sd.wait()

    # bola.plotFFT(tone, fs)
    # plt.show()

    # saida= tone*s
    # bola.plotFFT(saida, fs)
    # plt.show()

    # filter2= fc.LPF(saida, fsCorte, fs)

    # bola.plotFFT(filter2, fs)
    # plt.show()

    # sd.play(filter2, fs)
    # sd.wait()
    

if __name__ == "__main__":
    main()
