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

def main():
    
    try:
        com1 = enlace(serialName)
        
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()

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
        txBuffer= cria_pacote(mensagem, "b")
        # Faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
        os.system("cls")
        tempo_i= time.ctime()
        print (len(txBuffer))
        for i in txBuffer:
            com1.sendData(np.asarray(i))
        time.sleep(0.05)
        
        # print ("A recepção vai começar!")
        # # Recebe a quantidade de comandos em hexadecimal do serve
        # rxBuffer_again, nRx_2 = com1.getData(1)

        # # Transforma a quantidade de comandos em decimal
        # transforma = int.from_bytes(rxBuffer_again, 'big') # Para o teste dar errado b'x04'
        # n_rxBuffer_again= f"\033[92mSuccess:\033[0m\nO número de comandos recebidos é: {transforma}" if transforma == sorteado \
        #                     else "\033[91mFail:\033[0m\nO Server recebeu os comandos com problema de interpretação"

        # tempo_f     = time.ctime()
        # tempo_total = calcula_tempo(tempo_i, tempo_f)
        
        # # Encerra comunicação
        # print("-" * 50)
        # print("Comunicação encerrada!")
        # print ("O número de comandos sorteados foi de: {}".format(sorteado))
        # print(f"Tempo decorrido foi de: {tempo_total}")
        # print(f"{n_rxBuffer_again}")
        # print("-" * 50)
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    # Só roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
