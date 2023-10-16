





'''
	from UTF8.SCAN import SCAN_UTF8_NOTE
	[ UTF8_STRING, BYTES, HEXADECAGON_STRING ] = SCAN_UTF8_NOTE (PATH)
'''

from Crypto.PublicKey 		import ECC

from fractions import Fraction

def SCAN_UTF8_NOTE (PATH):
	with open (PATH, mode = 'rb') as NOTE:
		BYTES = NOTE.read ()		
		HEXADECAGON_STRING = BYTES.hex ()
		UTF8_STRING = BYTES.decode ('utf8')

		return [ UTF8_STRING, BYTES, HEXADECAGON_STRING ];

