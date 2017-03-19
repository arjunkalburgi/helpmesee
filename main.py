import picamera
from captionbot import CaptionBot
from GoogleAPI.visionbot import VisionBot
from IBM.bot import Watson

def takephoto():
	camera = picamera.PiCamera()
	camera.rotation = 270
	camera.capture('image.jpg')

def main(): 
	file = "image.jpg"
	takephoto()

	c = CaptionBot() 
	v = VisionBot()
	w = Watson()

	print(c.file_caption(file))
	print(v.file_caption(file))
	print(w.seeAnyone(file))

if __name__ == '__main__':
	main()
