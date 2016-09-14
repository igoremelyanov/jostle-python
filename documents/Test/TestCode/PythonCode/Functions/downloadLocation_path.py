
import os
from pathToPythonCode import pathToPythonCode


def downloadLocation_path():
	path = pathToPythonCode()
	downloadPath = path+"testDownloadFiles"
	return downloadPath

if __name__ == "__main__":
	path = downloadLocation_path()
	print path
