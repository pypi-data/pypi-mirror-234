



from .SCULPT 	import SCULPT_OPTIONS
from .SCAN 		import SCAN_CLIQUE
from .ERASE 	import ERASE_OPTIONS


def START ():

	import click
	@click.group ()
	def GROUP ():
		pass

	
	'''
	import click
	@click.command ("example")
	def EXAMPLE ():	
		print ("EXAMPLE")

		return;
	GROUP.add_command (EXAMPLE)
	'''

	SCULPT_OPTIONS (GROUP)
	SCAN_CLIQUE (GROUP)
	ERASE_OPTIONS (GROUP)

	GROUP ()
