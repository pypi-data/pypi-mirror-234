
from BOTANIST.PROCESSES.START_MULTIPLE import START_MULTIPLE

def START ():
	
	
	PROCS = START_MULTIPLE (
		PROCESSES = [
			{ 
				"STRING": 'python3 -m http.server 9000',
				"CWD": None
			}
		],
		WAIT = True
	)
	
	
	return;
	
	EXIT 			= PROCS ["EXIT"]
	PROCESSES 		= PROCS ["PROCESSES"]

	time.sleep (.5)
	
	EXIT ()