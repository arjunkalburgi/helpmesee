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

	prediction = c.file_caption(file) + v.file_caption(file) + w.see_anyone(file)
	print (prediction)
	prediction.decode('unicode_escape').encode('ascii','ignore')
	# SPEAK TO THE USER 
	os.system("./speech.sh " + prediction)
	# STORE THE QUERY + INFO
	

if __name__ == '__main__':
	main()
