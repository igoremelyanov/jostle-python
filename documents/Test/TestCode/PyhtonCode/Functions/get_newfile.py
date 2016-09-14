#function that goe to a certain directory and tells you what the most recently created file is

import os,time

def get_newfile(folder,startTime):
	"""this function receives as its input a path to a folder of interest
	it then searches the folder for the most recently CREATED file and returns to the user the complete
		path of the file ex: "dir1/dir2/dir3/file_newest.log" where file_newest.log is the most recently
		file in dir3
	"""
	inProgress = True
	global most_recent
	while inProgress:
		files = os.listdir(folder)
		stamp = []
		for entry in files:
			stamp.append(os.path.getctime(folder+os.sep+entry))
		full = sorted(zip(stamp,files)) # sorted in ascending order so most recent is last
		most_recent = folder+os.sep+full[-1][-1]
		if(startTime < os.path.getctime(most_recent) and ".part" not in most_recent):
			lastModTime = os.path.getmtime(most_recent)
			inProgress = False
	# Check if file was updated every 500 ms, if not it means download is done.
	while (lastModTime == os.path.getmtime(most_recent) and os.stat(most_recent).st_size > 0) == False:
		time.sleep(0.5)
		lastModTime = os.path.getmtime(most_recent)

	return most_recent

if __name__ == "__main__":
	folder = os.path.join(os.path.dirname(__file__), '../testDownloadFiles/') 
	# folder = "P:\\s\\documents\\Test\\TestCode\\PythonCode\\testDownloadFiles"
	newest=get_newfile(folder,time.time())
	print newest
