import picamera
from captionbot import CaptionBot
from GoogleAPI.visionbot import VisionBot

def takephoto():
	camera = picamera.PiCamera()
	camera.capture('image.jpg')
<<<<<<< HEAD
	print(1)
=======
>>>>>>> 32a880d9db54632d0f5d067c8d92d532df467ef7

def main(): 
	file = "image.jpg"
	takephoto()

	c = CaptionBot() 
	v = VisionBot()

	print(c.file_caption(file))
	print(v.file_caption(file))
<<<<<<< HEAD

if __name__ == '__main__':
	main()
=======
>>>>>>> 32a880d9db54632d0f5d067c8d92d532df467ef7
