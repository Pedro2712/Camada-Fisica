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

        imageR= "client/imgs/image.png"
        texto= "client/text/log.txt"

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
        # mensagem= [b'\x03--C\x01r\x00\x00\xa4\x13\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x02\x00\x00\x00\x02\x00\x08\x06\x00\x00\x00\xf4x\xd4\xfa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00\tpHYs\x00\x00\r\xd7\x00\x00\r\xd7\x01B(\x9bx\x00\x00\x00\x19tEXtSoftware\x00www.inkscape.org\x9b\xee<\x1a\x00\x00\x1d\x00IDA\xaa\xbb\xcc\xdd', b'\x03--C\x02r\x00\x007\xf3Tx\x9c\xed\xdd{\xd0\xadW]\x1f\xf0\xef\xefp\x02q\xe4f\x80\x84\x04\x8c#R\xab\x18\xd4\xdcH\x8d"\xd6\x11\x02($\x8c\x05\x07\x9d\xa9\x8eM\xe9\xd0\x96\xeat\x14f\x94\x9bH\xa9\x08:\xa0RfJ\xca\xd8v\x00\x8b:\x10@\xcaM\x04)Q8!( Z\xebeDIL\x80\x88\x10\xc6@\x0eY\xfdc?\'\x9e$\xe7\xe4\xbcg\xafg\xbf\xfb\xb2>\x9f\x993\xefp\xce~\xaa\xbb\xcc\xdd', b'\x03--C\x03r\x00\x00r\xab\xd6Z\x99\xbdy\x7f\xdf\xbd\x9eg\xadU\xad\xb5\x00\x00c9\xb0\xee\x01\x00\x00\xfbO\x00\x00\x80\x01\t\x00\x000 \x01\x00\x00\x06$\x00\x00\xc0\x80\x04\x00\x00\x18\x90\x00\x00\x00\x03\x12\x00\x00`@\x02\x00\x00\x0cH\x00\x00\x80\x01\t\x00\x000 \x01\x00\x00\x06$\x00\x00\xc0\x80\x04\x00\x00\x18\x90\x00\x00\x00\x03\x12\x00\x00`@\x02\x00\x00\x0c\xe8\xe0\xba\x07PUwKrF\x923\x93\x9c5\xfd\xaa\xbb\xcc\xdd', b'\x03--C\x04r\x00\x00\x80$<=\x1b06\x00\x98\xc1\xe1$7$\xb9.\xc9\xb5\xd3\xcf\xeb[k_^\xe7\xa0\xaa\xb5\xb6\x7f\x9dU\x9d\x9a\xe4\xd1I.Krn\xfe\xb1\xd8\x9b\x89\x00`$\xb7\xe6\x1fC\xc1\x87\x93\xbc1\xc9;[k7\xef\xd7\x00V\x1e\x00\xaa\xea\xb4$\xdf\x97E\xd1\x7fL\x92\xaf\\i\x87\x00\xb0\x9d\xbe\x90\xe4\x1dY\x84\x81\xb7\xb4\xd6n\\eg+\t\x00UUI\x9e\x9c\xe4\xe9I\x1e\x99\xe4\xaa\xbb\xcc\xdd']
        condicao= True
        while condicao:
            while condicao:
                if index== 0 and com1.rx.condicao:
                    txBuffer= cria_pacote() #envia Ta vivo?
                    com1.sendData(np.asarray(txBuffer[0]))
                    head, estilo, tamanho, contador, tam_payload, erro, ultimo, crc, payload, eop, tam_datagrama = desmembramento(txBuffer[0])
                    log+= printao(tipo= "envia", tam_datagrama= len(txBuffer), crc= crc)
                    os.system("cls")
                    print ("Reenviando o Handshack")
                if index!= 0 and com1.rx.condicao:
                    com1.sendData(np.asarray(mensagem[index]))
                    head, estilo, tamanho, contador, tam_payload, erro, ultimo, crc, payload, eop, tam_datagrama = desmembramento(mensagem[index])
                    log+= printao(tipo= "envia", estilo= 3, contador= index + 1, tamanho= len(mensagem), tam_datagrama= len(mensagem[index]), crc= crc)
                    os.system("cls")
                    print ("Reenviando o pacote")
                rxBuffer, nRx = com1.getData(1)
                if rxBuffer.endswith(bit_de_termino):
                    # if com1.rx.condicao_print: recebe.printProgressBar(0, len(mensagem), prefix = 'Progress:', suffix = 'Complete', length = 50)
                    com1.clear(len(rxBuffer))
                    com1.rx.cond()
                    break
                if rxBuffer == b'\xFF\xFF\xFF\xFF':
                    log+= "\nTime Out!\n" + "-" * 100
                    txBuffer= cria_pacote(estilo= 5) #envia Timeout
                    com1.sendData(np.asarray(txBuffer[0]))
                    head, estilo, tamanho, contador, tam_payload, erro, ultimo, crc, payload, eop, tam_datagrama = desmembramento(txBuffer[0])
                    log+= printao(tipo= "envia", estilo= 5, tam_datagrama= len(txBuffer[0]), crc= crc)
                    time.sleep(0.05)
                    condicao= False
                    print("-" * 50)
                    print ("Time Out", "\U0001F615")
                time.sleep(0.05)
            head, estilo, tamanho, contador, tam_payload, erro, ultimo, crc, payload, eop, tam_datagrama = desmembramento(rxBuffer)
            log+= printao(tipo= "receb", estilo= estilo, contador= index + 1, tam_datagrama= tam_datagrama)

            if estilo == 6: #recebe Erro
                log+= "\nERRO!\n" + "-" * 100
                index = erro
                
                com1.sendData(np.asarray(mensagem[index])) #envia Pacote
                head, estilo, tamanho, contador, tam_payload, erro, ultimo, crc, payload, eop, tam_datagrama = desmembramento(mensagem[index])
                log+= printao(tipo= "envia", estilo= 3, contador= index + 1, tamanho= len(mensagem), tam_datagrama= len(mensagem[index]), crc= crc)
                time.sleep(0.05)
            
            elif estilo == 2:
                com1.sendData(np.asarray(mensagem[index])) #envia Pacote
                head, estilo, tamanho, contador, tam_payload, erro, ultimo, crc, payload, eop, tam_datagrama = desmembramento(mensagem[index])
                log+= printao(tipo= "envia", estilo= 3, contador= index + 1, tamanho= len(mensagem), tam_datagrama= len(mensagem[index]), crc= crc)
                time.sleep(0.05)
                
            elif estilo == 4: #recebe Ok\
                index= ultimo
                if index > len(mensagem) - 1:
                    stop= cria_pacote(estilo= 7) #envia Fim
                    com1.sendData(np.asarray(stop[0]))
                    head, estilo, tamanho, contador, tam_payload, erro, ultimo, crc, payload, eop, tam_datagrama = desmembramento(stop[0])
                    log+= printao(tipo= "envia", estilo= 7, tam_datagrama= len(stop[0]), crc= crc)
                    time.sleep(0.05)
                    break
                # if sla == 10:
                #     index= index + 20
                # sla+= 1
                com1.sendData(np.asarray(mensagem[index])) #envia Pacote
                head, estilo, tamanho, contador, tam_payload, erro, ultimo, crc, payload, eop, tam_datagrama = desmembramento(mensagem[index])
                log+= printao(tipo= "envia", estilo= 3, contador= index + 1, tamanho= len(mensagem), tam_datagrama= len(mensagem[index]), crc= crc)
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
