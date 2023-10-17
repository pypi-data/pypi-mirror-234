


'''
PACT DUOM ED448 VERIFY \
--public-key-path "ED448_PUBLIC_KEY.DER" \
--unsigned-utf8-path "UNSIGNED_MESSAGE.UTF8" \
--signed-bytes-path "SIGNED_MESSAGE.BYTES"
'''
def VERIFY (GROUP):
	import click
	@click.option ('--public-key-path', default = '', help = '')
	@click.option ('--unsigned-utf8-path', default = '', help = '')
	@click.option ('--signed-bytes-path', default = '', help = '')
	@GROUP.command ("VERIFY")
	def VERIFY (
		public_key_path, 
		unsigned_utf8_path,
		signed_bytes_path
	):	
		from DUOM.ED448.PUBLIC_KEY.SCAN import SCAN_PUBLIC_KEY
		[ PUBLIC_KEY, PUBLIC_KEY_BYTES, PUBLIC_KEY_STRING ] = SCAN_PUBLIC_KEY (public_key_path)

		from UTF8.SCAN import SCAN_UTF8_NOTE
		UNSIGNED_BYTES = SCAN_UTF8_NOTE (unsigned_utf8_path) [1]

		print ("?????????????????")

		from BYTES.SCAN import SCAN_BYTES
		SIGNED_BYTES = SCAN_BYTES (signed_bytes_path) [0]

		from DUOM.ED448.VERIFY import VERIFY
		VERIFIED = VERIFY (
			PUBLIC_KEY, 
			UNSIGNED_BYTES, 
			SIGNED_BYTES
		)

		if (VERIFIED):
			exit (0)
			
		exit (99)
		

		return;	

