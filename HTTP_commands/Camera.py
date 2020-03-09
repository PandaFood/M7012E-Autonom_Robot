# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 10:22:24 2020

@author: ruben
"""

# importing the requests library 
# importing the requests library 
import requests 
import time
import http.server
import socketserver

Hdg = 42480/350
Vdg = 14562/120

def sayYes():
    URL="http://130.240.105.145/cgi-bin/aw_ptz?cmd=%23APC80005000&res=1"
    r = requests.get(url = URL) 
    time.sleep(1)
    URL="http://130.240.105.145/cgi-bin/aw_ptz?cmd=%23APC8000FF00&res=1"
    r = requests.get(url = URL) 
    time.sleep(1)
    URL="http://130.240.105.145/cgi-bin/aw_ptz?cmd=%23APC80005000&res=1"
    r = requests.get(url = URL) 
    time.sleep(1)
    URL="http://130.240.105.145/cgi-bin/aw_ptz?cmd=%23APC8000FF00&res=1"
    r = requests.get(url = URL) 
    time.sleep(1)
    
def convertDegrees(degrees, Cdg):
    degrees*=Cdg
    degrees = int(degrees)
    degrees+= (int("0x2d08",16)-5)
    degrees=hex(degrees)
    return str(degrees)[2:].upper()

def run(server_class=http.server.HTTPServer, handler_class=http.server.BaseHTTPRequestHandler):
    server_address = ('Camera_Server', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

print(convertDegrees(23,Vdg))   
#Range on the x dimension   
DMax="D2F8"
DMin="2D08"
D90X="5543"
D270="A97C"
DMitad="8000"

#Range on the y dimension
DUp="8E38"
D90Y="7FFF"
DDown="5556"
D45="6AAA"
DPrueba="7000"



# location given here 
location = "delhi technological university"
  
# defining a params dict for the parameters to be sent to the API 
  
# sending get request and saving the response as response object 
URL="http://130.240.105.145/cgi-bin/aw_ptz?cmd=%23APC"+convertDegrees(319,Vdg)+DPrueba+"&res=1"
r = requests.get(url = URL) 
#time.sleep(5)
#URL="http://130.240.105.145/cgi-bin/aw_ptz?cmd=%23APC"+DMitad+"7000&res=1"
#r = requests.get(url = URL) 
#time.sleep(5)
#URL="http://130.240.105.145/cgi-bin/aw_ptz?cmd=%23APC"+DMax+"7000&res=1"
#r = requests.get(url = URL) 
#time.sleep(5)
#URL="http://130.240.105.145/cgi-bin/aw_ptz?cmd=%23APC"+DMitad+"7000&res=1"
#r = requests.get(url = URL) 
#time.sleep(5)
#URL="http://130.240.105.145/cgi-bin/aw_ptz?cmd=%23APC"+DMin+"7000&res=1"
#r = requests.get(url = URL) 
