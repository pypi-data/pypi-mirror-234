



from .KEG 		import KEG
from .DUOM 		import DUOM
#from .BYTES 	import BYTES


def START ():
	import click
	@click.group ()
	def GROUP ():
		pass


	import click
	@click.command ("example")
	def EXAMPLE ():	
		print ("EXAMPLE")

		return;
	GROUP.add_command (EXAMPLE)

	KEG (GROUP)
	DUOM (GROUP)
	#BYTES (GROUP)

	GROUP ()




#
