import paho.mqtt.client as mqtt
import PythonRESTClient as RESTClient
import datetime
import time
from datetime import datetime,timezone, timedelta, date
import sys
import json

#MQTT IP for widefind
broker_url = "130.240.114.24"
broker_port = 1883

#out_data_path = "../data/weaklabels2/"
out_data_path="./"

#userslist = ['472491134@qq.com']#,' sy17@mails.tsinghua.edu.cn']#['moto@test.co.uk','xperia@test.co.uk']
blacklist = ['h2al']#NO DATA EXPECTED FOR ADMIN THEREFORE IS IN BLACKLIST (no data downloaded for users in blacklist)
entrypoint = "b4401.lab.ltu.se"
port = "8080"
#username = "472491134@qq.com" #
#password = "2016213647" #
#USING AN ADMIN ACCOUNT TO DOWNLOAD DATA
username = "DoorSensor@gmail.com"
password = "Door2019"

aggregator = RESTClient.PythonRESTClient(entrypoint,username,password,port)


def refreshToken(rc):
	rc.login()
	return rc.token

print("Logging in...")
response_status, response_body = aggregator.login()

token = aggregator.token

print("Token: ", aggregator.token)

user_id =  response_body["id"]
user_name = response_body["personalData"]["userName"]

#DATA must be sent inside an event object 
event = {}


#for raw data measurement use the data field oin the event
#in this example every event contains two 
#event["data"] = aggregator.encode_data("x1,y1,z1,t1\nx2,y2,z2,t2\nx3,y3,z3,t3\n")



def on_connect(client, userdata, flags, rc):
   print("Connected With Result Code "+rc)

def on_message(client, userdata, message):
   #print("Message Recieved: "+message.payload.decode())
   mqttMsgString = message.payload.decode()
   mqttMsgJson = json.loads(mqttMsgString)
   #if (mqttMsgJson["message"][0:6] == "REPORT"):
   print(mqttMsgJson)
   mqttListIndex = mqttMsgJson["message"].split(',')
   mqttXVar = mqttListIndex[2]
   mqttYVar = mqttListIndex[3]
   mqttZVar = mqttListIndex[4]
   timeVar= datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
   event["startTime"] = timeVar+".000+0100"
   event["endTime"] = timeVar+".000+0100"
   event["type"] = "WideFind"
   if ((int(mqttXVar) < 3150) and (int(mqttYVar) < -2000)):
      event["label"] = "Kitchen"
   else:
      event["label"] = "Livingroom"


      # All events must be sent as a list of evevnts
      # in case of a single event you add only an event to the list
   events = {"events":[]}
   events["events"].append(event)

      #performing PUSH data query
#      aggregator.addEvents(user_id,events)
#   time.sleep(5)



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_url, broker_port)
client.loop_start()

# '#' means subcribe to all topics
client.subscribe("#")

while True:
    time.sleep(1)
