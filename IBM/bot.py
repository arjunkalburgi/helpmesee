import subprocess
import requests
import os
import json



class WatsonBot: 
	def __init__(self): 
		self.url = "https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classify?api_key=a565bbae556ab7df7a78d9ea788f170538281b2a&version=2016-05-20"

	def write_to_file(self, filename): 
		'''
			params = (
		    		('api_key', 'a565bbae556ab7df7a78d9ea788f170538281b2a'),
		    		('version', '2016-05-20'),
			)

			files = [
		    		('images_file', open('image.jpg', 'rb')),
		    		('parameters', open('myparams.json', 'rb')),
			]
		'''
		os.system('curl -o watsonSeeWatsonDo.json -X POST -F "images_file=@' + filename + '" -F "parameters=@IBM/myparams.json" "https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classify?api_key=a565bbae556ab7df7a78d9ea788f170538281b2a&version=2016-05-20"')

	def read_file(self): 
		with open('watsonSeeWatsonDo.json') as data_file:    
		    data = json.load(data_file)

		    sentence = ""

		    classifiers = [i["classes"][0]["class"] for i in data["images"][0]["classifiers"] if i["name"] == "nwHacks_1233774800"]
		    
		    first = True
		    for c in classifiers: 
		    	if first: 
		    		sentence = sentence + "Looks like you're with " + c
		    		first = False
		    	else: 
		    		sentence = sentence + " and " + c
		    	return sentence + ". "
		    return "Can't seem to make out anyone you know around."

	def see_anyone(self, filename): 
		self.write_to_file(filename)
		return self.read_file()

		