from WideFindStream import WfStream
from time import sleep

def print_only_spot_info( nodeobj ):
    #print( nodeobj )
    if nodeobj.type() == "tag" :
        print(  "id:",
                nodeobj.id(),
                "pos:",
                nodeobj.position(),
                "battery:",
                nodeobj.battery(),
                "V")

# initialize the WfStream object with the connection details for the server and
# a callback function to be run when new/updated data arrives, the argument to
# the callback function is a "Node" object, containing all relevant data
t = WfStream(print_only_spot_info, "35.180.30.36", 28016, "UnlikelySnuggleBuild")

# start thread, callback will be run in the threads context
t.start()

while 1:
    sleep(1)

