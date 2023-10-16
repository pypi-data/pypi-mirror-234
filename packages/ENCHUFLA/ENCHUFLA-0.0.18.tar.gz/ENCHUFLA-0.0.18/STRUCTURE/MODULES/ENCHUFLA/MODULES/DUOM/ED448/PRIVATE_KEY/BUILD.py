

'''
	NEW VERSION -> "CREATE"
'''

'''
	from DUOM.ED448.PRIVATE_KEY.BUILD import BUILD_PRIVATE_KEY
	[ PRIVATE_KEY, PRIVATE_KEY_EXPORT ] = BUILD_PRIVATE_KEY (SEED, FORMAT)
'''

'''
	SEED:
		4986888b11358bf3d541b41eea5daece1c6eff64130a45fc8b9ca48f3e0e02463c99c5aedc8a847686d669b7d547c18fe448fc5111ca88f4e8
		5986888b11358bf3d541b41eea5daece1c6eff64130a45fc8b9ca48f3e0e02463c99c5aedc8a847686d669b7d547c18fe448fc5111ca88f4e8
		
		4986888B11358BF3D541B41EEA5DAECE1C6EFF64130A45FC8B9CA48F3E0E02463C99C5AEDC8A847686D669B7D547C18FE448FC5111CA88F4E8
		
	FORMAT:
		DER
		PEM
'''
from Crypto.PublicKey.ECC 	import EccKey

def WRITE (PATH, PRIVATE_KEY_STRING):
	import os.path
	if (os.path.exists (PATH)):
		print ("PUBLIC KEY ALREADY EXISTS, EXITING.");
		exit ()
		return False;
	
	f = open (PATH, 'wb')
	# f = open (PATH, 'wt')
	f.write (PRIVATE_KEY_STRING)
	f.close ()
	
	return True;


def BUILD_PRIVATE_KEY (
	SEED, 
	FORMAT, 
	
	PATH = ""
):	
	try:
		assert (len (SEED) == 114)
	except Exception:
		#
		#	WORD LIST: https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki
		#
		#		EACH WORD IS:
		#			2 ** 11 = 2048 BITS
		#
		#			11 BOOLEAN UNITS
		#
	
		#
		#	SEED BOOLEAN UNITS:
		#		57 BYTES = (2 ** 8) * 57
		#
		#		8 * 57 = 456
		#
		
		#
		#	11 BOOLEAN UNIT WORDS NECESSARY:
		#
		#		456 / 11 -> 41.45 -> 42 WORDS
		#
	
		#
		#	1 BYTE = 2 ** 8 = 256 BITS
		#
		#	2 BYTES = 
		#
		print ("Seed must be 57 bytes")
		exit (9)

	SEED_BYTES = bytes.fromhex (SEED)
	PRIVATE_KEY			= EccKey (
		curve 			= "Ed448", 
		seed 			= SEED_BYTES
	)
	PRIVATE_KEY_STRING 	= PRIVATE_KEY.export_key (format = FORMAT)
	#print ("PRIVATE STRING:", PRIVATE_KEY_STRING)
	
	if (len (PATH) >= 1):
		WRITE (PATH, PRIVATE_KEY_STRING)

	#print (PRIVATE_KEY, PRIVATE_KEY_STRING)
	
	return [ PRIVATE_KEY, PRIVATE_KEY_STRING ] 