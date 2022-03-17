from enlace import *
import time
import numpy as np
import os
from funcao import *
from animacao import Animacao

serialName = "COM3"


def main():
    
    try:
        com1 = enlace(serialName) 
        recebe = Animacao()
        com1.enable()

        imageR= "./imgs/image.png"

        with open(imageR, 'rb') as arquivo:
            m= arquivo.read()
        
        os.system("cls")
        tempo_i= time.ctime()

        print ("A transmissão vai começar!")
        print ("A recepção vai começar!")

        bit_de_termino= b'\xff\xff\xff\xff'
        index = 0
        sla= 0
        mensagem= cria_pacote(mensagem=m, estilo= 'p')
        # mensagem= [b'pa001262--\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\xc8\x00\x00\x00\x96\x08\x06\x00\x00\x00\x9b\xdc\xc7\x19\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00 cHRM\x00\x00z&\x00\x00\x80\x84\x00\x00\xfa\x00\x00\x00\x80\xe8\x00\x00u0\x00\x00\xea`\x00\x00:\x98\x00\x00\x17p\x9c\xbaQ<\x00\x00\x00\x06bKGD\x00\x00\x00\x00\x00\x00\xf9C\xbb\x7f\x00\x00\x00\xff\xff\xff\xff']
        while True:
            while True:
                if com1.rx.condicao:
                    txBuffer= cria_pacote()
                    com1.sendData(np.asarray(txBuffer[0]))
                rxBuffer, nRx = com1.getData(1)
                if rxBuffer.endswith(bit_de_termino):
                    if com1.rx.condicao_print: recebe.printProgressBar(0, len(mensagem), prefix = 'Progress:', suffix = 'Complete', length = 50)
                    com1.clear(len(rxBuffer))
                    com1.rx.cond()
                    break
                time.sleep(0.05)
            head, estilo, tam_pacotes, contador, tamanho, payload, eop = desmembramento(rxBuffer)

            if estilo == b'e':
                index = int(payload.decode("utf-8")) - 1
                
                com1.sendData(np.asarray(mensagem[index]))
                time.sleep(0.05)
                index+= 1

            elif estilo == b'v': # Tá vivo?
                txBuffer= cria_pacote(estilo= "t")
                com1.sendData(np.asarray(txBuffer[0]))
                time.sleep(0.05)

            elif estilo == b't': # Pode mandar!
                if index > len(mensagem) - 1:
                    stop= cria_pacote(estilo= "d")
                    com1.sendData(np.asarray(stop[0]))
                    time.sleep(0.05)
                    break
                # if sla == 20:
                #     index= index + 20
                # sla+= 1
                com1.sendData(np.asarray(mensagem[index]))
                time.sleep(0.05)
                recebe.printProgressBar(index + 1, len(mensagem), prefix = 'Progress:', suffix = 'Complete', length = 50)
                index+= 1

            elif estilo == b'd': # Deu tudo certo!
                print("Deu tudo certo!")
                break
                
        tempo_f     = time.ctime()
        tempo_total = calcula_tempo(tempo_i, tempo_f)
        
        # Encerra comunicação
        os.system("cls")
        print("-" * 50)
        print("Comunicação encerrada!")
        print(f"Tempo decorrido foi de: {tempo_total}")
        print("-" * 50)
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    # Só roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
