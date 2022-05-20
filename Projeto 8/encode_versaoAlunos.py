#importe as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

#funções a serem utilizadas
# def signal_handler(signal, frame):
#         print('You pressed Ctrl+C!')
#         sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)




def main():
    
    DTMF= {"1": [1206, 697], "4": [1206, 770], "7": [1206, 852], "X": [1206, 941],
           "2": [1339, 697], "5": [1339, 770], "8": [1339, 852], "0": [1339, 941],
           "3": [1477, 697], "6": [1477, 770], "9": [1477, 852], "#": [1477, 941],
           "A": [1633, 697], "B": [1633, 770], "C": [1633, 852], "D": [1633, 941],}
   
    #********************************************instruções*********************************************** 
    # seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada
    # então inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF
    # agora, voce tem que gerar, por alguns segundos, suficiente para a outra aplicação gravar o audio, duas senoides com as frequencias corresposndentes à tecla pressionada, segundo a tabela DTMF
    # se voce quiser, pode usar a funcao de construção de senoides existente na biblioteca de apoio cedida. Para isso, você terá que entender como ela funciona e o que são os argumentos.
    # essas senoides tem que ter taxa de amostragem de 44100 amostras por segundo, entao voce tera que gerar uma lista de tempo correspondente a isso e entao gerar as senoides
    # lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t)
    # o tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Seja razoável.
    # some as senoides. A soma será o sinal a ser emitido.
    # utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    # grave o som com seu celular ou qualquer outro microfone. Cuidado, algumas placas de som não gravam sons gerados por elas mesmas. (Isso evita microfonia).
    
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado. Como as frequencias sao relativamente altas, voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
    bola= signalMeu()
    while True:
        tecla = input("Digite alguma letra: ")
        if tecla in DTMF.keys():
            break
        print ("Digite uma letra que está no teclado numérico DTMF")
    
    freq_1= DTMF[tecla][0]
    freq_2= DTMF[tecla][1]
    fs= 44100
    time= 2
    amplitude= 0.25

    graf=np.linspace(0.0, time, int(fs/100))

    x_1, s_1  = bola.generateSin(freq_1, amplitude, time, fs)
    x_2, s_2  = bola.generateSin(freq_2, amplitude, time, fs)

    tone= s_1+s_2

    print("Inicializando encoder")
    print("Aguardando usuário")
    print("Gerando Tons base")
    print("Executando as senoides (emitindo o som)")
    print("Gerando Tom referente ao símbolo : {}".format(tecla))
    sd.play(tone, fs)
    # Exibe gráficos
    # aguarda fim do audio
    sd.wait()
    plt.plot(graf, tone[0:441])
    bola.plotFFT(tone, fs)
    plt.show()
    

if __name__ == "__main__":
    main()
