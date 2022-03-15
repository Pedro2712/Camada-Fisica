from enlace import *
import time
import numpy as np
import os
from funcao import *
from animacao import Animacao
from PIL import Image

serialName = "COM4"

mensagem = """sapucaiba sapucaiba"""

def main():
    
    try:
        com1 = enlace(serialName)
        # recebe= Animacao()
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        imageW= "./imgs/recebidaCopia.png"
        
        com1.enable()
        
        os.system("cls")
        print ("A recepção vai começar!")

        # Acesso aos bytes recebidos
        bit_de_termino= b'\xff\xff\xff\xff'
        lista_mensagem =[]
        count = 1
        while True:
            while True:
                rxBuffer, nRx = com1.getData(1)
                if rxBuffer.endswith(bit_de_termino):
                    com1.rx.cond()
                    com1.clear(len(rxBuffer))
                    break
                time.sleep(0.05)
            
            head, estilo, tam_payload, contador, tamanho, payload, eop = desmembramento(rxBuffer)

            if estilo == b'v': # Tá vivo?
                txBuffer= cria_pacote(estilo= 't')
                com1.sendData(np.asarray(txBuffer[0]))
                time.sleep(0.05)

            elif estilo == b'p': # Pacote
                print(f"tamanho do payload: {tam_payload}, tamanho real: {len(payload)}")
                print(f"contador do payload: {contador}, contador real: {count}, TOTAL: {tamanho}")
                print("-"*50)
                if contador == count and tam_payload == len(payload):
                    lista_mensagem.append(payload)
                    txBuffer= cria_pacote(estilo= 't')
                    com1.sendData(np.asarray(txBuffer[0]))
                    time.sleep(0.05)
                    count+= 1
                else:
                    print ("\033[31mERRO!\033[m")
                    if tam_payload != len(payload):
                        print(f"tamanho do payload: {tam_payload}, tamanho real: {len(payload)}")
                        break
                    else:
                        txBuffer= cria_pacote(mensagem=str(count), estilo= 'e')
                        com1.sendData(np.asarray(txBuffer[0]))
                        time.sleep(0.05)
                

            elif estilo == b'd': # Deu tudo certo!
                txBuffer= cria_pacote(estilo= 'd')
                com1.sendData(np.asarray(txBuffer[0]))
                time.sleep(0.05)
                os.system("cls")
                print("Deu tudo certo!")
                break
        
        imagem= b''
        for i in lista_mensagem:
            imagem= imagem + i
        
        with open(imageW, 'wb') as f:
            f.write(imagem)

        im= Image.open("./imgs/recebidaCopia.png")
        im.show()

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
