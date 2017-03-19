# Pi Dependencies 
import picamera
import json

# Google Dependencies 
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

# Image Dependencies 
import base64

def takephoto():
    camera = picamera.PiCamera()
    camera.capture('image.jpg')

def analyzephoto(): 
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

	credentials = GoogleCredentials.get_application_default()
	service = discovery.build('vision', 'v1', credentials=credentials)

	with open('image.jpg', 'rb') as image:
	image_content = base64.b64encode(image.read())
	service_request = service.images().annotate(body={
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

	print()
	num_high_conf = 0 
	num_mid_conf = 0
	num_low_conf = 0

	# FACES
	faceres = response["responses"][0]["faceAnnotations"][0]
	emotions = ["joyLikelihood", "sorrowLikelihood", "angerLikelihood", "surpriseLikelihood"]
	for emo in emotions: 
		if faceres[emo] > 0.9: 
			returndict["FACE_DETECTION"]["high"].append(emo)
			num_high_conf++
		if else faceres[emo] > 0.8: 
			returndict["FACE_DETECTION"]["mid"].append(emo)
			num_mid_conf++
		if else faceres[emo] > 0.7: 
			returndict["FACE_DETECTION"]["low"].append(emo)
			num_low_conf++

	# LABELS 
	labelres = response["responses"][0]["labelAnnotations"]
	for label in labelres: 
		if label["score"] > 0.9: 
			returndict["LABEL_DETECTION"]["high"].append(label["description"])
			num_high_conf++
		if else label["score"] > 0.8: 
			returndict["LABEL_DETECTION"]["mid"].append(label["description"])
			num_mid_conf++
		if else label["score"] > 0.7: 
			returndict["LABEL_DETECTION"]["low"].append(label["description"])
			num_low_conf++

	# TEXT 
	textres = response["responses"][0]["textAnnotations"]
	words = set() 
	for text in textres: 
		if text["locale"]: 
			returndict["TEXT_DETECTION"].append(text)

	# LANDMARK 
	landres = response["responses"][0]["landmarkAnnotations"]
	for landmark in landres: 
		if landmark["score"] > 0.9
			returndict["LANDMARK_DETECTION"]["high"].append(landmark["description"])
			num_high_conf++
		if else label["score"] > 0.8: 
			returndict["LANDMARK_DETECTION"]["mid"].append(landmark["description"])
			num_mid_conf++
		if else label["score"] > 0.7: 
			returndict["LANDMARK_DETECTION"]["low"].append(landmark["description"])
			num_low_conf++

	# LOGO
	logores = response["responses"][0]["logoAnnotations"]
	for logo in logores: 
		if logo["score"] > 0.9
			returndict["LOGO_DETECTION"]["high"].append(logo["description"])
			num_high_conf++
		if else label["score"] > 0.8: 
			returndict["LOGO_DETECTION"]["mid"].append(logo["description"])
			num_mid_conf++
		if else label["score"] > 0.7: 
			returndict["LOGO_DETECTION"]["low"].append(logo["description"])
			num_low_conf++

	return [returndict, num_high_conf, num_mid_conf, num_low_conf]

def speakanalysis(photoanalysisarray): 
	'''
	photoanalysis = {"FACE_DETECTION": {"low": [], "mid": [], "high": []}, 
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
		text: "the text " + text
	'''
	photoanalysis = photoanalysisarray[0]
	num_high_conf = photoanalysisarray[1]
	num_mid_conf = photoanalysisarray[2]
	num_low_conf = photoanalysisarray[3]


	highconfface = photoanalysis["FACE_DETECTION"]["high"]
	midconfface = photoanalysis["FACE_DETECTION"]["mid"]
	lowconfface = photoanalysis["FACE_DETECTION"]["low"]

	highconflabels = photoanalysis["LABEL_DETECTION"]["high"]
	midconflabels = photoanalysis["LABEL_DETECTION"]["mid"]
	lowconflabels = photoanalysis["LABEL_DETECTION"]["low"]

	highconflandmark = photoanalysis["LANDMARK_DETECTION"]["high"]
	midconflandmark = photoanalysis["LANDMARK_DETECTION"]["mid"]
	lowconflandmark = photoanalysis["LANDMARK_DETECTION"]["low"]

	highconflogo = photoanalysis["LOGO_DETECTION"]["high"]
	midconflogo = photoanalysis["LOGO_DETECTION"]["mid"]
	lowconflogo = photoanalysis["LOGO_DETECTION"]["low"]

	text = photoanalysis["TEXT_DETECTION"]


	sentence = "I think it's "

	if num_high_conf > 6

	if highconfface or midconfface or lowconfface: 
		if highconfface > 0: 




def main(): 
	# TAKE PHOTO
	takephoto()

	# MAKE DICTIONARY | ANALYZE PHOTOS
	photoanalysis = analyzephoto()

	# CREATE OUTPUT 
	speakanalysis(photoanalysis)

	# SAVE PHOTO AND DATA
	# storedetection()

