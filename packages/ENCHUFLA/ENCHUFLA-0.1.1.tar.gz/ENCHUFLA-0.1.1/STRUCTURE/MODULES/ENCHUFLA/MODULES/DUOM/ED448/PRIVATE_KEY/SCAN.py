


'''
	from DUOM.ED448.PRIVATE_KEY.SCAN import SCAN_PRIVATE_KEY
	[ PRIVATE_KEY, PRIVATE_KEY_BYTES, PRIVATE_KEY_STRING ] = SCAN_PRIVATE_KEY (PATH)
'''

from Crypto.PublicKey 		import ECC

from fractions import Fraction

def SCAN_PRIVATE_KEY (PATH):
	with open (PATH, mode = 'rb') as file:
		BYTES = file.read ()
		
		PRIVATE_KEY			= ECC.import_key (
			BYTES,
			curve_name		= "Ed448"
		)
		
		STRING = BYTES.hex ()

		return [ PRIVATE_KEY, BYTES, STRING ];

