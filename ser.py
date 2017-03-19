import serial
import main
#import os

#os.system("sudo su")
#os.system("export GOOGLE_APPLICATION_CREDENTIALS=apiKey.json")

def ser()
	ser = serial.Serial('/dev/ttyACM0',9600)
	s = [0,1]
	while True:
		read_serial=ser.readline()


		print read_serial
		if read_serial!="":
			print "TAKE PICTURE"
			#PUT func here test1.main()
			main.main()

		
