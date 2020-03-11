import paho.mqtt.client as mqtt
import datetime
import time
from datetime import datetime, timezone, timedelta, date
import sys
import json
import numpy as np
from math import acos, sqrt, pi
sys.path.insert(1, "..")
from camera.camera import Camera

#MQTT IP for widefind
broker_url = "130.240.114.24"
broker_port = 1883

def refreshToken(rc):
	rc.login()
	return rc.token


#DATA must be sent inside an event object 
event = {}
pos = {}

ids = []

person = [0, 0, 0]
p1 = [0, 0, 0]
#cameraRoof = [3141, -3812, 1220]
camera = [3261, -3800, 740]
cameraFloor = [3635, -4074, 418]

# Object controlling the camera
c = Camera()
currentRotation = 0

def updatePerson(val):
   global person
   person = val

def updateP1(val):
   global p1
   p1 = val

#def updateCameraFloor(val):
#   global cameraFloor
#   cameraFloor = val

def updateRotation(val):
   global currentRotation
   currentRotation = val

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
   if event["id"] == "F1587D88122BE247":
      updatePerson([int(pos["X"]), int(pos["Y"]), int(pos["Z"])])

   # Insert the widefind id of the sensor placed in the cameras 0 degree direction
   if event["id"] == "8F44CDEF5DC36678":
      updateP1([int(pos["X"]), int(pos["Y"]), int(pos["Z"])])

   # Insert the widefind id of the sensor on the floor right beneath the camera
   #if event["id"] == "AD9C473EACA8830B":
   #   updateCameraFloor([int(pos["X"]), int(pos["Y"]), int(pos["Z"])])

   # A vector in the direction of the camera when the camera is rotated 0 degrees
   # p1 is a widefind sensor placed somewhere in that direction
   v1 = [p1[0] - camera[0], p1[1] - camera[1], p1[2] - camera[2]]

   # A vector from the camera in the roof, to the floor right underneath the camera.
   #v2 = [cameraFloor[0] - cameraRoof[0], cameraFloor[1] - cameraRoof[1], cameraFloor[2] - cameraRoof[2]]

   # A vector from the camera (at the same height as a person would wear it, i.e not at roof height nor floor height) to a person wearing a widefind sensor
   vp = [person[0] - camera[0], person[1] - camera[1], person[2] - camera[2]]

   # A vector from the camera (at roof height) to a person wearing a widefind sensor
   #vcp = [person[0] - cameraRoof[0], person[1] - cameraRoof[1], person[2] - cameraRoof[2]]

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
   rotation = acos((v1[0] * vp[0] + v1[1] * vp[1] + v1[2] * vp[2]) / (sqrt(v1[0]**2 + v1[1]**2 + v1[2]**2) * sqrt(vp[0]**2 + vp[1]**2 + vp[2]**2)))
   rotationDeg = rotation * 180/pi

   # Calculate the angle between v2 and vcp using the dot product
   #tilt = acos((v2[0] * vcp[0] + v2[1] * vcp[1] + v2[2] * vcp[2]) / (sqrt(v2[0]**2 + v2[1]**2 + v2[2]**2) * sqrt(vcp[0]**2 + vcp[1]**2 + vcp[2]**2)))
   #tiltDeg = tilt * 180/pi

   if(side < 0):
      rotationDeg = 360 - rotationDeg

   msg = ""
   new = Event(event["id"], pos["X"], pos["Y"], pos["Z"], event["time"])

   if(len(ids) == 0):
      ids.append(new) 
      print("no prior item in list. adding first")

   print(time.asctime( time.localtime(time.time()) )) 
   print(ids)
   print("Rotation: " + str(rotationDeg))
   #print("Tilt: " + str(tiltDeg))

   # Dont rotate if the difference of the new and old rotation is less than 10, to prevent shakiness
   if abs(currentRotation - rotationDeg) > 10:
      c.rotate(rotationDeg)
      updateRotation(rotationDeg)


   for i, e in enumerate(ids):
      if(e.id == new.id):

         ids[i] = new
         return

   print(e.id + " is not same as " + new.id)
   ids.append(new)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_url, broker_port)
client.loop_start()

# '#' means subcribe to all topics
client.subscribe("#")

while True:
    time.sleep(1)
