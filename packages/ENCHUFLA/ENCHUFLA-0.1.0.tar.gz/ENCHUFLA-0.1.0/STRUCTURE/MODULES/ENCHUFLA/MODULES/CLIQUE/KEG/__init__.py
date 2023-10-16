

def KEG (GROUP):
	import click
	@GROUP.group ("KEG")
	def GROUP ():
		pass
		
	import click
	@GROUP.command ("TAP")
	@click.option ('--port', default = 1110, help = '')
	def EXAMPLE (port):	
		from KEG import TAP
		TAP (
			PORT = port
		)

		return;

	return;