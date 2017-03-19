import picamera
from captionbot import CaptionBot
from GoogleAPI.visionbot import VisionBot
from IBM.bot import WatsonBot
import os

def takephoto():
	camera = picamera.PiCamera()
	camera.rotation = 270
	camera.capture('image.jpg')

def main(): 
	# TAKE THE PHOTO
	file = "image.jpg"
	takephoto()
	camera.stop()

	# ANALYZE THE PHOTO
	c = CaptionBot() 
	v = VisionBot()
	w = WatsonBot()

	print(c.file_caption(file))
	print(v.file_caption(file))
	print(w.see_anyone(file))

	# SPEAK TO THE USER 
	os.system("./speak.sh " + c.file_caption(file) +" "+ v.file_caption(file) +" "+ w.see_anyone(file))
	# STORE THE QUERY + INFO
	

if __name__ == '__main__':
	main()
