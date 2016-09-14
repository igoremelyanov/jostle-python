import os

from pathToPythonCode import pathToPythonCode


def build_path_admin2_patch(buildNo):

	path = pathToPythonCode()
	buildPath_patch = path+"logFiles"+os.sep+"adminPages2_patch"+os.sep+"buildData"+os.sep+buildNo+os.sep
	if not os.path.exists(buildPath_patch):
		os.makedirs(buildPath_patch)
	return buildPath_patch

if __name__ == "__main__":
	path = build_path_admin2_patch("17345")
	print path


