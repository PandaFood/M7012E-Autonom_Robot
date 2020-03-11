from widefindScript import WidefindTracker
import time


print("starting... ")

wf = WidefindTracker('1')
print("initialized")
wf.start()
print("started")
wf.follow()
print("following now")
time.sleep(5)
print("stopping")
wf.stop()
print("stopped")