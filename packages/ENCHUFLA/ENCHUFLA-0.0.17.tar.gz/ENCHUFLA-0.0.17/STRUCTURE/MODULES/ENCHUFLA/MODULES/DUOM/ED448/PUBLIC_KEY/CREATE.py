

'''
	from DUOM.ED448.PUBLIC_KEY.CREATE import CREATE_PUBLIC_KEY
	PUBLIC_KEY = CREATE_PUBLIC_KEY ({
		"PRIVATE KEY PATH": "",
		"PUBLIC KEY PATH": "",
		"PUBLIC KEY FORMAT": "DER"
	})
'''

'''
	FORMAT:
		DER
		PEM
'''
from Crypto.PublicKey.ECC 	import EccKey
from Crypto.PublicKey 		import ECC

def WRITE (PATH, STRING):
	import os.path
	if (os.path.exists (PATH)):
		return [ False, "PUBLIC KEY ALREADY EXISTS AT PATH." ];
	
	f = open (PATH, 'wb')
	f.write (STRING)
	f.close ()
	
	return [ True, "" ];

#
#	S & V = { SIGNER, SIGNATORY } & { APPROVER, RATIFIER, VERIFIER }
#
#	SIGNER & VALIDATOR
#
SEED = {
	"PRIVATE KEY PATH": "",
	"PUBLIC KEY PATH": "",
	"PUBLIC KEY FORMAT": "DER"
}

def CREATE_PUBLIC_KEY (SELECTS):
	OPTIONS = {
		** SEED,
		** SELECTS
	}
	
	print ("OPTIONS:", OPTIONS)
	
	PRIVATE_KEY_PATH = OPTIONS ["PRIVATE KEY PATH"]
	PUBLIC_KEY_PATH = OPTIONS ["PUBLIC KEY PATH"]
	PUBLIC_KEY_FORMAT = OPTIONS ["PUBLIC KEY FORMAT"]

	#
	#	https://pycryptodome.readthedocs.io/en/latest/src/public_key/ecc.html#Crypto.PublicKey.ECC.import_key
	#
	from DUOM.ED448.PRIVATE_KEY.READ import READ_PRIVATE_KEY
	PRIVATE_KEY_BYTES = READ_PRIVATE_KEY (PRIVATE_KEY_PATH)
	PRIVATE_KEY			= ECC.import_key (
		PRIVATE_KEY_BYTES,
		curve_name		= "Ed448"
	)

	PUBLIC_KEY			= PRIVATE_KEY.public_key ()
	PUBLIC_KEY_STRING	= PUBLIC_KEY.export_key (format = PUBLIC_KEY_FORMAT)
	
	if (len (PUBLIC_KEY_PATH) >= 1):
		[ WRITTEN, NOTE ] = WRITE (PUBLIC_KEY_PATH, PUBLIC_KEY_STRING)
		if (WRITTEN == False):
			return {
				"GOOD": False,
				"ALARM": NOTE 
			}
			
	return {
		"GOOD": True,
		
		"CLASS": PUBLIC_KEY, 
		"STRING": PUBLIC_KEY_STRING
	}
