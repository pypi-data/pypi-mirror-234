

import json

def ERASE_OPTIONS (GROUP):
	import click
	@GROUP.group ("ERASE")
	def GROUP ():
		pass
		
	'''
		BRUNCH ERASE ENTIRELY --drive-path /dev/sde --last-byte-index 40018599423
		BRUNCH ERASE ENTIRELY --drive-path /dev/sde --last-byte-index 32010928127
	'''
	import click
	@GROUP.command ("ENTIRELY")
	@click.option ('--drive-path', required = True, help = '')
	@click.option ('--last-byte-index', required = True, help = '')
	@click.option ('--skip-over', default = 0, help = '')
	def ERASE_ENTIRELY (drive_path, last_byte_index, skip_over):	
		from BRUNCH.ERASE import ERASE
		from BRUNCH.SCULPT.ROUTINES.ROUTINE_1 import ROUTINE_1
		from BRUNCH.SCULPT.ROUTINES.ROUTINE_2 import ROUTINE_2
				
		ERASE ({
			"SKIP OVER": int (skip_over),
			
			"DRIVE PATH": drive_path,
			"LAST BYTE INDEX": int (last_byte_index),
			
			"SCULPT": {
				"ROUTINES": [{
					"BYTES PER PLATE": 512 * 512,
					"BYTES": ROUTINE_1 ()
				},{
					"BYTES PER PLATE": 512 * 512,
					"BYTES": ROUTINE_2 ()
				}]
			}
		})
		
		
		return;

	return;
