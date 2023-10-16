


'''
	from DUOM.ED448.VERIFY import VERIFY
	VERIFY (
		PUBLIC_KEY, 
		UNSIGNED_BYTES, 
		SIGNED_BYTES
	)
'''

from Crypto.Signature 	import eddsa

def VERIFY (
	PUBLIC_KEY, 
	UNSIGNED_BYTES, 
	SIGNED_BYTES
):
	# PUBLIC_KEY = ECC.import_key (PUBLIC_KEY_STRING)
	VERIFIER = eddsa.new (PUBLIC_KEY, 'rfc8032')
	
	try:
		VERIFIER.verify (UNSIGNED_BYTES, SIGNED_BYTES)
		print ("VERIFICATION SUCCESSFUL")
		
		return True;
		
	except ValueError:
		print ("VERIFICATION FAILED")
		
	return False;