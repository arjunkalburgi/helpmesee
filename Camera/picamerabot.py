import picamera

class CameraBot: 
	def __init__(self): 
		self.camera = picamera.PiCamera()

	def takephoto(self, file):
		self.camera.rotation = 270
		self.camera.capture('image.jpg')

	def closecam(self): 
		self.camera.close()

		