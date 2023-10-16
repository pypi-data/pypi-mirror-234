

from fractions import Fraction

def READ_BYTES (PATH):
	with open (PATH, mode = 'rb') as file:
		BYTES = file.read ()
		STRING = BYTES.hex ()
		
		print (BYTES)
		print (STRING)
		
		print (len (STRING))
		print ("BYTE COUNT = ", Fraction (len (STRING), 2))