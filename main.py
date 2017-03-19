import picamera
from captionbot import CaptionBot
from GoogleAPI.visionbot import VisionBot
import subprocess
import requests
import os

def takephoto():
	camera = picamera.PiCamera()
	camera.rotation = 270
	camera.capture('image.jpg')

def main(): 
	file = "image.jpg"
	takephoto()

	c = CaptionBot() 
	v = VisionBot()
	
	print(c.file_caption(file))
	print(v.file_caption(file))
	#bash_com = 'curl -X POST -F "images_file=@image.jpg" -F "parameters=@myparams.json" "https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classify?api_key=a565bbae556ab7df7a78d9ea788f170538281b2a&version=2016-05-20'
	#subprocess.Popen(bash_com)
	#output = subprocess.check_output(['bash','-c', bash_com])


	params = (
    		('api_key', 'a565bbae556ab7df7a78d9ea788f170538281b2a'),
    		('version', '2016-05-20'),
	)

	files = [
    		('images_file', open('image.jpg', 'rb')),
    		('parameters', open('myparams.json', 'rb')),
	]

	#output=requests.post('https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classify', params=params, files=files)

	os.system('curl -o watsonSeeWatsonDo.txt -X POST -F "images_file=@image.jpg" -F "parameters=@myparams.json" "https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classify?api_key=a565bbae556ab7df7a78d9ea788f170538281b2a&version=2016-05-20"')

	print('IBM:')
	#print(output)
	#print(output.json())
	camera.stop()

if __name__ == '__main__':
	main()
