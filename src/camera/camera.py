import requests 
import time
import http.server
import socketserver

class Camera:
    def __init__(self):
        # Values for converting between camera hex and degrees
        self.Hdg = 42480/350
        self.Vdg = 14562/120

        #Range on the y dimension
        self.D45="6AAA"
        self.DPrueba="7000"
        
    
    def __convertDegrees(self, degrees, Cdg):
        degrees *= Cdg
        degrees = int(degrees)
        degrees += (int("0x2d08",16)-5)
        degrees=hex(degrees)
        return str(degrees)[2:].upper()

    def move(self, degrees):
        URL="http://130.240.105.145/cgi-bin/aw_ptz?cmd=%23APC" + self.__convertDegrees(degrees, self.Vdg) + self.D45 + "&res=1"
        r = requests.get(url = URL) 
        return r

# #Range on the x dimension   
# DMax="D2F8"
# DMin="2D08"
# D90X="5543"
# D270="A97C"
# DMitad="8000"

# #Range on the y dimension
# DUp="8E38"
# D90Y="7FFF"
# DDown="5556"
# D45="6AAA"
# DPrueba="7000"
