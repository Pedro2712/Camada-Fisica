import math
import os

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
    
    horas     = str(int((tempo/3600))).rjust(2, '0')
    minutos   = str(int((tempo%3600)/60)).rjust(2, '0')
    segundos  = str((tempo%3600)%60).rjust(2, '0')

    return f"{horas}:{minutos}:{segundos}"

def header(contador= "001", tamanho= "001", tam_payload= 0, estilo= "v"):
    ############################################################################################
    # Ordem adotado no Head: estilo, tam_payload, contador, tamanho, desconhecido, deconhecido #
    ############################################################################################
    # 3 contador, 3 tamanho, 1 tam_pacotes, 1 estilo, 2 desconhecidos
    head= bytes(estilo, encoding= "utf-8") + tam_payload.to_bytes(1, byteorder='big') + bytes(f"{contador}{tamanho}--", encoding= "utf-8")
    return head

    
def cria_pacote(mensagem= "", estilo= "v"):
    mensagem= bytes(mensagem, encoding= "utf-8")
    tamanho= str(math.ceil(len(mensagem)/114)).rjust(3, '0')

    pacote= b''; contador= 1; eop= b'\xff\xff\xff\xff'
    lista_datagrama= [header(estilo=estilo) + pacote + eop]
    for count, i in enumerate(mensagem):
        pacote+= i.to_bytes(1, byteorder='big')
        if len(pacote) == 114 or count == len(mensagem)-1:
            contador= str(contador).rjust(3, '0')
            head= header(contador=contador, tamanho=tamanho, tam_payload=len(pacote), estilo=estilo)
            
            datagrama= head + pacote + eop
            lista_datagrama.append(datagrama)
            
            pacote= b''
            contador= int(contador) + 1
        if count == len(mensagem)-1: lista_datagrama.pop(0)
    return lista_datagrama

def desmembramento(rxBuffer):
    head = rxBuffer[:10]
    tam_payload = head[1]
    payload = rxBuffer[10:tam_payload+10]
    eop = rxBuffer[tam_payload+10:]

    estilo = head[0].to_bytes(1,byteorder='big')
    contador = int(head[2:5])
    tamanho = int(head[5:8])

    return head, estilo, tam_payload, contador, tamanho, payload, eop

def tempo_decorrido(temp):
    os.system("cls")
    print ("A recepção vai começar!")
    print (f"Tempo decorrido é: {temp}")