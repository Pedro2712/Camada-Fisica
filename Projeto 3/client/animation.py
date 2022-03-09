import os
import time
import threading

class animation:

    def __ini__(self):
        self.animation_on= True

    def recebendo(self):
        espera= 0.15
        while self.animation_on:
            os.system("cls")
            print ("recebendo.")
            time.sleep(espera)
            os.system("cls")
            print ("recebendo..")
            time.sleep(espera)
            os.system("cls")
            print ("recebendo...")
            time.sleep(espera)
            os.system("cls")
            print ("recebendo")
    
    def enable(self):
        recebe= threading.Thread(target= self.recebendo, args= ())
        recebe.start()
    
    def disable(self):
        self.animation_on= False