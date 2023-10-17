

def ED448 (GROUP):
	import click
	@GROUP.group ("ED448")
	def GROUP ():
		pass
	
	from .BUILD_PRIVATE_KEY import BUILD_PRIVATE_KEY
	BUILD_PRIVATE_KEY (GROUP)
	
	from .BUILD_PUBLIC_KEY import BUILD_PUBLIC_KEY
	BUILD_PUBLIC_KEY (GROUP)
	
	from .SIGN import SIGN
	SIGN (GROUP)
	
	from .VERIFY import VERIFY
	VERIFY (GROUP)

	return;