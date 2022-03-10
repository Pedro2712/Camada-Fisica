import os
import time
import threading

class Animacao:

    def __ini__(self):
        self.valor= True

    def recebendo(self):
        while self.valor:
            os.system("cls")
            print ("recebendo.")
            time.sleep(0.4)
            os.system("cls")
            print ("recebendo..")
            time.sleep(0.4)
            os.system("cls")
            print ("recebendo...")
            time.sleep(0.4)
            os.system("cls")
            print ("recebendo")
        os.system("cls")
    
    def enable(self):
        self.recebendo= threading.Thread(target= self.recebendo, args= ())
        self.recebendo.start()
    
    def disable(self):
        self.valor= False
    
    def getValor(self):
        return self.valor