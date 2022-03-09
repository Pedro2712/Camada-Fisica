from pyrsistent import b
from enlace import *
import time
import numpy as np
import os
from funcao import *
from animation import animation

serialName = "COM4"

def tempo_decorrido(temp):
    os.system("cls")
    print ("A transmissão vai começar!")
    print ("A recepção vai começar!")
    print (f"Tempo decorrido é: {temp}")

mensagem = """sapucaiba sapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaiba vsapucaiba
sapucaibasapucaibasapucaibasapucaibasapucaibasap sapucaiba sapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaiba vsapucaiba
sapucaibasapucaibasapucaibasapucaibásapucaibasap
sapucaiba sapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaiba vsapucaiba
sapucaibasapucaibasapuácaibasapucaibasapucaibasaáp
sapucaiba sapucaiba sapucaibasaáááááááááááááááááááááááááááááááááááááááááááááááááááááááááááááááááááááápucaiba sapucaibasapucaiba sapucaiba vsapucaiba
sapucaiba sapucaiba sapucaibasaáááááááááááááááááááááááááááááááááááááááááááááááááááááááááááááááááááááápucaiba sapucaibasapucaiba sapucaiba vsapucaiba
sapucaiba sapucaiba sapucaibasaáááááááááááááááááááááááááááááááááááááááááááááááááááááááááááááááááááááápucaiba sapucaibasapucaiba sapucaiba vsapucaiba
sapucaiba sapucaiba sapucaibasaáááááááááááááááááááááááááááááááááááááááááááááááááááááááááááááááááááááápucaiba sapucaibasapucaiba sapucaiba vsapucaiba
sapucaibasapucaibasapucaibasapucaibasapááucaibasap
sapucaiba sapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaiba vsapucaiba
sapucaibasapucaibasapucaibasapucaibasapucaibasap
sapucaiba sapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaiba vsapucaiba
sapucaibasapucaibasapucaibasapucaibasapucaibasap
sapucaiba sapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaiba vsapucaiba
sapucaibasapucaibasapucaibasapucaibasapucaibasap
sapucaiba sapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaiba vsapucaiba
sapucaibasapucaibasapucaibasapucaibasapáááucaibasap
sapucaiba sapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaiba vsapucaiba
sapucaibasapucaibasapucaibasapucaibasapucaibasap
sapucaiba sapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaiba vsapucaiba
sapucaibasapucaibasapucaibasapucaibasapucaibasap
sapucaiba sapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaiba vsapucaiba
sapucaibasapucaibasapucaibasapucaibasapucaibasap
sapucaiba sapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaiba vsapucaiba
sapucaibasapucaibasapucaibasapucaibasapucaibasap
sapucaiba sapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaiba vsapucaiba
sapucaibasapucaibasapucaibasapucaibasapucaibasap
sapucaiba sapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaiba vsapucaiba
sapucaibasapucaibasapucaibasapucaibasapucaibasap
v
sapucaiba sapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaiba vsapucaiba
sapucaibasapucaibasapucaibasapucaibasapucaibasap
sapucaiba sapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaiba vsapucaiba
sapucaibasapucaibasapucaibasapucaibasapucaibasap
sapucaiba sapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaiba vsapucaiba
sapucaibasapucaibasapucaibasapucaibasapucaibasap
sapucaiba sapucaiba sapucaibasapucaiba sapucaibasapucaiba sapucaiba vsapucaiba
sapucaibasapucaibasapucaibasapucaibasapucaibasap
"""

def main():
    
    try:
        com1 = enlace(serialName)
        com1.enable()

        os.system("cls")
        tempo_i= time.ctime()
        txBuffer= cria_pacote()

        com1.sendData(np.asarray(txBuffer[0]))
        time.sleep(0.05)
        

        bit_de_termino= b'\xff\xff\xff\xff'
        mensagem =[]
        cont = 0
        while True:
            while True:
                rxBuffer, nRx = com1.getData(1)
                # recebe.enable()
                if rxBuffer.endswith(bit_de_termino):
                    break
                time.sleep(0.5)
            
            head, estilo, tam_pacotes, contador, tamanho, playload, eop = desmembramento(rxBuffer)

            if estilo == b'v': # Tá vivo?
                #FAZER O SEND DATA de Pode mandar! == b't'
                continue

            elif estilo == b't': # Pode mandar!
                # Fazer o SEND DATA do pacote == b'p'
                continue

            elif estilo == b'p': # Pacote
                # Criar variável count para salvar a contagem
                # Criar lista para salvar o pacote
                # Verificar se a contagem é igual a count + 1
                # Adicionar o pacote para a lista de pacotes
                # Fazer o SEND DATA Pode mandar! == b't'
                # Atualizar o count para count+= 1
                # Criar condição quando o count == contador se entrar na condição 
                    # Mandar SEND DATA deu tudo certo! == b'd' e break
                
                # cont+=1
                # #FAZER SEND
                # mensagem.append(playload)
                # if cont == contador:
                #     break
                continue

            elif estilo == b'd': # Deu tudo certo!
                # Print Deu tudo certo!
                # Break
                continue
        
        txBuffer= cria_pacote(mensagem, "b")
        os.system("cls")
        tempo_i= time.ctime()
        print (len(txBuffer))
        for i in txBuffer:
            com1.sendData(np.asarray(i))
        time.sleep(0.05)

        tempo_f     = time.ctime()
        tempo_total = calcula_tempo(tempo_i, tempo_f)
        
        # # Encerra comunicação
        print("-" * 50)
        print("Comunicação encerrada!")
        # print ("O número de comandos sorteados foi de: {}".format(sorteado))
        print(f"Tempo decorrido foi de: {tempo_total}")
        # print(f"{n_rxBuffer_again}")
        print("-" * 50)
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    # Só roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
