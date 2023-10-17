

'''
PACT DUOM ED448 SIGN \
--private-key-path "ED448_PRIVATE_KEY.DER" \
--message "12341234"
'''

'''
PACT DUOM ED448 SIGN \
--private-key-path "ED448_PRIVATE_KEY.DER" \
--unsigned-utf8-path "UNSIGNED_MESSAGE.UTF8" \
--signed-bytes-path "SIGNED_MESSAGE.BYTES"
'''
def SIGN (GROUP):
	import click
	@click.option ('--private-key-path', default = '', help = '')
	@click.option ('--note', default = '', help = '')
	@click.option ('--unsigned-utf8-path', default = '', help = '')
	@click.option ('--signed-bytes-path', default = '', help = '')
	@GROUP.command ("SIGN")
	def SIGN (
		private_key_path, 
		note,
		unsigned_utf8_path,
		signed_bytes_path
	):	
		from DUOM.ED448.PRIVATE_KEY.SCAN import SCAN_PRIVATE_KEY
		[ PRIVATE_KEY, PRIVATE_KEY_BYTES, PRIVATE_KEY_STRING ] = SCAN_PRIVATE_KEY (private_key_path)
	
		#
		#	https://docs.python.org/3/library/stdtypes.html#str.encode
		#
		if (len (unsigned_utf8_path) >= 1):
			from UTF8.SCAN import SCAN_UTF8_NOTE
			[ UTF8_STRING, UNSIGNED_BYTES, HEX_STRING ] = SCAN_UTF8_NOTE (unsigned_utf8_path)
		else:
			UTF8_STRING = note.encode ('utf8')
	
		PATH = signed_bytes_path
		
		from DUOM.ED448.SIGN import SIGN
		[ SIGNED_MESSAGE ] = SIGN (
			PRIVATE_KEY,
			UNSIGNED_BYTES = UNSIGNED_BYTES,
			
			PATH = PATH
		)

		print ("SIGNED MESSAGE:", SIGNED_MESSAGE)
		print ("SIGNED MESSAGE HEX STRING:", SIGNED_MESSAGE.hex ())
		print ("SIGNED MESSAGE HEX STRING LENGTH:", len (SIGNED_MESSAGE.hex ()))

		

		return;