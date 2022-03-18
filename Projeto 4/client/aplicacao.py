from cmath import log
from enlace import *
import time
import numpy as np
import os
from funcao import *
from animacao import Animacao

serialName = "COM4"


def main():
    
    try:
        com1 = enlace(serialName) 
        recebe = Animacao()
        com1.enable()

        imageR= "./imgs/image.png"
        texto= "./text/log.txt"

        with open(imageR, 'rb') as arquivo:
            m= arquivo.read()
        
        os.system("cls")
        tempo_i= time.ctime()

        print ("A transmissão vai começar!")
        print ("A recepção vai começar!")

        bit_de_termino= b'\xAA\xBB\xCC\xDD'
        index = 0
        sla= 0
        log= ''
        mensagem= cria_pacote(mensagem=m, estilo= 3)
        # mensagem= [b'\x03--\x05\x01r\x00\x00--na xcksmwx,lca sscawmcomc,w cwkcm aksclac woc,a wcoawmc awmkcplm wmlpclkwam cm,l;plawm  cm,l;[;l,m\nna xcksmwx,lca \xaa\xbb\xcc\xdd', b'\x03--\x05\x02r\x00\x00--sscawmcomc,w cwkcm aksclac woc,a wcoawmc awmkcplm wmlpclkwam cm,l;plawm  cm,l;[;l,m\nna xcksmwx,lca sscawmcomc,w cw\xaa\xbb\xcc\xdd', b'\x03--\x05\x03a\x00\x00--kcm aksclac woc,a wcoawmc awmkcplm wmlpclkwam cm,l;plawm  cm,l;[;l,m\nna xcksmwx,lca sscawmcomc,w cwkcm aksclac woc\xaa\xbb\xcc\xdd', b'\x03--\x05\x04r\x00\x00--,a wcoawmc awmkcplm wmlpclkwam cm,l;plawm  cm,l;[;l,m\nna xcksmwx,lca sscawmcomc,w cwkcm aksclac woc,a wcoawmc awmk\xaa\xbb\xcc\xdd', b"\x03--\x05\x05'\x00\x00--cplm wmlpclkwam cm,l;plawm  cm,l;[;l,m \xaa\xbb\xcc\xdd"]
        condicao= True
        while condicao:
            while condicao:
                if index== 0 and com1.rx.condicao:
                    txBuffer= cria_pacote() #envia Ta vivo?
                    com1.sendData(np.asarray(txBuffer[0]))
                    log+= printao(tipo= "envia", tam_datagrama= len(txBuffer))
                    os.system("cls")
                    print ("Reenviando o Handshack")
                if index!= 0 and com1.rx.condicao:
                    com1.sendData(np.asarray(mensagem[index]))
                    log+= printao(tipo= "envia", estilo= 3, contador= index + 1, tamanho= len(mensagem), tam_datagrama= len(mensagem[index]))
                    os.system("cls")
                    print ("Reenviando o pacote")
                rxBuffer, nRx = com1.getData(1)
                if rxBuffer.endswith(bit_de_termino):
                    if com1.rx.condicao_print: recebe.printProgressBar(0, len(mensagem), prefix = 'Progress:', suffix = 'Complete', length = 50)
                    com1.clear(len(rxBuffer))
                    com1.rx.cond()
                    break
                if rxBuffer == b'\xFF\xFF\xFF\xFF':
                    log+= "\nTime Out!\n" + "-" * 100
                    txBuffer= cria_pacote(estilo= 5) #envia Timeout
                    com1.sendData(np.asarray(txBuffer[0]))
                    log+= printao(tipo= "envia", estilo= 5, tam_datagrama= len(txBuffer[0]))
                    time.sleep(0.05)
                    condicao= False
                    print("-" * 50)
                    print ("Time Out", "\U0001F615")
                time.sleep(0.05)
            head, estilo, tamanho, contador, tam_payload, erro, ultimo, payload, eop, tam_datagrama = desmembramento(rxBuffer)
            log+= printao(tipo= "receb", estilo= estilo, contador= index + 1, tam_datagrama= tam_datagrama)

            if estilo == 6: #recebe Erro
                log+= "\nERRO!\n" + "-" * 100
                index = erro
                
                com1.sendData(np.asarray(mensagem[index])) #envia Pacote
                log+= printao(tipo= "envia", estilo= 3, contador= index + 1, tamanho= len(mensagem), tam_datagrama= len(mensagem[index]))
                time.sleep(0.05)
            
            elif estilo == 2:
                com1.sendData(np.asarray(mensagem[index])) #envia Pacote
                log+= printao(tipo= "envia", estilo= 3, contador= index + 1, tamanho= len(mensagem), tam_datagrama= len(mensagem[index]))
                time.sleep(0.05)
                
            elif estilo == 4: #recebe Ok\
                index= ultimo
                if index > len(mensagem) - 1:
                    stop= cria_pacote(estilo= 7) #envia Fim
                    com1.sendData(np.asarray(stop[0]))
                    log+= printao(tipo= "envia", estilo= 7, tam_datagrama= len(stop[0]))
                    time.sleep(0.05)
                    break
                # if sla == 10:
                #     index= index + 20
                # sla+= 1
                com1.sendData(np.asarray(mensagem[index])) #envia Pacote
                log+= printao(tipo= "envia", estilo= 3, contador= index + 1, tamanho= len(mensagem), tam_datagrama= len(mensagem[index]))
                time.sleep(0.05)
                recebe.printProgressBar(index + 1, len(mensagem), prefix = 'Progress:', suffix = 'Complete', length = 50)

            elif estilo == 7: #recebe Fim
                print("Deu tudo certo!")
                log+= "\nDeu tudo certo!\n" + "-" * 100
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
    
    with open(texto, 'w') as arquivo:
            arquivo.write(log)
        

    # Só roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
