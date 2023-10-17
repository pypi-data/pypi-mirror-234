
from ACADEMY import START as START_ACADEMY

def ACADEMY (GROUP):
	import click
	@GROUP.group ("ACADEMY")
	def GROUP ():
		pass
		
	import click
	@GROUP.command ("START")
	def START ():	
		print ("START ACADEMY")

		START_ACADEMY ()


		return;
		

	return;