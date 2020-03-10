import paho.mqtt.client as mqtt
#from rethinkdb import RethinkDB
import datetime
import time
from datetime import datetime,timezone, timedelta, date
import sys
import json
import numpy as np
from math import acos, sqrt, pi

#MQTT IP for widefind
broker_url = "130.240.114.24"
broker_port = 1883

#RETHINKDB
#r = RethinkDB()
#rethink_url = "localhost"
#rethink_port = 28015

def refreshToken(rc):
	rc.login()
	return rc.token


#DATA must be sent inside an event object 
event = {}
pos = {}

ids = []

person = [0, 0, 0]
p1 = [0, 0, 0]
camera = [3261, -3800, 740]
cameraFloor = [3568, -4051, 90]

def updatePerson(val):
   global person
   person = val

def updateP1(val):
   global p1
   p1 = val

class Event():
   def __init__(self, id, x, y, z, time):
      self.id = id
      self.x = x
      self.y = y
      self.z = z
      self.time = time
   def __str__(self):
      return "\t\t ID:" + self.id + " - " + "\t\t POS:" + self.x + ":" + self.y + ":" + self.z + "\t-\t\tstamp:" + self.time + "\n"
   def __repr__(self):
      return "\t\t ID:" + self.id + " - " + "\t\t POS:" + self.x + ":" + self.y + ":" + self.z + "\t-\t\tstamp:" + self.time + "\n"



def on_connect(client, userdata, flags, rc):
   print("Connected With Result Code "+rc)

def on_message(client, userdata, message):
   mqttMsgString = message.payload.decode()
   mqttMsgJson = json.loads(mqttMsgString)


   # BEACON:96E9E196C540FE15,0.2.7,0,-4700,2700,4.00,-87.5,2051917,MAN,SAT*5B73
   mqttListIndex = mqttMsgJson["message"].split(',')

   pos["X"] = mqttListIndex[2]
   pos["Y"] = mqttListIndex[3]
   pos["Z"] = mqttListIndex[4]

   timeVar= datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


   event["id"] = mqttListIndex[0][7:]
   event["version"] = mqttListIndex[1]
   event["time"] = mqttMsgJson["time"]
   event["type"] = "WideFind"
   event["pos"] = pos

   # Insert the widefind id of the sensor the person is wearing here
   if event["id"] == "8F44CDEF5DC36678":
      updatePerson([int(pos["X"]), int(pos["Y"]), int(pos["Z"])])

   # Insert the widefind id of the sensor placed in the cameras 0 degree direction
   if event["id"] == "F1587D88122BE247":
      updateP1([int(pos["X"]), int(pos["Y"]), int(pos["Z"])])

   # A vector in the direction of the camera when the camera is rotated 0 degrees
   # p1 is a widefind sensor placed somewhere in that direction
   v1 = [p1[0] - camera[0], p1[1] - camera[1], p1[2] - camera[2]]

   # A vector from the camera to a person wearing a widefind sensor
   vp = [person[0] - camera[0], person[1] - camera[1], person[2] - camera[2]]

   # Calculate which side of the room the person is at
   # side < 0 => bedroom side of the room
   # side > 0 => kitchen side of the room
   # https://math.stackexchange.com/questions/214187/point-on-the-left-or-right-side-of-a-plane-in-3d-space

   bprim = [cameraFloor[0] - camera[0], cameraFloor[1] - camera[1], cameraFloor[2] - camera[2]]
   cprim = [p1[0] - camera[0], p1[1] - camera[1], p1[2] - camera[2]]
   xprim = [person[0] - camera[0], person[1] - camera[1], person[2] - camera[2]]

   matrix = np.array([bprim, cprim, xprim])
   side = np.linalg.det(matrix)

   # Calculate the angle between v1 and vp using the dot product
   theta = acos( (v1[0] * vp[0] + v1[1] * vp[1] + v1[2] * vp[2]) / ( sqrt(v1[0]**2 + v1[1]**2 + v1[2]**2) * sqrt(vp[0]**2 + vp[1]**2 + vp[2]**2) ) )
   thetaDeg = theta * 180/pi

   if(side < 0):
      thetaDeg = 360 - thetaDeg

   msg = ""
   new = Event(event["id"], pos["X"], pos["Y"], pos["Z"], event["time"])

   #print(new)

   if(len(ids) == 0):
      ids.append(new) 
      print("no prior item in list. adding first")

   print(time.asctime( time.localtime(time.time()) )) 
   print(ids)
   print(thetaDeg)

   for i, e in enumerate(ids):
      if(e.id == new.id):

         ids[i] = new
         return

   print(e.id + " is not same as " + new.id)
   ids.append(new)

   # if(event.x not in ids):
   #    ids.append(event["pos"])
   #    print(event)

   # if(str(event["id"]) not in ids):
   #    msg = r.table('current_state').insert(event).run(conn)
   #    ids.append(str(event["id"]))
   # else:
   #    msg = r.table('current_state').replace(event).run(conn)


#   print(event)
   #print( msg )




client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_url, broker_port)

# msg = {
#    'host': 'WFGATEWAY-3ABFF8D01EFF', 
#    'message': 'BEACON:96E9E196C540FE15,0.2.7,0,-4700,2700,4.00,-87.3,1183981,MAN,SAT*9383', 
#    'source': '03FF5C0A2BFA3A9B', 
#    'time': '2020-02-07T11:33:12.854889928Z', 
#    'type': 'widefind_message'
#    }

#conn = r.connect(host=rethink_url, port=rethink_port, db="WIDEFIND" ).repl()

#rint ('Creating app database...')
#try:
#   r.db_create('WIDEFIND').run(conn)
#   r.db('WIDEFIND').table_create('current_state').run(conn)
#   print ('App database created.')
#except:
#   print( 'App database already exists. Continuing')

client.loop_start()

# '#' means subcribe to all topics
client.subscribe("#")

while True:
    time.sleep(1)
