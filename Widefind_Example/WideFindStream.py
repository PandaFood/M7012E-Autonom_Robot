from threading import Thread
from rethinkdb import RethinkDB

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

    # def __getitem__(self, key):
    #     if key not in Node._keys:
    #         raise KeyError
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

    def __init__( self, callback, address = "localhost" , port = 28015 , password = ""):

        self.r = RethinkDB()
        self.callback = callback
        try:
            self.cnx = r.connect( host = address, port = port, user = "admin", password = password ).repl()
            print("Connected to DB")
        except:
            self.cnx = None
            print("Could not connect to db")

    def start(self):
        if self.cnx is not None:
            cursor = r.db( "wf100" ).table("current_state").changes().run( self.cnx )
            #cursor = r.db( "wf100" ).table("current_state").run( self.cnx )
            for document in cursor:
                val =  document['new_val']
                n =  Node( val )
                self.callback( n )
        else:
            return "Not connected to server"

