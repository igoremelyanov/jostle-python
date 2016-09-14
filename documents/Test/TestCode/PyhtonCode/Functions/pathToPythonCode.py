# will get the relative path to the PythonCode folder

import os

def pathToPythonCode():
	prog = os.path.abspath(__file__).split(os.sep)    #location of this program
	levels = prog.index("PythonCode")
	folders = prog[:levels+1]
	path = ''
	for entry in folders:
		path += entry+os.sep
	return path

if __name__ == '__main__':
	pathToPythonCode()
