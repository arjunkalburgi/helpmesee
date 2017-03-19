import picamera
from captionbot import CaptionBot
from GoogleAPI.visionbot import VisionBot
from IBM.bot import WatsonBot

def takephoto():
	camera = picamera.PiCamera()
	camera.rotation = 270
	camera.capture('image.jpg')

def main(): 
	file = "image.jpg"
	takephoto()

	c = CaptionBot() 
	v = VisionBot()
	w = WatsonBot()

	print(c.file_caption(file))
	print(v.file_caption(file))
	print(w.see_anyone(file))

	camera.stop()

if __name__ == '__main__':
	main()
