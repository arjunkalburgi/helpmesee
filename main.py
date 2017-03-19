

def main(cameraBot, captionBot, visionBot, watsonBot, storeBot): 
	file = "image.jpg"

	# TAKE THE PHOTO
	cameraBot.takephoto(file)
	cameraBot.closecam()

	# ANALYZE THE PHOTO
	caption = captionBot.file_caption(file)
	vision = visionBot.file_caption(file)
	watson = watsonBot.see_anyone(file)

	print(caption)
	print(vision)
	print(watson)

	# SPEAK TO THE USER 

	# STORE THE QUERY + INFO
	path = storeBot.movefile(file)
	storeBot.log(path, caption, vision, watson)
	

if __name__ == '__main__':
	main()
