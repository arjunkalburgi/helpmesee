# Pi Dependencies 
# import picamera
import json

# Google Dependencies 
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

# Image Dependencies 
import base64

class VisionBot: 
	def __init__(self):
		self.credentials = GoogleCredentials.get_application_default()
		self.service = discovery.build('vision', 'v1', credentials=self.credentials)

	# def takephoto(self):
	#     camera = picamera.PiCamera()
	#     camera.capture('image.jpg')

	def analyzephoto(self, filename): 
		'''
			input type is a string
			FACE_DETECTION | LABEL_DETECTION | TEXT_DETECTION
			LANDMARK_DETECTION | LOGO_DETECTION 

			return a dictionary with important info from image analysis
			which has confidence over 75%
		'''
		returndict = {"FACE_DETECTION": [], 
			"LABEL_DETECTION": {"low": [], "mid": [], "high": []},
			"LANDMARK_DETECTION": {"low": [], "mid": [], "high": []},
			"LOGO_DETECTION": {"low": [], "mid": [], "high": []},
			"TEXT_DETECTION": []}

		# credentials = GoogleCredentials.get_application_default()
		# service = discovery.build('vision', 'v1', credentials=credentials)

		with open(filename, 'rb') as image:
			image_content = base64.b64encode(image.read())
			service_request = self.service.images().annotate(body={
			    'requests': [{
			        'image': {
			            'content': image_content.decode('UTF-8')
			        },
			        'features': [{
				            'type': "FACE_DETECTION",
				            'maxResults': 5
				        }, {
				            'type': "LABEL_DETECTION",
				            'maxResults': 5
				        }, {
				            'type': "TEXT_DETECTION",
				            'maxResults': 5
				        }, {
				            'type': "LANDMARK_DETECTION",
				            'maxResults': 5
				        }, {
				            'type': "LOGO_DETECTION",
				            'maxResults': 5
				        }
			        ]
			    }]
			})
			response = service_request.execute()

			print json.dumps(response, sort_keys=True, indent=4)

			# FACES
			if "faceAnnotations" in response["responses"][0]:
				faceres = response["responses"][0]["faceAnnotations"]
				emotions = [("joyLikelihood", "joy"), ("sorrowLikelihood", "sorrow"), ("angerLikelihood", "anger"), ("surpriseLikelihood", "shock")]
				i = 0
				for face in faceres: 
					returndict["FACE_DETECTION"].append({"low": "", "mid": "", "high": ""})
					for emo in emotions: 
						if face[emo[0]] > 0.9: 
							returndict["FACE_DETECTION"][i]["high"] = emo[1]
						elif face[emo[0]] > 0.8: 
							returndict["FACE_DETECTION"][i]["mid"] = emo[1]
						elif face[emo[0]] > 0.7: 
							returndict["FACE_DETECTION"][i]["low"] = emo[1]
					i = i + 1

			# LABELS 
			if "labelAnnotations" in response["responses"][0]:
				labelres = response["responses"][0]["labelAnnotations"]
				for label in labelres: 
					if label["score"] > 0.9: 
						returndict["LABEL_DETECTION"]["high"].append(label["description"])
					elif label["score"] > 0.8: 
						returndict["LABEL_DETECTION"]["mid"].append(label["description"])
					elif label["score"] > 0.7: 
						returndict["LABEL_DETECTION"]["low"].append(label["description"])

			# TEXT 
			if "textAnnotations" in response["responses"][0]:
				textres = response["responses"][0]["textAnnotations"]
				for text in textres: 
					if "locale" in text: 
						returndict["TEXT_DETECTION"].append(text["description"])

			# LANDMARK 
			if "landmarkAnnotations" in response["responses"][0]:
				landres = response["responses"][0]["landmarkAnnotations"]
				for landmark in landres: 
					if landmark["score"] > 0.9:
						returndict["LANDMARK_DETECTION"]["high"].append(landmark["description"])
					elif landmark["score"] > 0.8: 
						returndict["LANDMARK_DETECTION"]["mid"].append(landmark["description"])
					elif landmark["score"] > 0.7: 
						returndict["LANDMARK_DETECTION"]["low"].append(landmark["description"])

			# LOGO
			if "logoAnnotations" in response["responses"][0]:
				logores = response["responses"][0]["logoAnnotations"]
				for logo in logores: 
					if logo["score"] > 0.9:
						returndict["LOGO_DETECTION"]["high"].append(logo["description"])
					elif logo["score"] > 0.8: 
						returndict["LOGO_DETECTION"]["mid"].append(logo["description"])
					elif logo["score"] > 0.7: 
						returndict["LOGO_DETECTION"]["low"].append(logo["description"])

		return returndict

	def speakanalysis(self, photoanalysis): 
		'''
		photoanalysis = {"FACE_DETECTION": [{"low": [], "mid": [], "high": []}], 
			"LABEL_DETECTION": {"low": [], "mid": [], "high": []},
			"LANDMARK_DETECTION": {"low": [], "mid": [], "high": []},
			"LOGO_DETECTION": {"low": [], "mid": [], "high": []},
			"TEXT_DETECTION": []}

		Goes through photoanalysis and makes a sentence 

		"I think it's " or " with " or ""
			face: a face that's happy/sad/mad/shocked 
			label: (if doesn't end in an s) "a " + label, (else): label
			landmark: "the " + landmark
			logo: "the " + logo + " logo"
			text: "with the text " + text

		{'FACE_DETECTION': [{'high': ['joy'], 'low': [], 'mid': []}, {'high': ['anger'], 'low': [], 'mid': []}], 
		'TEXT_DETECTION': ['Wake up human!\n'], 
		'LOGO_DETECTION': {'high': [], 'low': [], 'mid': []}, 
		'LANDMARK_DETECTION': {'high': [], 'low': [], 'mid': []}, 
		'LABEL_DETECTION': {'high': ['cat', 'mammal'], 'low': ['whiskers'], 'mid': []}}
		'''
		# photoanalysis = photoanalysisarray[0]


		sentence = ""


		highconflabels = photoanalysis["LABEL_DETECTION"]["high"]
		midconflabels = photoanalysis["LABEL_DETECTION"]["mid"]
		lowconflabels = photoanalysis["LABEL_DETECTION"]["low"]
		if highconflabels or midconflabels or lowconflabels: 
			carryover = False
			if highconflabels: 
				sentence = sentence + "I can see "
				first = True
				for label in highconflabels: 
					if first: 
						if label[-1] == "s": 
							sentence = sentence + "a "
						sentence = sentence + label + " "
					else: 
						if label[-1] == "s": 
							sentence = sentence + "and a"+ label + " "
						else: 
							sentence = sentence + "and "+ label + " "
			elif midconflabels: 
				sentence = sentence + "I think I can see "
				first = True
				for label in midconflabels: 
					if first: 
						if label[-1] == "s": 
							sentence = sentence + "a "
						sentence = sentence + label + " "
					else: 
						if label[-1] == "s": 
							sentence = sentence + "and a"+ label + " "
						else: 
							sentence = sentence + "and "+ label + " "
			elif lowconflabels: 
				sentence = sentence + "I might be seeing "
				first = True
				for label in lowconflabels: 
					if first: 
						if label[-1] == "s": 
							sentence = sentence + "a "
						sentence = sentence + label + " "
					else: 
						if label[-1] == "s": 
							sentence = sentence + "and a"+ label + " "
						else: 
							sentence = sentence + "and "+ label + " "
			sentence = sentence.strip() + ". "

		text = photoanalysis["TEXT_DETECTION"]
		if len(text) > 0: 
			sentence = sentence + "can read text saying "
			first = True
			for t in text: 
				if first: 
					sentence = sentence + t
				else: 
					sentence = sentence + "and " + t
			sentence = sentence.strip() + ". "
		
		if len(photoanalysis["FACE_DETECTION"]) > 0: 
			if len(photoanalysis["FACE_DETECTION"]) > 1: 
				sentence = sentence + "There are " + str(len(photoanalysis["FACE_DETECTION"])) + " faces showing "
				# ONE EMOTION PER FACE
				emos = {"high": [], "mid": [], "low": []}
				for face in photoanalysis["FACE_DETECTION"]: 
					if len(face["high"]) > 0: 
						emos["high"].append(face["high"])
					if len(face["mid"]) > 0: 
						emos["mid"].append(face["mid"])
					if len(face["low"]) > 0: 
						emos["low"].append(face["low"])
				if len(face["high"]) > 0: 
					first = True
					for emo in face["high"]: 
						if first: 
							sentence = sentence + emo + " "
							first = False
						else: 
							sentence = sentence + "and " + emo + " "
					if len(face["mid"]) or len(face["low"]): 
						sentence = sentence + ", "
				if len(face["mid"]) > 0: 
					sentence = sentence + "signs of "
					first = True
					for emo in face["mid"]: 
						if first: 
							sentence = sentence + emo + " "
							first = False
						else: 
							sentence = sentence + "and " + emo + " "
					if len(face["low"]): 
						sentence = sentence + ", "
				if len(face["low"]) > 0: 
					sentence = sentence + "slight signs of "
					first = True
					for emo in face["low"]: 
						if first: 
							sentence = sentence + emo + " "
							first = False
						else: 
							sentence = sentence + "and " + emo + " "
				sentence = sentence.strip() + ". "
			else: 
				sentence = sentence + "There is one face that "

				highconfface = photoanalysis["FACE_DETECTION"][0]["high"]
				midconfface = photoanalysis["FACE_DETECTION"][0]["mid"]
				lowconfface = photoanalysis["FACE_DETECTION"][0]["low"]

				if highconfface: 
					sentence = sentence + "is expressing " + highconfface + ". "
				elif midconfface: 
					sentence = sentence + "seems to express " + midconfface + ". "
				elif lowconfface: 
					sentence = sentence + "could be expressing " + highconfface + ". "

		highconflandmark = photoanalysis["LANDMARK_DETECTION"]["high"]
		midconflandmark = photoanalysis["LANDMARK_DETECTION"]["mid"]
		lowconflandmark = photoanalysis["LANDMARK_DETECTION"]["low"]
		if highconflandmark or midconflandmark or lowconflandmark: 
			sentence = sentence + "Looks like "
			if highconflandmark: 
				sentence = sentence + "you're in "
				first = True
				for mark in highconflandmark: 
					if first: 
						sentence = sentence + mark + " "
					else: 
						sentence = sentence + "or " + mark + " "
			elif midconflandmark: 
				sentence = sentence + "you could be in "
				first = True
				for mark in midconflandmark: 
					if first: 
						sentence = sentence + mark + " "
					else: 
						sentence = sentence + "or " + mark + " "
			elif lowconflandmark: 
				sentence = sentence + "you might be in "
				first = True
				for mark in lowconflandmark: 
					if first: 
						sentence = sentence + mark + " "
					else: 
						sentence = sentence + "or " + mark + " "
			sentence = sentence + "."

		highconflogo = photoanalysis["LOGO_DETECTION"]["high"]
		midconflogo = photoanalysis["LOGO_DETECTION"]["mid"]
		lowconflogo = photoanalysis["LOGO_DETECTION"]["low"]
		if highconflogo or midconflogo or lowconflogo: 
			sentence = sentence + "Looks like "
			if highconflogo: 
				sentence = sentence + "there's a "
				first = True
				for logo in highconflogo: 
					if first: 
						sentence = sentence + logo + " "
					else: 
						sentence = sentence + "or " + logo + " "
			elif midconflogo: 
				sentence = sentence + "could be a "
				first = True
				for logo in midconflogo: 
					if first: 
						sentence = sentence + logo + " "
					else: 
						sentence = sentence + "or " + logo + " "
			elif lowconflogo: 
				sentence = sentence + "there might be a "
				first = True
				for logo in lowconflogo: 
					if first: 
						sentence = sentence + logo + " "
					else: 
						sentence = sentence + "or " + logo + " "
			sentence = sentence + "logo here."

		return sentence

	def file_caption(self, filename): 

		photoanalysis = self.analyzephoto(filename)
		return self.speakanalysis(photoanalysis)
		
		# SAVE PHOTO AND DATA
		# storedetection(photoanalysis)


