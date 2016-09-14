import os

from pathToPythonCode import pathToPythonCode


def build_path_admin2_ap(buildNo):

	path = pathToPythonCode()
	buildPath_AP = path+"logFiles"+os.sep+"adminPages2_ap"+os.sep+"buildData"+os.sep+buildNo+os.sep
	if not os.path.exists(buildPath_AP):
		os.makedirs(buildPath_AP)
	return buildPath_AP

if __name__ == "__main__":
	path = build_path_admin2_ap("17345")
	print path


