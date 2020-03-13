from widefindScript import WidefindTracker
import time


print("starting... ")

wf = WidefindTracker()
print("initialized")
wf.run()
print("started")

while True:
    wf.help()
    time.sleep(10)
