

import json

def SCAN_CLIQUE (GROUP):
	import click
	@GROUP.group ("SCAN")
	def GROUP ():
		pass
		
	'''
		BRUNCH SCAN BYTES --drive-path /dev/sdb --indexes '[ 0, 99 ]' --bytes-per-plate 512
	'''
	import click
	@GROUP.command ("BYTES")
	@click.option ('--drive-path', required = True, help = '')
	@click.option ('--indexes', required = True, help = '')
	@click.option ('--bytes-per-plate', default = 512, help = '')
	def EXAMPLE (drive_path, indexes, bytes_per_plate):	
		print ("INDEXES", indexes)
		INDEXES = json.loads ('{ "INDEXES": ' + indexes + '}')["INDEXES"]
		
		START_INDEX = INDEXES [0]
		assert (type (START_INDEX) == int)
		
		END_INDEX = INDEXES [1]
		assert (type (END_INDEX) == int)
		
		DRIVE_PATH = drive_path
		
		BYTES_PER_PLATE = bytes_per_plate
		
		#BYTE_STRING = b''
		def PROGRESS (PARAMS):
			#nonlocal BYTE_STRING;
			#BYTE_STRING += PARAMS ['PLATE']
			
			INDEXES = PARAMS ["INDEXES"]
			
			print ()
			print ("INDEXES:", INDEXES[0], "TO", INDEXES[1])
			print (PARAMS ['PLATE'].hex ())
		
		import BRUNCH.SCAN as SCAN
		SCAN.START ({
			"DRIVE PATH": DRIVE_PATH, 
			
			"BYTES INDEXES": [ START_INDEX, END_INDEX ],		
			"BYTES PER PLATE": BYTES_PER_PLATE,
			
			"PROGRESS": PROGRESS
		})	
		
		
		return;

	return;
