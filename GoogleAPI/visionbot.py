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
		returndict = {"FACE_DETECTION": {"low": [], "mid": [], "high": []}, 
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

			# print()

			# FACES
			faceres = response["responses"][0]["faceAnnotations"][0]
			emotions = [("joyLikelihood", "joy"), ("sorrowLikelihood", "sorrow"), ("angerLikelihood", "anger"), ("surpriseLikelihood", "shock")]
			i = 0
			for face in faceres: 
				returndict["FACE_DETECTION"][i] = {"low": "", "mid": "", "high": ""}
				for emo in emotions: 
					if face[emo[0]] > 0.9: 
						returndict["FACE_DETECTION"][i]["high"] = emo[1]
						num_high_conf = num_high_conf + 1
					elif face[emo[0]] > 0.8: 
						returndict["FACE_DETECTION"][i]["mid"] = emo[1]
						num_mid_conf = num_mid_conf + 1
					elif face[emo[0]] > 0.7: 
						returndict["FACE_DETECTION"][i]["low"] = emo[1]
						num_low_conf = num_low_conf + 1
				i = i + 1

			# LABELS 
			labelres = response["responses"][0]["labelAnnotations"]
			for label in labelres: 
				if label["score"] > 0.9: 
					returndict["LABEL_DETECTION"]["high"].append(label["description"])
					num_high_conf = num_high_conf + 1
				elif label["score"] > 0.8: 
					returndict["LABEL_DETECTION"]["mid"].append(label["description"])
					num_mid_conf = num_mid_conf + 1
				elif label["score"] > 0.7: 
					returndict["LABEL_DETECTION"]["low"].append(label["description"])
					num_low_conf = num_low_conf + 1

			# TEXT 
			textres = response["responses"][0]["textAnnotations"]
			for text in textres: 
				if "locale" in text: 
					returndict["TEXT_DETECTION"].append(text["description"])

			# LANDMARK 
			landres = response["responses"][0]["landmarkAnnotations"]
			for landmark in landres: 
				if landmark["score"] > 0.9:
					returndict["LANDMARK_DETECTION"]["high"].append(landmark["description"])
					num_high_conf = num_high_conf + 1
				elif landmark["score"] > 0.8: 
					returndict["LANDMARK_DETECTION"]["mid"].append(landmark["description"])
					num_mid_conf = num_mid_conf + 1
				elif landmark["score"] > 0.7: 
					returndict["LANDMARK_DETECTION"]["low"].append(landmark["description"])
					num_low_conf = num_low_conf + 1

			# LOGO
			logores = response["responses"][0]["logoAnnotations"]
			for logo in logores: 
				if logo["score"] > 0.9:
					returndict["LOGO_DETECTION"]["high"].append(logo["description"])
					num_high_conf = num_high_conf + 1
				elif logo["score"] > 0.8: 
					returndict["LOGO_DETECTION"]["mid"].append(logo["description"])
					num_mid_conf = num_mid_conf + 1
				elif logo["score"] > 0.7: 
					returndict["LOGO_DETECTION"]["low"].append(logo["description"])
					num_low_conf = num_low_conf + 1

		return returndict

	def speakanalysis(self, photoanalysisarray): 
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
		photoanalysis = photoanalysisarray[0]
		num_high_conf = photoanalysisarray[1]
		num_mid_conf = photoanalysisarray[2]
		num_low_conf = photoanalysisarray[3]


		sentence = ""


		highconflabels = photoanalysis["LABEL_DETECTION"]["high"]
		midconflabels = photoanalysis["LABEL_DETECTION"]["mid"]
		lowconflabels = photoanalysis["LABEL_DETECTION"]["low"]
		if highconflabels or midconflabels or lowconflabels: 
			sentence = "Looks like it "
			if highconflabels: 
				sentence = sentence + "is "
				first = True
				for label in highconflabels: 
					if label[-1] == "s": 
						sentence = sentence + "a "
					if first: 
						sentence = sentence + label + " "
					else: 
						sentence = sentence + "or "+ label + " "
				if midconflabels: 
					sentence = sentence + "with "
				elif lowconflabels: 
					sentence = sentence + "with maybe "
			if midconflabels: 
				if sentence[-5:-1] is not "with": 
					sentence = sentence + "could be "
				first = True
				for label in midconflabels: 
					if label[-1] == "s": 
						sentence = sentence + "a "
					if first: 
						sentence = sentence + label + " "
					else: 
						sentence = sentence + "or "+ label + " "
				if lowconflabels: 
					sentence = sentence + "with maybe "
			if lowconflabels: 
				if sentence[-12:-1] is not "with maybe ": 
					sentence = sentence + "might be "
				first = True
				for label in lowconflabels: 
					if label[-1] == "s": 
						sentence = sentence + "a "
					if first: 
						sentence = sentence + label + " "
					else: 
						sentence = sentence + "or "+ label + " "
			sentence = sentence + ". "

		text = photoanalysis["TEXT_DETECTION"]
		if text[0]: 
			sentence = sentence + "It has text saying "
			first = True
			for t in text: 
				if first: 
					sentence = sentence + t
				else: 
					sentence = sentence + "and " + t

		if len(photoanalysis["FACE_DETECTION"]) > 0: 
			if len(photoanalysis["FACE_DETECTION"]) > 1: 
				sentence = sentence + "There are " + len(photoanalysis["FACE_DETECTION"]) + " faces showing "
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
			sentence = sentence + ". "

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


