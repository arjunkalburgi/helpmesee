import serial
import os

from Camera import CameraBot
from captionbot import CaptionBot
from GoogleAPI.visionbot import VisionBot
from IBM.bot import WatsonBot
from Store.storebot import CockroachBot

ser = serial.Serial('/dev/ttyACM0',9600)
s = [0,1]

cam = CameraBot()
cap = CaptionBot() 
vis = VisionBot()
wat = WatsonBot()
sto = CockroachBot()
sto.newfolder()

def main(): 
	file = "image.jpg"

	# TAKE THE PHOTO
	cam.takephoto(file)
	cam.closecam()

	# ANALYZE THE PHOTO
	caption = cap.file_caption(file)
	vision = vis.file_caption(file)
	watson = wat.see_anyone(file)

	print(caption)
	print(vision)
	print(watson)

	# SPEAK TO THE USER 

	# STORE THE QUERY + INFO
	path = sto.movefile(file)
	sto.log(path, caption, vision, watson)

while True:

	read_serial=ser.readline()
	print read_serial

	if read_serial!="":
		print "TAKE PICTURE"
		#PUT func here test1.main()
		main()



