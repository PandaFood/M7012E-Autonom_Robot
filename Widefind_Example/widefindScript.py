import paho.mqtt.client as mqtt
from rethinkdb import RethinkDB
import datetime
import time
from datetime import datetime,timezone, timedelta, date
import sys
import json

#MQTT IP for widefind
broker_url = "130.240.114.24"
broker_port = 1883

#RETHINKDB
r = RethinkDB()
rethink_url = "localhost"
rethink_port = 28015

def refreshToken(rc):
	rc.login()
	return rc.token


#DATA must be sent inside an event object 
event = {}
pos = {}

ids = []


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

   msg = ""

   if(str(event["id"]) not in ids):
      msg = r.table('current_state').insert(event).run(conn)
      ids.append(str(event["id"]))
   else:
      msg = r.table('current_state').replace(event).run(conn)


   #print(event)
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

conn = r.connect(host=rethink_url, port=rethink_port, db="WIDEFIND" ).repl()

print ('Creating app database...')
try:
   r.db_create('WIDEFIND').run(conn)
   r.db('WIDEFIND').table_create('current_state').run(conn)
   print ('App database created.')
except:
   print( 'App database already exists. Continuing')

client.loop_start()

# '#' means subcribe to all topics
client.subscribe("#")

while True:
    time.sleep(1)
