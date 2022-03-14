import os
import time
import threading
from colorama import init
from termcolor import colored

# use Colorama to make Termcolor work on Windows too
init()

class Animacao:

    def __init__(self):
        self.valor= True

    def enviando(self):
        while self.valor:
            os.system("cls")
            print ("enviando.")
            time.sleep(0.4)
            os.system("cls")
            print ("enviando..")
            time.sleep(0.4)
            os.system("cls")
            print ("enviando...")
            time.sleep(0.4)
            os.system("cls")
            print ("enviando")
            time.sleep(0.4)
    
    def enable(self):
        self.enviando= threading.Thread(target= self.enviando, args= ())
        self.enviando.start()
    
    def disable(self):
        self.valor= False
    
    def printProgressBar (self, iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = colored(fill * filledLength, 'green')
        falta= colored('-' * (length - filledLength), 'grey')
        print(f'\r{prefix} |{bar}{falta}| {percent}% {suffix} Arquivos: {iteration}/{total}', end = printEnd)
        # Print New Line on Complete
        if iteration == total: 
            print()
    
    def getValor(self):
        return self.valor