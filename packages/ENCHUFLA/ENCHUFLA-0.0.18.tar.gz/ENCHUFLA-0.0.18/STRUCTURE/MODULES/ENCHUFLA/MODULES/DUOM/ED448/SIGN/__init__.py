

'''
	from DUOM.ED448.SIGN import SIGN_MESSAGE
'''

from Crypto.PublicKey 	import ECC
from Crypto.Signature 	import eddsa

def WRITE (PATH, SIGNED_MESSAGE):
	import os.path
	if (os.path.exists (PATH)):
		print ("PATH FOR SIGNED MESSAGE ISN'T EMPTY, EXITING.");
		exit ()
		return False;
	
	f = open (PATH, 'wb')
	f.write (SIGNED_MESSAGE)
	f.close ()


def SIGN (
	PRIVATE_KEY,
	UNSIGNED_BYTES,
	
	PATH = ""
):
	SIGNER 				= eddsa.new (PRIVATE_KEY, 'rfc8032')
	SIGNED_MESSAGE 		= SIGNER.sign (UNSIGNED_BYTES)
	
	if (len (PATH) >= 1):
		WRITE (PATH, SIGNED_MESSAGE)
	
	return [ SIGNED_MESSAGE ]