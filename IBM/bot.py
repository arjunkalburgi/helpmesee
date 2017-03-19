import subprocess

class Watson: 
	def __init__(self): 
		self.url = "https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classify?api_key=a565bbae556ab7df7a78d9ea788f170538281b2a&version=2016-05-20"

	def seeAnyone(self, filename): 
		return subprocess.call('curl -X POST -F "images_file=@' + filename + '" -F "parameters=@myparams.json "' + self.url + '"'