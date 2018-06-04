import os

'''
open_File requires two parameters
	-fileName for target file name
	-mode for reading or writing[read, write]

open_File returns a dictionary of values
	-"FileExist" for whether the target file exists[True, False]
	-"File" for the file object
	-"Mode" for the mode of the file object["read", "write"]
'''

def open_File(fileName, mode):
	if os.path.isfile(fileName)==False:
		file=open(fileName, "w")
		return {"FileExist":False, "File":file, "Mode":"write"}
	elif mode=="write":
		file=open(fileName, "w")
		return {"FileExist":True, "File":file, "Mode":"write"}
	elif mode=="read":
		file=open(fileName, "r")
		return {"FileExist":True, "File":file, "Mode":"read"}
	print(os.path.isfile(fileName))