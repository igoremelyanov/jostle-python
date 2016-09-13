import os

from pathToPythonCode import pathToPythonCode


def build_path_admin2_usqa(buildNo):

	path = pathToPythonCode()
	buildPath_USQA = path+"logFiles"+os.sep+"adminPages2_usqa"+os.sep+"buildData"+os.sep+buildNo+os.sep
	if not os.path.exists(buildPath_USQA):
		os.makedirs(buildPath_USQA)
	return buildPath_USQA

if __name__ == "__main__":
	path = build_path_admin2_usqa("17345")
	print path


