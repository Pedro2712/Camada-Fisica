import os
import time
import threading
import multiprocessing as mp

class animation:

    def __ini__(self):
        self.animation_on= True

    def recebendo(self):
        print (self.animation_on)
        espera= 0.4
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
        recebe= mp.Process(target= self.recebendo, args= ())
        recebe.start()
    
    def disable(self):
        self.animation_on= False