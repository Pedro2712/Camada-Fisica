from sqlalchemy import null, true
from enlace import *
import random
import time
import numpy as np
import interfaceFisica
import os

serialName = "COM3"

# Calcula o tempo total da transmissão dos dados, ou seja, o tempo inicial menos o tempo final 
def calcula_tempo(tempo_i, tempo_f):
    hora_i    = int(tempo_i.split()[3][:2]) * 3600
    minuto_i  = int(tempo_i.split()[3][3:5]) * 60
    segungo_i = int(tempo_i.split()[3][6:])
    total_i   = hora_i + minuto_i + segungo_i
    
    hora_f    = int(tempo_f.split()[3][:2]) * 3600
    minuto_f  = int(tempo_f.split()[3][3:5]) * 60
    segungo_f = int(tempo_f.split()[3][6:])
    total_f   = hora_f + minuto_f + segungo_f

    tempo= total_f - total_i
    
    horas     = int((tempo/3600)) if int((tempo/3600)) >= 10 else f"0{int((tempo/3600))}"
    minutos   = int((tempo%3600)/60) if int((tempo%3600)/60) >= 10 else f"0{int((tempo%3600)/60)}"
    segundos  = (tempo%3600)%60 if (tempo%3600)%60 >= 10 else f"0{(tempo%3600)%60}"

    return f"{horas}:{minutos}:{segundos}"

def tempo_decorrido(temp):
    os.system("cls")
    print ("A recepção vai começar!")
    print (f"Tempo decorrido é: {temp}")

def recebendo():
    os.system("cls")
    print ("recebendo.")
    time.sleep(0.15)
    os.system("cls")
    print ("recebendo..")
    time.sleep(0.15)
    os.system("cls")
    print ("recebendo...")
    time.sleep(0.15)
    os.system("cls")
    print ("recebendo")

def main():
    
    try:
        com1 = enlace(serialName)
        
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        
        os.system("cls")
        print ("A recepção vai começar!")
        # Acesso aos bytes recebidos
        bit_de_termino= "E0"
        while True:
            rxBuffer, nRx = com1.getData(1)
            recebendo()
            ultimo_bit= str(rxBuffer).split('/')[-1][:-1:]
            if ultimo_bit == bit_de_termino:
                break
            time.sleep(1.5)
        os.system("cls")
        
        # Calcula a quantidade de comandos enviados e o transforma em hexadecimal
        n_rxBuffer= bytes([len(str(rxBuffer).split('/'))-1])
        print("-" * 50)

        print("A transmissão vai começar")
        # Envia a quantidade de comandos para o client em hexadecimal
        print(f"Enviando o número de comandos de: {len(str(rxBuffer).split('/'))-1}")
        com1.sendData(np.asarray(n_rxBuffer))

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