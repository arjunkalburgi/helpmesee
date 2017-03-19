from picamera import PiCamera
from time import sleep
import os
camera = PiCamera()
camera.rotation = 270
camera.start_preview()
sleep(2)
camera.capture('/home/pi/nwHacks/try1.jpg')
camera.stop_preview()
