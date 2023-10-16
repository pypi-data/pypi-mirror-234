
'''
PACT DUOM ED448 BUILD-PUBLIC-KEY \
--private-key-path "ED448_PRIVATE_KEY.DER" \
--public-key-path "ED448_PUBLIC_KEY.DER"
'''
def BUILD_PUBLIC_KEY (GROUP):
	import click
	@GROUP.command ("BUILD-PUBLIC-KEY")
	@click.option ('--private-key-path', default = '', help = '')
	@click.option ('--public-key-path', default = '', help = '')
	def BUILD_PUBLIC_KEY (private_key_path, public_key_path):
		PRIVATE_KEY_PATH = private_key_path
		PUBLIC_KEY_PATH = public_key_path
	
		from DUOM.ED448.PUBLIC_KEY.BUILD import BUILD_PUBLIC_KEY
		[ PUBLIC_KEY, PUBLIC_KEY_EXPORT ] = BUILD_PUBLIC_KEY (
			PRIVATE_KEY_PATH,
			PUBLIC_KEY_PATH
		)

	return;