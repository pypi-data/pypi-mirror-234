

'''
	from DUOM.ED448.PRIVATE_KEY.CREATE import CREATE_PRIVATE_KEY
	PRIVATE_KEY = CREATE_PRIVATE_KEY (SEED, FORMAT)
	if (PRIVATE_KEY ["GOOD"]):
		#	PRIVATE_KEY ["CLASS"]
		#	PRIVATE_KEY ["STRING"]
		
	
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
import os.path

def WRITE (PATH, PRIVATE_KEY_STRING):
	if (os.path.exists (PATH)):
		return [ False, "PUBLIC KEY ALREADY EXISTS." ];
	
	f = open (PATH, 'wb')
	f.write (PRIVATE_KEY_STRING)
	f.close ()
	
	return [ True, "" ];


def CREATE_PRIVATE_KEY (
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
		#			11 BOOLEAN UNITS
		#
	
		#
		#	SEED BOOLEAN UNITS:
		#		57 BYTES = (2 ** 8) * 57
		#		8 * 57 = 456
		#
		
		#
		#	11 BOOLEAN UNIT WORDS NECESSARY:
		#		456 / 11 -> 41.45 -> 42 WORDS
		#
	
		#
		#	1 BYTE = 2 ** 8 = 256 BITS
		#	2 BYTES = 
		#
		print ("Seed must be 57 bytes")
		return {
			"GOOD": False,
			"ALARM": "Seed must be 57 bytes" 
		}

	SEED_BYTES = bytes.fromhex (SEED)
	PRIVATE_KEY	= EccKey (
		curve 	= "Ed448", 
		seed 	= SEED_BYTES
	)
	PRIVATE_KEY_STRING 	= PRIVATE_KEY.export_key (format = FORMAT)	
	if (len (PATH) >= 1):
		[ WRITTEN, NOTE ] = WRITE (PATH, PRIVATE_KEY_STRING)
		if (WRITTEN == False):
			return {
				"GOOD": False,
				"ALARM": NOTE 
			}
	
	return {
		"GOOD": True,
		
		"CLASS": PRIVATE_KEY, 
		"STRING": PRIVATE_KEY_STRING
	}