import paho.mqtt.client as mqtt
import datetime
import time
from datetime import datetime, timezone, timedelta, date
import sys
import json
import numpy as np
import threading
from math import acos, sqrt, pi
sys.path.insert(1, "..")
from camera.camera import Camera

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

class WidefindTracker( threading.Thread ):

   def __init__(self):
      threading.Thread.__init__(self)

      #MQTT IP for widefind
      self.broker_url = "130.240.114.24"
      self.broker_port = 1883

      #DATA must be sent inside an event object 
      self.event = {}
      self.pos = {}

      self.ids = []

      self.person = [0, 0, 0]
      self.p1 = [0, 0, 0]
      #self.cameraRoof = [3141, -3812, 1220]
      self.camera = [3261, -3800, 740]
      self.cameraFloor = [3635, -4074, 418]

      # Object controlling the camera
      self.c = Camera()

      self.following = False
      self.rotation = 0

      self.client = mqtt.Client()
      self.client.on_connect = self.on_connect
      self.client.on_message = self.on_message

   def run(self):
      self.client.connect(self.broker_url, self.broker_port)
      self.client.loop_start()

      # '#' means subcribe to all topics
      self.client.subscribe("#")

      while self.following:
         if abs(self.c.currentRotation() - self.rotation) > 5:
            if self.rotation < 20 or self.rotation > 340:
               self.c.rotate(0)
            else:
               self.c.rotate(self.rotation)

         time.sleep(1)

   def refreshToken(self, rc):
	   rc.login()
	   return rc.token

   def updatePerson(self, val):
      self.person = val

   def updateP1(self, val):
      self.p1 = val

   #def updateCameraFloor(val):
   #   global cameraFloor
   #   cameraFloor = val

   def follow(self):
      self.following = True

   def stop(self):
      self.following = False

   def on_connect(self, client, userdata, flags, rc):
      print("Connected With Result Code "+rc)

   def on_message(self, client, userdata, message):

      p1 = self.p1
      camera = self.camera
      cameraFloor = self.cameraFloor
      person = self.person

      mqttMsgString = message.payload.decode()
      mqttMsgJson = json.loads(mqttMsgString)

      # BEACON:96E9E196C540FE15,0.2.7,0,-4700,2700,4.00,-87.5,2051917,MAN,SAT*5B73
      mqttListIndex = mqttMsgJson["message"].split(',')

      self.pos["X"] = mqttListIndex[2]
      self.pos["Y"] = mqttListIndex[3]
      self.pos["Z"] = mqttListIndex[4]

      timeVar = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

      self.event["id"] = mqttListIndex[0][7:]
      self.event["version"] = mqttListIndex[1]
      self.event["time"] = mqttMsgJson["time"]
      self.event["type"] = "WideFind"
      self.event["pos"] = self.pos

      # Insert the widefind id of the sensor the person is wearing here
      if self.event["id"] == "F1587D88122BE247":
         self.updatePerson([int(self.pos["X"]), int(self.pos["Y"]), int(self.pos["Z"])])

      # Insert the widefind id of the sensor placed in the cameras 0 degree direction
      if self.event["id"] == "8F44CDEF5DC36678":
         self.updateP1([int(self.pos["X"]), int(self.pos["Y"]), int(self.pos["Z"])])

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
      new = Event(self.event["id"], self.pos["X"], self.pos["Y"], self.pos["Z"], self.event["time"])

      if(len(self.ids) == 0):
         self.ids.append(new) 
         print("no prior item in list. adding first")

      print(time.asctime( time.localtime(time.time()) )) 
      print(self.ids)
      print("Rotation: " + str(rotationDeg))
      print("CurrentRotation: " + str(self.c.currentRotation()))
      self.rotation = rotationDeg
      #print("Tilt: " + str(tiltDeg))

      for i, e in enumerate(self.ids):
         if(e.id == new.id):

            self.ids[i] = new
            return

      print(e.id + " is not same as " + new.id)
      self.ids.append(new)
