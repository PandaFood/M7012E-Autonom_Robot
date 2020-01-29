# WideFind server structure

This documents outlines the usage of the WideFind data stored in a server. The data is put into the
server by the WF-HUB unit, as long as it is connected to the internet and given the correct credentials

## Database

The server is running a Database called [RethinkDB](https://www.rethinkdb.com/) and is a real time
open source pub/sub NoSql database where everything is Json. Very easy to use,
with no typesafety whatsoever.

The database storing the system information is named "wf100"

The "wf100" database consists of 3 tables:

 - "maps" - Contains the maps as images, along with scaling, position and rotation information. The
 image is base64 encoded
 - "current_state" - contains information about all of the Nodes the system has seen, they always update
 to the latest state seen, so no old information is retained. This is the main database.
 - "cmd_requests" - Reserved for setting up the system. Sending information here might actually break
 the installation, and is thus not recommended

By using the 'current_state' table and listening to changes to it, the position data can be streamed

## Software

WideFind recommends using the official python driver called "rethinkdb" which can be installed using
the python package manager pip3

### Example stream data

WideFind supplies a very basic python3 streaming data implementation that starts a thread and outputs the
information in a callback function. The WfStream is very a small wrapper around the very easy to use
python interface supplied by rethinkdb, that only abstracts the subscriber part.

