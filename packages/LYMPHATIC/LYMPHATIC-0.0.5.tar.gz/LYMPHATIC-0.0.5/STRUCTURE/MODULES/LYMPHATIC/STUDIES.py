
from BOTANIST.PROCESSES.START_MULTIPLE import START_MULTIPLE

def OPEN ():	
	import pathlib
	from os.path import dirname, join, normpath
	import sys
	
	THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()	
	# normpath (join (THIS_FOLDER, PATH))

	PROCS = START_MULTIPLE (
		PROCESSES = [
			{ 
				"STRING": 'python3 -m http.server 47382',
				"CWD": THIS_FOLDER
			}
		],
		WAIT = True
	)
	
	'''
	EXIT 			= PROCS ["EXIT"]
	PROCESSES 		= PROCS ["PROCESSES"]

	time.sleep (.5)
	
	EXIT ()
	'''
	
	


