
'''
	from BYTES.SCAN import SCAN_BYTES
	[ BYTES ] = SCAN_BYTES ()
'''

from fractions import Fraction

def SCAN_BYTES (PATH):
	with open (PATH, mode = 'rb') as NOTE:
		BYTES 	= NOTE.read ()
		STRING 	= BYTES.hex ()
		
		print (len (STRING))
		print ("BYTE COUNT = ", Fraction (len (STRING), 2))
		
		
		return [ BYTES ];