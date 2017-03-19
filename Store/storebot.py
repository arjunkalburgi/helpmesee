import os
import psycopg2

class CockroachBot: 
	def __init__(self): 
		self.counter = 0
		self.newfolder()
	
	def newfolder(self): 
		self.path = "0"
		i = 0
		while True: 
			if not os.path.exists("Store/Images/"+str(i)):
				os.makedirs("Store/Images/"+str(i))
				self.path = "Store/Images/"+str(i)
				return
			i = i + 1

	def movefile(self, originalfilepath): 
		os.system("cp " + originalfilepath + " " + self.path + "/image" + str(self.counter) + ".jpg")

	def log(self, f, c, v, w): 
		conn = psycopg2.connect(database='bank', user='maxroach', host='localhost', port=5433)
		conn.set_session(autocommit=True)
		cur = conn.cursor()
		# cur.execute("CREATE TABLE IF NOT EXISTS accounts (id INT PRIMARY KEY, balance INT)")
		# CREATE TABLE letmesee.img(path CHAR PRIMARY KEY, caption CHAR, vision CHAR, watson CHAR)
		cur.execute("INSERT INTO letmesee.img (path, caption, vision, watson) VALUES ('" + f + "', '" + c + "', '" + v + "', '" + w + "')")
