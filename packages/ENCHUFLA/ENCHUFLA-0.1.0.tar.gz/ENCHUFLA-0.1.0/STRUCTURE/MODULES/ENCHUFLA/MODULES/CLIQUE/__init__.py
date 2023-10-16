



from .ACADEMY	import ACADEMY
from .DUOM 		import DUOM
from .KEG 		import KEG


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

	ACADEMY (GROUP)
	DUOM (GROUP)
	KEG (GROUP)
	
	#BYTES (GROUP)

	GROUP ()




#
