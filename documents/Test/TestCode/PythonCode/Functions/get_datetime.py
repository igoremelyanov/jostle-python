# function to get the date and time and print it out in the proper format

from datetime import datetime

def get_datetime():
	"""this function gets the current date and time in the preferred
			format, 2013.05.28___time___"
			it returns the complete date and time as well as just the date.
			this is helpful for doing the filename stuff we want
	"""
	now = datetime.now()
	now = str(now)
	full = now.replace(":",".").replace("-",".").replace(" ","_") # getting preferred 2013.05.28 formatting
	date = full.split("_")[0]
	return full, date


if __name__ == "__main__":
	now = get_datetime()
	print now
