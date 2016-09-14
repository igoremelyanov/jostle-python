#this is a function that i just supposed to simplify the console and log outputs
#all it does is hide the two statements(print and append) in a single function call
import os

def writer(string,output):
	"""this function prints a string as well as appends that string
	to a list to be printed to a file later
	"""
	path = prog = os.path.abspath(__file__).split(os.sep) 

	f = open(os.path.join(os.path.dirname(__file__), '../logFiles/logTextSuperDump.txt'),"a")
	f.write(string+"\n")
	f.close()
	print string
	output.append(string+"\n")
	return output

if __name__ == '__main__':
	output = []
	output = writer("testing",output)
	print output
	output = writer("verify",output)
	print output
