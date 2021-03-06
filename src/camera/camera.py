import requests, time

class Camera:

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

    def __init__(self):
        # Values for converting between camera hex and degrees
        self.Hdg = 42480/350
        self.Vdg = 14562/120

        self.BASEURL = "http://130.240.105.145/cgi-bin/aw_ptz?cmd=%23"

        #Range on the y dimension
        self.D45="6AAA"
        self.DPrueba="7000"

        self.rotation = 0
        
    
    def __convertDegrees(self, degrees, Cdg):
        degrees *= Cdg
        degrees = int(degrees)
        degrees += (int("0x2d08",16)-5)
        degrees=hex(degrees)
        return str(degrees)[2:].upper()

    def rotate(self, degrees):
        URL="http://130.240.105.145/cgi-bin/aw_ptz?cmd=%23APC" + self.__convertDegrees(degrees, self.Vdg) + self.D45 + "&res=1"
        r = requests.get(url = URL) 

        if r.status_code == 200:
            self.rotation = degrees
        
        return r

    def currentRotation(self):
        return self.rotation

    def move(self, degrees):
        degrees = self.__convertDegrees(degrees, self.Hdg)
        return self.__sendCommand(self.__createMovementURL(degrees, self.D45))
    
    def stop(self):
        return self.__sendCommand()

    def start(self):
        pass



