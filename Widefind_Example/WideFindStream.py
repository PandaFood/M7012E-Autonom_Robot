from threading import Thread
from rethinkdb import RethinkDB
import sys

class Node( dict ):
    _keys = "version id type pos vel bat time rssi".split()
    #Initializes a node from values
    def __init__(self, type = "none" , address = 0, vel = [0.0,0.0,0.0],
                 pos = [0.0,0.0,0.0], battery = 0.0, rssi = 0.0, version = "0.0.0"):
        self["id"] = address
        self["type"] = type
        self["pos"] = pos
        self["vel"] = vel
        self["bat"] = battery
        self["rssi"] = rssi
        self["version"] = version

    #Initializes a node from the DB response
    def __init__(self, rdb_rsp):
        print( rdb_rsp )
        self["id"] = rdb_rsp["id"]
        self["type"] = rdb_rsp["type"]
        self["pos"] = rdb_rsp["pos"]
        self["vel"] = rdb_rsp["vel"]
        self["bat"] = rdb_rsp["bat"]
        self["rssi"] = rdb_rsp["rssi"]
        self["version"] = rdb_rsp["version"]


    def __setitem__(self, key, val):
        if key not in Node._keys:
            raise KeyError
        dict.__setitem__(self, key, val)
    #     return self[key]

    def type(self):
        return self["type"]

    def battery(self):
        return self["bat"]

    def version(self):
        return self["version"]

    def position(self):
        return self["pos"]

    def velocity(self):
        return self["vel"]

    def id(self):
        return self["id"]

    def rssi(self):
        return self["rssi"]

    def version(self):
        return self["version"]

    def address(self):
        return self["address"]

class WfStream( Thread ):

    def __init__( self, callback, address = "localhost" , port = 28015 , password = "", db = "WIDEFIND"):

        self.r = RethinkDB()
        self.callback = callback
        try:

            self.cnx = self.r.connect( host=address, port=port, db=db).repl()
            print("Connected to DB")
        except:
            print(address)
            print(port)
            self.cnx = None
            print("Could not connect to db", sys.exc_info())

    def start(self):
        if self.cnx is not None:
            cursor = self.r.db( "WIDEFIND" ).table("current_state").changes().run( self.cnx )
            #cursor = self.r.db( "WIDEFIND" ).table("current_state").run( self.cnx )
            for document in cursor:
                print(document)
                #val =  document['new_val']
                #n =  Node( val )
                #self.callback( n )
        else:
            return "Not connected to server"

