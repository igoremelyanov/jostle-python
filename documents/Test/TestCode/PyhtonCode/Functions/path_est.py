# function to check if a given folder exists and if it doesnt to make it

import os
from pathToPythonCode import pathToPythonCode

def path_est(date):
	""" this file accepts as its input the name of folder that has the form year.month.day
		it looks for this folder in the logFiles folder and if it isnt there it makes it
	"""
	path = pathToPythonCode()
	log_path = path+"logFiles"+os.sep+date+os.sep
	#log_path = "P:\\s\documents\\Test\\TestCode\\PythonCode\\logFiles\\"+date+"\\"
	if not os.path.exists(log_path):
		os.makedirs(log_path)
	shot_path = path+"screenShots"+os.sep+date+os.sep
#	shot_path = "P:\\s\documents\\Test\\TestCode\\PythonCode\\screenShots\\"+date+"\\"
	if not os.path.exists(shot_path):
		os.makedirs(shot_path)
	return log_path,shot_path

if __name__ == "__main__":
		log, shot = path_est("2014.02.04")
		print log
		print shot
