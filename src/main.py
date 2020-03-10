import sys

from camera.camera import Camera

c = Camera()

res = c.move(int(sys.argv[1]))
print(res)