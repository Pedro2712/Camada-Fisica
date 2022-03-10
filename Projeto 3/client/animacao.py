import os
import time
import threading

class Animacao:

    def __ini__(self):
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
    
    def getValor(self):
        return self.valor