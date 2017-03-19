from Camera import CameraBot

from captionbot import CaptionBot
from GoogleAPI.visionbot import VisionBot
from IBM.bot import WatsonBot
import os

def main(): 
	file = "image.jpg"

	# TAKE THE PHOTO
	cam = CameraBot()
	cam.takephoto(file)
	cam.closecam()

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
