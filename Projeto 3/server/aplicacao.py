from enlace import *
import time
import math
import os

serialName = "COM5"

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

def header(contador= "001", tamanho= "001", tam_payload= 0, estilo= "a"):
    ############################################################################################
    # Ordem adotado no Head: estilo, tam_payload, contador, tamanho, desconhecido, deconhecido #
    ############################################################################################
    # 3 contador, 3 tamanho, 1 tam_pacotes, 1 estilo, 2 desconhecidos
    head= bytes(estilo, encoding= "utf-8") + tam_payload.to_bytes(1, byteorder='big') + bytes(f"{contador}{tamanho}--", encoding= "utf-8")
    return head

    
def cria_pacote(mensagem= "", estilo= "a"):
    mensagem= bytes(mensagem, encoding= "utf-8")
    tamanho= str(math.ceil(len(mensagem)/114)).rjust(3, '0')

    pacote= b''; contador= 1; eop= b'\xff\xff\xff\xff'
    lista_datagrama= [header() + pacote + eop]
    for count, i in enumerate(mensagem):
        pacote+= i.to_bytes(1, byteorder='big')
        if len(pacote) == 114 or count == len(mensagem)-1:
            contador= str(contador).rjust(3, '0')
            head= header(contador, tamanho, len(pacote), estilo)
            
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

def main():
    
    try:
        com1 = enlace(serialName)
        
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        
        os.system("cls")
        print ("A recepção vai começar!") 
        # Acesso aos bytes recebidos
        bit_de_termino= b'\xff\xff\xff\xff'
        mensagem =[]
        cont = 0
        while True:
            while True:
                rxBuffer, nRx = com1.getData(1)
                recebendo()
                if rxBuffer.endswith(bit_de_termino):
                    break
                time.sleep(0.5)
            
            head, estilo, tam_pacotes, contador, tamanho, playload, eop = desmembramento(rxBuffer)

            # if estilo == b'a':

            #     #FAZER O SEND DATA
            #     continue

            if estilo == b'b':
                cont+=1
                #FAZER SEND
                mensagem.append(playload)
                if cont == contador:
                    break
        
        print(mensagem)
        print(len(mensagem))
        # print(mensagem.join(""))
        
        # # Calcula a quantidade de comandos enviados e o transforma em hexadecimal
        # n_rxBuffer= bytes([len(str(rxBuffer).split('/'))-1])
        # print("-" * 50)

        # print("A transmissão vai começar")
        # # Envia a quantidade de comandos para o client em hexadecimal
        # print(f"Enviando o número de comandos de: {len(str(rxBuffer).split('/'))-1}")
        # com1.sendData(np.asarray(n_rxBuffer))

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
