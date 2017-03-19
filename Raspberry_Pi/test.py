# FACES
def readFACES(returndict, response):
	num_high_conf = 0
	num_mid_conf = 0
	num_low_conf = 0
	faceres = response["responses"][0]["faceAnnotations"][0]
	emotions = ["joyLikelihood", "sorrowLikelihood", "angerLikelihood", "surpriseLikelihood"]
	for emo in emotions: 
		if faceres[emo] > 0.9: 
			returndict["FACE_DETECTION"]["high"].append(emo)
			num_high_conf = num_high_conf + 1
		elif faceres[emo] > 0.8: 
			returndict["FACE_DETECTION"]["mid"].append(emo)
			num_mid_conf = num_mid_conf + 1
		elif faceres[emo] > 0.7: 
			returndict["FACE_DETECTION"]["low"].append(emo)
			num_low_conf = num_low_conf + 1
	return returndict

# LABELS 
def readLABELS(returndict, response):
	num_high_conf = 0
	num_mid_conf = 0
	num_low_conf = 0
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
	return returndict

# TEXT 
def readTEXT(returndict, response):
	num_high_conf = 0
	num_mid_conf = 0
	num_low_conf = 0
	textres = response["responses"][0]["textAnnotations"]
	words = set() 
	for text in textres: 
		if text["locale"]: 
			returndict["TEXT_DETECTION"].append(text)
	return returndict

# LANDMARK 
def readLANDMARK(returndict, response):
	num_high_conf = 0
	num_mid_conf = 0
	num_low_conf = 0
	landres = response["responses"][0]["landmarkAnnotations"]
	for landmark in landres: 
		if landmark["score"] > 0.9:
			returndict["LANDMARK_DETECTION"]["high"].append(landmark["description"])
			num_high_conf = num_high_conf + 1
		elif label["score"] > 0.8: 
			returndict["LANDMARK_DETECTION"]["mid"].append(landmark["description"])
			num_mid_conf = num_mid_conf + 1
		elif label["score"] > 0.7: 
			returndict["LANDMARK_DETECTION"]["low"].append(landmark["description"])
			num_low_conf = num_low_conf + 1
	return returndict

# LOGO
def readLOGO(returndict, response):
	num_high_conf = 0
	num_mid_conf = 0
	num_low_conf = 0
	logores = response["responses"][0]["logoAnnotations"]
	for logo in logores: 
		if logo["score"] > 0.9:
			returndict["LOGO_DETECTION"]["high"].append(logo["description"])
			num_high_conf = num_high_conf + 1
		elif label["score"] > 0.8: 
			returndict["LOGO_DETECTION"]["mid"].append(logo["description"])
			num_mid_conf = num_mid_conf + 1
		elif label["score"] > 0.7: 
			returndict["LOGO_DETECTION"]["low"].append(logo["description"])
			num_low_conf = num_low_conf + 1
	return returndict