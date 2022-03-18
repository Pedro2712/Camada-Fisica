import math
import os
import time

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

def header(contador= 1, tamanho= 1, tam_payload= 0, estilo= 1, erro=0, ultimo=0):
    ############################################################################################
    # Ordem adotado no Head: estilo, livre, livre, tamanho, contador, livre, erro, ultimo, livre, livre #
    # Ordem adotado no Head: estilo, livre, livre, tamanho, contador, tam_payload, erro, ultimo, livre, livre #
    ############################################################################################
    if estilo == 3 :
        head= estilo.to_bytes(1, byteorder='big') + bytes("--", encoding="utf-8") + tamanho.to_bytes(1, byteorder='big') + \
                contador.to_bytes(1, byteorder='big') + tam_payload.to_bytes(1, byteorder='big') + erro.to_bytes(1, byteorder='big') + \
                ultimo.to_bytes(1, byteorder='big') + bytes("--", encoding="utf-8")
        return head
        
    head= estilo.to_bytes(1, byteorder='big') + bytes("--", encoding="utf-8") + tamanho.to_bytes(1, byteorder='big') + \
        contador.to_bytes(1, byteorder='big') + bytes("-", encoding="utf-8") + erro.to_bytes(1, byteorder='big') + \
        ultimo.to_bytes(1, byteorder='big') + bytes("--", encoding="utf-8")
    return head
    
def cria_pacote(mensagem= "", estilo= 1, erro=0, ultimo=0):
    mensagem= bytes(mensagem, encoding= "utf-8")
    tamanho= math.ceil(len(mensagem)/114)

    pacote= b''; contador= 1; eop= b'\xAA\xBB\xCC\xDD'
    lista_datagrama= [header(estilo=estilo, ultimo=ultimo) + pacote + eop]
    for count, i in enumerate(mensagem):
        pacote+= i.to_bytes(1, byteorder='big')
        if len(pacote) == 114 or count == len(mensagem)-1:
            print(ultimo)
            head= header(contador=contador, tamanho=tamanho, tam_payload=len(pacote), estilo=estilo, erro=erro)
            
            datagrama= head + pacote + eop
            lista_datagrama.append(datagrama)
            
            pacote = b''
            contador += 1
        if count == len(mensagem)-1: lista_datagrama.pop(0)
    return lista_datagrama

def desmembramento(rxBuffer):
    head = rxBuffer[:10]
    estilo = head[0]
    tamanho = head[3]
    contador = head[4]
    tam_payload = head[5]
    erro = head[6]
    ultimo = head[7]
    tam_datagrama = len(rxBuffer)

    payload = rxBuffer[10:-4]
    eop = rxBuffer[tam_payload+10:]

    return head, estilo, tamanho, contador, tam_payload, erro, ultimo, payload, eop, tam_datagrama

def tempo_decorrido(temp):
    print (f'\rTempo decorrido é: {temp}', end = "\r")

def printao(tipo= "receb", estilo= 0, contador= 0, tamanho= 0, tam_datagrama= 0):
    if tipo=="receb":
        print(f"{time.ctime()} / {tipo} / estilo: {estilo} / tam_data: {tam_datagrama} / contador: {contador} / tamanho: {tamanho} / CRC")
    else:
        print(f"{time.ctime()} / {tipo} / estilo: {estilo} / tam_data: {tam_datagrama}")
    print("-"*100)