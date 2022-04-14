from enlace import *
import time
import numpy as np
import os
from funcao import *
from animacao import Animacao
from PIL import Image

serialName = "COM4"

def main():
    
    try:
        com1 = enlace(serialName)
        # recebe= Animacao()
        # Ativa comunicacao. Inicia os threads e a comunicação serial
        imageW= "./imgs/recebidaCopia.png"
        texto = "./text/texto.txt"
        
        com1.enable()

        os.system("cls")
        print ("A recepção vai começar!\n")

        logg=""
        
        # Acesso aos bytes recebidos
        bit_de_termino= b'\xAA\xBB\xCC\xDD'
        lista_mensagem =[]
        count = 1
        index= 0
        condicao= True
        while condicao:
            while condicao:
                rxBuffer, nRx = com1.getData(1)
                if index!= 0 and com1.rx.condicao:
                    txBuffer= cria_pacote(estilo= 4, ultimo=count) #envia Pacote
                    com1.sendData(np.asarray(txBuffer[0]))
                    print(printao(tipo="envio", estilo= 4, tam_datagrama=len(txBuffer[0])))
                    logg+=printao(tipo="envio", estilo= 4, tam_datagrama=len(txBuffer[0]))
                    time.sleep(0.05)
                if rxBuffer == b'\xFF\xFF\xFF\xFF':
                    txBuffer= cria_pacote(estilo= 5) #envia Timeout
                    com1.sendData(np.asarray(txBuffer[0]))
                    print(printao(tipo="envio", estilo= 5, tam_datagrama=len(txBuffer[0])))
                    logg+=printao(tipo="envio", estilo= 5, tam_datagrama=len(txBuffer[0]))
                    time.sleep(0.05)
                    print("-" * 100)
                    print ("Time Out", "\U0001F615")
                    logg+="\nTime Out\n"+"-"*100
                    condicao= False
                if rxBuffer.endswith(bit_de_termino):
                    index= 1
                    com1.rx.cond()
                    com1.clear(len(rxBuffer))
                    break
                time.sleep(0.05)
            
            head, estilo, tamanho, contador, tam_payload, erro, ultimo, crc, payload, eop, tam_datagrama = desmembramento(rxBuffer)
            print(printao(tipo="receb", estilo= estilo, contador=contador,tamanho=tamanho ,tam_datagrama=tam_datagrama, crc=crc))
            logg+=printao(tipo="receb", estilo= estilo, contador=contador,tamanho=tamanho ,tam_datagrama=tam_datagrama, crc=crc)
            if estilo == 1 and len(lista_mensagem)==0: #recebe Ta vivo?
                txBuffer= cria_pacote(estilo= 2) #envia To vivo
                com1.sendData(np.asarray(txBuffer[0]))
                print(printao(tipo="envio", estilo= 2, tam_datagrama=len(txBuffer[0])))
                logg+=printao(tipo="envio", estilo= 2, tam_datagrama=len(txBuffer[0]))
                time.sleep(0.05)

            elif estilo == 3: #recebe Ok
                crc_calculator = CrcCalculator(Crc16.CCITT)
                CRCb = crc_calculator.calculate_checksum(payload)
                CRCbb = CRCb.to_bytes(2,byteorder="big")

                if contador == count and tam_payload == len(payload) and crc==CRCbb:
                    lista_mensagem.append(payload)
                    txBuffer= cria_pacote(estilo= 4, ultimo=count) #envia Pacote
                    com1.sendData(np.asarray(txBuffer[0]))
                    print(printao(tipo="envio", estilo= 4, tam_datagrama=len(txBuffer[0])))
                    logg+=printao(tipo="envio", estilo= 4, tam_datagrama=len(txBuffer[0]))
                    time.sleep(0.05)
                    
                    count+= 1
                else:
                    print ("\033[31mERRO!\033[m")
                    logg+="\nERRO\n"+"-"*100
                    if tam_payload != len(payload):
                        print(f"\nErro no tamanho do payload do pacote: {contador} / tamanho payload correto: {len(payload)}/ tamanho payload recebido: {tam_payload}")
                        txBuffer= cria_pacote(estilo= 6) #envia Erro
                        com1.sendData(np.asarray(txBuffer[0]))
                        print("-" * 100)
                        print(printao(tipo="envio", estilo= 6, tam_datagrama=len(txBuffer[0])))
                        logg+=printao(tipo="envio", estilo= 6, tam_datagrama=len(txBuffer[0]))
                        time.sleep(0.05)
                        
                    else:
                        txBuffer= cria_pacote(estilo= 6, erro=count-1, ultimo=count) #envia Erro
                        com1.sendData(np.asarray(txBuffer[0]))
                        print()
                        print(printao(tipo="envio", estilo= 6, tam_datagrama=len(txBuffer[0])))
                        logg+=printao(tipo="envio", estilo= 6, tam_datagrama=len(txBuffer[0]))
                        time.sleep(0.05)

            elif estilo == 5: #recebe Timeout
                time.sleep(0.05)
                os.system("cls")
                print("Timeout sem handshack!")
                logg+="\nTimeout sem handshack!\n"+"-"*100
                break
                

            elif estilo == 7: #recebe Fim 
                txBuffer= cria_pacote(estilo= 7) #envia Fim
                com1.sendData(np.asarray(txBuffer[0]))
                print(printao(tipo="envio", estilo= 7, tam_datagrama=len(txBuffer[0])))
                logg+=printao(tipo="envio", estilo= 7, tam_datagrama=len(txBuffer[0]))
                time.sleep(0.05)
                os.system("cls")
                print("-"*100)
                print("Deu tudo certo!")
                logg+="\nDeu tudo certo!\n"+"-"*100
                break
        
        imagem= b''
        for i in lista_mensagem:
            imagem= imagem + i
        
        with open(imageW, 'wb') as f:
            f.write(imagem)

        # im= Image.open("./imgs/recebidaCopia.png")
        # im.show()

        # Encerra comunicação
        print("-" * 50)
        print("Comunicação encerrada!")
        print("-" * 50)
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        
    with open(texto, 'w') as f:
        f.write(logg)

    # Só roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
