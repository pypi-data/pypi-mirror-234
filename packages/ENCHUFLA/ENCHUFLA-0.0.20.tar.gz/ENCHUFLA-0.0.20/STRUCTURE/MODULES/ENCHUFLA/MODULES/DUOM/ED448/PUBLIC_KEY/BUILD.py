

'''
	from DUOM.ED448.PUBLIC_KEY.BUILD import BUILD_PUBLIC_KEY
	[ PUBLIC_KEY, PUBLIC_KEY_EXPORT ] = BUILD_PUBLIC_KEY (
		PRIVATE_KEY_PATH,
		PUBLIC_KEY_PATH
	)
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
		print ("PUBLIC KEY ALREADY EXISTS, EXITING.");
		exit ()
		return False;
	
	f = open (PATH, 'wb')
	f.write (STRING)
	f.close ()
	
	return True;



def BUILD_PUBLIC_KEY (
	PRIVATE_KEY_PATH = "",
	PUBLIC_KEY_PATH = "",
	FORMAT = "DER"
):	
	#
	#	https://pycryptodome.readthedocs.io/en/latest/src/public_key/ecc.html#Crypto.PublicKey.ECC.import_key
	#
	from DUOM.ED448.PRIVATE_KEY.READ import READ_PRIVATE_KEY
	PRIVATE_KEY_BYTES = READ_PRIVATE_KEY (PRIVATE_KEY_PATH)

	print ("PRIVATE_KEY_BYTES:", PRIVATE_KEY_BYTES)
	print ("PRIVATE_KEY_BYTES LEN:", len (PRIVATE_KEY_BYTES))

	PRIVATE_KEY			= ECC.import_key (
		PRIVATE_KEY_BYTES,
		curve_name		= "Ed448"
	)

	PUBLIC_KEY			= PRIVATE_KEY.public_key ()
	PUBLIC_KEY_STRING	= PUBLIC_KEY.export_key (format = FORMAT)
	
	if (len (PUBLIC_KEY_PATH) >= 1):
		WRITE (PUBLIC_KEY_PATH, PUBLIC_KEY_STRING)

	return [ 
		PUBLIC_KEY, 
		PUBLIC_KEY_STRING 
	] 