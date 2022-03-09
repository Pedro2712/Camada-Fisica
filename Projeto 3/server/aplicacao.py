from enlace import *
import time
import os
from animation import animation
from funcao import *

serialName = "COM5"

def tempo_decorrido(temp):
    os.system("cls")
    print ("A recepção vai começar!")
    print (f"Tempo decorrido é: {temp}")

def main():
    
    try:
        com1 = enlace(serialName)
        recebe= animation()
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        
        os.system("cls")
        print ("A recepção vai começar!") 
        # Acesso aos bytes recebidos
        bit_de_termino= b'\xff\xff\xff\xff'
        mensagem =[]
        cont = 0
        while True:
            while True:
                rxBuffer, nRx = com1.getData(1)
                recebe.enable()
                if rxBuffer.endswith(bit_de_termino):
                    break
                time.sleep(0.5)
            
            head, estilo, tam_pacotes, contador, tamanho, playload, eop = desmembramento(rxBuffer)

            # if estilo == b'a':

            #     #FAZER O SEND DATA
            #     continue

            if estilo == b'b':
                cont+=1
                #FAZER SEND
                mensagem.append(playload)
                if cont == contador:
                    break
        recebe.disable()
        
        print(mensagem)
        print(len(mensagem))
        # print(mensagem.join(""))
        
        # # Calcula a quantidade de comandos enviados e o transforma em hexadecimal
        # n_rxBuffer= bytes([len(str(rxBuffer).split('/'))-1])
        # print("-" * 50)

        # print("A transmissão vai começar")
        # # Envia a quantidade de comandos para o client em hexadecimal
        # print(f"Enviando o número de comandos de: {len(str(rxBuffer).split('/'))-1}")
        # com1.sendData(np.asarray(n_rxBuffer))

        # Encerra comunicação
        print("-" * 50)
        print("Comunicação encerrada!")
        print("-" * 50)
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    # Só roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
