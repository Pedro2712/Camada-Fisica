from pyrsistent import b
from enlace import *
import random
import time
import numpy as np
import os

serialName = "COM4"

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
    print ("A transmissão vai começar!")
    print ("A recepção vai começar!")
    print (f"Tempo decorrido é: {temp}")

# Sorteia os comandos que serão enviados para o server
def sorteia_comandos():
    global sorteado
    comandos= ["00 FF 00 FF", "00 FF FF 00", "FF", "00", "FF 00", "00 FF"]
    sorteado= random.randint(10, 30)
    lista_comandos= []
    for i in range(sorteado):
        index = random.randint(0, 5)
        lista_comandos.append(comandos[index])
    bit_de_termino= "E0"
    lista_comandos.append (bit_de_termino)
    return bytes('/'.join(lista_comandos).encode())

def header(contador, tamanho, tam_pacotes, estilo):
    # 3 contador, 3 tamanho, 1 tam_pacotes, 1 estilo, 2 sem nada
    head= bytes(f"{contador}{tamanho}xx", encoding= "utf-8")
    head= bytes(estilo, encoding= "utf-8") + tam_pacotes.to_bytes(1, byteorder='big') + head
    return head

    
def cria_pacote(mensagem, estilo):
    mensagem= bytes(mensagem, encoding= "utf-8")
    lista_pacotes= []
    tamanho= int(len(mensagem)/114)
    if len(mensagem) % 114 != 0:  
        tamanho += 1
    tamanho= str(tamanho).rjust(3, '0')

    contador= 1
    pacote= b''
    for count, i in enumerate(mensagem):
        pacote+= i.to_bytes(1, byteorder='big')
        if len(pacote) == 114 or count == len(mensagem)-1:
            contador= str(contador).rjust(3, '0')
            head= header(contador, tamanho, len(pacote), estilo)
            eop= b'\xff\xff\xff\xff'
            datagrama= head + pacote + eop
            lista_pacotes.append(datagrama)
            pacote= b''
            contador= int(contador) + 1
    return lista_pacotes

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
