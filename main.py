from Camera import CameraBot

from captionbot import CaptionBot
from GoogleAPI.visionbot import VisionBot
from IBM.bot import WatsonBot

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

	# STORE THE QUERY + INFO
	

if __name__ == '__main__':
	main()
