import os

print(1)
os.system("sudo su")
print(2)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "apiKey.json"
print(3)

import ser
ser()
print(4)
