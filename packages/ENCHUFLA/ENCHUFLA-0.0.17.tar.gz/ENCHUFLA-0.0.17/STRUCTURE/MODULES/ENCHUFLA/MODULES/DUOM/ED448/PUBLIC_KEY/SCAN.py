


'''
	from DUOM.ED448.PUBLIC_KEY.SCAN import SCAN_PUBLIC_KEY
	[ PUBLIC_KEY, PUBLIC_KEY_BYTES, PUBLIC_KEY_STRING ] = SCAN_PUBLIC_KEY (PATH)
'''


#
#	IMPORT A PUBLIC OR PRIVATE KEY:
#
#		https://pycryptodome.readthedocs.io/en/latest/src/public_key/ecc.html#Crypto.PublicKey.ECC.import_key
#

from Crypto.PublicKey 	import ECC

from fractions 			import Fraction

def SCAN_PUBLIC_KEY (PATH):
	with open (PATH, mode = 'rb') as file:
		PUBLIC_KEY_BYTES = file.read ()
		
		PUBLIC_KEY			= ECC.import_key (
			PUBLIC_KEY_BYTES,
			curve_name		= "Ed448"
		)
		
		PUBLIC_KEY_STRING = PUBLIC_KEY_BYTES.hex ()

		return [ 
			PUBLIC_KEY, 
			PUBLIC_KEY_BYTES, 
			PUBLIC_KEY_STRING 
		];

