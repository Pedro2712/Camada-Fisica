from enlace import *
import time
import numpy as np
import os
from funcao import *
from animacao import Animacao

serialName = "COM4"

mensagem = """sapucaiba sapucaiba"""

def main():
    
    try:
        com1 = enlace(serialName)
        recebe= Animacao()
        recebe.__ini__()
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        
        os.system("cls")
        print ("A recepção vai começar!") 
        # Acesso aos bytes recebidos
        bit_de_termino= b'\xff\xff\xff\xff'
        lista_mensagem =[]
        count = 1
        index = 0
        while True:
            while True:
                rxBuffer, nRx = com1.getData(1)
                # if com1.rx.condicao: recebe.enable()
                if rxBuffer.endswith(bit_de_termino):
                    com1.rx.cond()
                    com1.clear(len(rxBuffer))
                    break
                time.sleep(0.05)
            
            head, estilo, tam_payload, contador, tamanho, payload, eop = desmembramento(rxBuffer)

            contador_erro=1
            if estilo == b'v': # Tá vivo?
                txBuffer= cria_pacote(estilo= 't')
                com1.sendData(np.asarray(txBuffer[0]))
                time.sleep(0.5)

            elif estilo == b't': # Pode mandar!
                txBuffer= cria_pacote(mensagem=mensagem, estilo= 'p')
                if index > len(txBuffer) - 1:
                    stop= cria_pacote(estilo= "d")
                    com1.sendData(np.asarray(stop[0]))
                    break
                com1.sendData(np.asarray(txBuffer[index]))
                index+= 1
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
                    print ("ERRO!")
                    txBuffer= cria_pacote(mensagem=str(count), estilo= 'e')
                    com1.sendData(np.asarray(txBuffer[0]))
                    time.sleep(0.05)
                    if contador_erro == 3:
                        break
                    contador_erro+=1
                

            elif estilo == b'd': # Deu tudo certo!
                # Print Deu tudo certo!
                recebe.disable()
                time.sleep(1.5)
                txBuffer= cria_pacote(estilo= 'd')
                com1.sendData(np.asarray(txBuffer[0]))
                time.sleep(0.05)
                os.system("cls")
                print("Deu tudo certo!")
                break
        
        frase= b''
        for i in lista_mensagem:
            frase= frase + i
        frase= frase.decode("utf-8")

        # Encerra comunicação
        print("-" * 50)
        print("Comunicação encerrada!")
        print("-" * 50)
        print(f"A frase enviada foi:\n{frase}")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    # Só roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
