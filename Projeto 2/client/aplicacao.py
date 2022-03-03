from enlace import *
import random
import time
import numpy as np

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

# Calcula os segundos totais da transmissão dos dados
def segundos_totais(temp):
    horas      = int(temp[:2])
    minutos    = int(temp[3:5])
    segundos   = int(temp[6:])

    segundos_f = horas * 3600 + minutos * 60 + segundos

    return segundos_f

# Sorteia os comandos que serão enviados para o server
def sorteia_comandos():
    global sorteado
    comandos= ["00 FF 00 FF", "00 FF FF 00", "FF", "00", "FF 00", "00 FF"]
    sorteado= random.randint(10, 30)
    lista_comandos= []
    for i in range(sorteado):
        index = random.randint(0, 5)
        lista_comandos.append(comandos[index])
    return bytes('/'.join(lista_comandos).encode())

def main():
    
    try:
        txBuffer= sorteia_comandos()
        com1 = enlace(serialName)
        
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()

        # Faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
        print ("O número de comandos é de {}".format(sorteado))

        print("A transmissão vai começar!")
        tempo_i= time.ctime()
        com1.sendData(np.asarray(txBuffer))

        print ("A recepção vai começar!")
        # Acesso aos bytes recebidos
        rxBuffer, nRx = com1.getData()
        n_rxBuffer= bytes([len(str(rxBuffer).split('/'))])     # Calcula a quantidade de comandos enviados e o transforma em hexadecimal
        print("-" * 50)

        #########################################################
        print("A transmissão vai começar de novo!")
        com1.sendData(np.asarray(n_rxBuffer))                  # Envia a quantidade de comandos para o client em hexadecimal
        
        print ("A recepção vai começar de novo!")
        rxBuffer_again, nRx_2 = com1.getData()                 # Recebe a quantidade de comandos em hexadecimal do serve

        # Transforma a quantidade de comandos em decimal
        transforma = int.from_bytes(rxBuffer_again, 'big')
        n_rxBuffer_again= f"\033[92mSuccess:\033[0m\nO número de comandos recebidos é: {transforma}" if transforma == sorteado \
                            else "\033[91mFail:\033[0m\nO Server recebeu os comandos com problema de interpretação"
        #########################################################

        tempo_f     = time.ctime()
        tempo_total = calcula_tempo(tempo_i, tempo_f)
        
        # Encerra comunicação
        print("-" * 50)
        print("Comunicação encerrada!")
        print(f"Tempo decorrido foi de: {tempo_total}")
        print(f"{n_rxBuffer_again}")
        print("-" * 50)
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    # Só roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()