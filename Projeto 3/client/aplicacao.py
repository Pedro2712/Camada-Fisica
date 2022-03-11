from pyrsistent import b
from enlace import *
import time
import numpy as np
import os
from funcao import *
from animacao import Animacao

serialName = "COM3"

mensagem = """Nesse projeto, sua aplicação que exerce o papel de client deverá enviar um arquivo para a aplicação server.
Esse arquivo deverá ser fragmentado e enviado através de “pacotes” (datagramas) De agora em diante você está PROIBIDO de trocar mensagens entre server e client que não sejam um datagrama 
completo (um pacote). Isso significa que mesmo que queira enviar um único byte, deverá enviar um pacote 
compondo um datagrama. Para isso vamos considerar o seguinte datagrama:
Nesse projeto, sua aplicação que exerce o papel de client deverá enviar um arquivo para a aplicação server.
Esse arquivo deverá ser fragmentado e enviado através de “pacotes” (datagramas) De agora em diante você está PROIBIDO de trocar mensagens entre server e client que não sejam um datagrama 
completo (um pacote). Isso significa que mesmo que queira enviar um único byte, deverá enviar um pacote 
compondo um datagrama. Para isso vamos considerar o seguinte datagrama:
Nesse projeto, sua aplicação que exerce o papel de client deverá enviar um arquivo para a aplicação server.
Esse arquivo deverá ser fragmentado e enviado através de “pacotes” (datagramas) De agora em diante você está PROIBIDO de trocar mensagens entre server e client que não sejam um datagrama 
completo (um pacote). Isso significa que mesmo que queira enviar um único byte, deverá enviar um pacote 
compondo um datagrama. Para isso vamos considerar o seguinte datagrama:
Nesse projeto, sua aplicação que exerce o papel de client deverá enviar um arquivo para a aplicação server.
Esse arquivo deverá ser fragmentado e enviado através de “pacotes” (datagramas) De agora em diante você está PROIBIDO de trocar mensagens entre server e client que não sejam um datagrama 
completo (um pacote). Isso significa que mesmo que queira enviar um único byte, deverá enviar um pacote 
compondo um datagrama. Para isso vamos considerar o seguinte datagrama:"""


def main():
    
    try:
        com1 = enlace(serialName)
        recebe = Animacao()
        com1.enable()

        os.system("cls")
        tempo_i= time.ctime()

        time.sleep(0.05)
        bit_de_termino= b'\xff\xff\xff\xff'
        lista_mensagem =[]
        count = 1
        index = 0
        sla= 0
        while True:
            while True:
                if com1.rx.condicao:
                    txBuffer= cria_pacote()
                    com1.sendData(np.asarray(txBuffer[0]))
                rxBuffer, nRx = com1.getData(1)
                if rxBuffer.endswith(bit_de_termino):
                    if com1.rx.condicao: recebe.enable()
                    com1.clear(len(rxBuffer))
                    com1.rx.cond()
                    break
                time.sleep(0.05)
            head, estilo, tam_pacotes, contador, tamanho, payload, eop = desmembramento(rxBuffer)

            if estilo == b'e':
                print (index, "antes")
                index = int(payload.decode("utf-8")) - 1
                print (index, "depois")
                txBuffer= cria_pacote(mensagem=mensagem, estilo= 'p')
                com1.sendData(np.asarray(txBuffer[index]))
                time.sleep(0.05)
                index+= 1
            
            elif estilo == b'v': # Tá vivo?
                #FAZER O SEND DATA de Pode mandar! == b't'
                txBuffer= cria_pacote(estilo= "t")
                com1.sendData(np.asarray(txBuffer[0]))
                time.sleep(0.05)

            elif estilo == b't': # Pode mandar!
                # Fazer o SEND DATA do pacote == b'p'
                txBuffer= cria_pacote(mensagem=mensagem, estilo= 'p')
                if index > len(txBuffer) - 1:
                    stop= cria_pacote(estilo= "d")
                    com1.sendData(np.asarray(stop[0]))
                    recebe.disable()
                    time.sleep(1.8)
                    break
                if sla == 5:
                    print ("entrou")
                    index= index + 4
                sla+= 1
                com1.sendData(np.asarray(txBuffer[index]))
                index+= 1
                time.sleep(0.05)

            elif estilo == b'd': # Deu tudo certo!
                # Print Deu tudo certo!
                recebe.disable()
                time.sleep(1)
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
