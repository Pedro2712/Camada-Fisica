from enlace import *
import time
import numpy as np
import os
from funcao import *
from animacao import Animacao

serialName = "COM3"

mensagem = """sapucaiba sapucaiba sapucaiba sapucaibasapucaiba sapucaiba
sapucaiba sapucaiba sapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaiba
sapucaiba sapucaiba
sapucaiba sapucaibasapucaiba sapucaiba
sapucaiba sapucaiba
sapucaiba sapucaiba
sapucaiba sapucaiba
sapucaiba sapucaibasapucaiba sapucaiba
sapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaiba
sapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaiba
sapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaiba
sapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaiba
sapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaiba
sapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaiba fim!!!"""

def main():
    
    try:
        com1 = enlace(serialName)
        recebe = Animacao()
        recebe.__ini__()
        com1.enable()

        os.system("cls")
        tempo_i= time.ctime()
        txBuffer= cria_pacote()

        com1.sendData(np.asarray(txBuffer[0]))
        time.sleep(0.05)

        bit_de_termino= b'\xff\xff\xff\xff'
        lista_mensagem =[]
        count = 1
        index = 0
        while True:
            while True:
                rxBuffer, nRx = com1.getData(1)
                if com1.rx.condicao: recebe.enable()
                if rxBuffer.endswith(bit_de_termino):
                    com1.rx.cond()
                    com1.clear(len(rxBuffer))
                    break
                time.sleep(0.05)
            head, estilo, tam_pacotes, contador, tamanho, payload, eop = desmembramento(rxBuffer)

            if estilo == b'v': # Tá vivo?
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
                com1.sendData(np.asarray(txBuffer[index]))
                index+= 1
                time.sleep(0.05)

            elif estilo == b'p': # Pacote
                # Criar variável count para salvar a contagem #
                # Criar lista para salvar o pacote #
                # Verificar se a contagem é igual a count
                # Adicionar o pacote para a lista de pacotes
                # Fazer o SEND DATA Pode mandar! == b't'
                # Atualizar o count para count+= 1
                # Criar condição quando o contagem == tamanho se entrar na condição 
                    # Mandar SEND DATA deu tudo certo! == b'd' e break
                if contador == count:
                    lista_mensagem.append(payload)
                    txBuffer= cria_pacote(estilo= 't')
                    com1.sendData(np.asarray(txBuffer[0]))
                    time.sleep(0.05)
                count+= 1

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
