import picamera
from captionbot import CaptionBot
from GoogleAPI.visionbot import VisionBot

def takephoto():
	camera = picamera.PiCamera()
	camera.capture('image.jpg')
	print(1)

def main(): 
	file = "image.jpg"
	takephoto()

	c = CaptionBot() 
	v = VisionBot()

	print(c.file_caption(file))
	print(v.file_caption(file))

if __name__ == '__main__':
	main()
