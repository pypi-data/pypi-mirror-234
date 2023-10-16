
'''
	from DUOM.ED448.PRIVATE_KEY.READ import READ_PRIVATE_KEY
	READ_PRIVATE_KEY ()
'''

from fractions import Fraction

def READ_PRIVATE_KEY (PATH, FORMAT = "BYTES"):
	with open (PATH, mode = 'rb') as file:
		BYTES = file.read ()

		if (FORMAT == "BYTES"):
			return BYTES;
		
		STRING = BYTES.hex ()
		return STRING;