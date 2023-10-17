
'''
	VENTURES:
		
		from BRUNCH.ERASE import ERASE
		from BRUNCH.SCULPT.ROUTINES.ROUTINE_1 import ROUTINE_1
		from BRUNCH.SCULPT.ROUTINES.ROUTINE_2 import ROUTINE_2
		
		ERASE ({
			"SKIP OVER": 0,
			
			"DRIVE PATH": DRIVE_PATH,
			"LAST BYTE INDEX": LAST_BYTE_INDEX,
			
			"SCULPT": {
				"ROUTINES": [{
					"BYTES PER PLATE": 512 * 512,
					"BYTES": ROUTINE_1 ()
				},{
					"BYTES PER PLATE": 512 * 512,
					"BYTES": ROUTINE_2 ()
				}]
			},
			"SCAN": {
				"BYTES PER PLATE": 512 * 512
			}
		})
'''

import BRUNCH.SCAN as SCAN
import BRUNCH.SCAN.IS_LAST_BYTE as IS_LAST_BYTE

import BRUNCH.ERASE.FUNCTIONS.BYTE_STRING_EQ as BYTE_STRING_EQ

import BRUNCH.SCULPT as SCULPT

from fractions import Fraction

from time import sleep, perf_counter



def ERASE (CARGO):
	'''
		SKIP_OVER = 0	-> SKIPS NOTHING
		SKIP_OVER = 1 -> SKIPS FIRST SCULPT
		SKIP_OVER = 2 -> SKIPS TO SECOND LOOP
	'''	

	SKIP_OVER = CARGO ["SKIP OVER"]

	DRIVE_PATH = CARGO ["DRIVE PATH"]
	LAST_BYTE_INDEX = CARGO ["LAST BYTE INDEX"]
	SCULPT_ROUTINES = CARGO ["SCULPT"]["ROUTINES"]

	#
	#
	SCULPT_START = 0
	#
	#

	[ IS_LAST, NOTE ] = IS_LAST_BYTE.DEEM ({
		"drive path": DRIVE_PATH,
		"last byte index": LAST_BYTE_INDEX + 1
	})
	if (IS_LAST == False):
		print (NOTE)
	
	print ("LAST_BYTE_INDEX IS_LAST:", IS_LAST)
	


	SCULPT_LOOP = 1
	def SCULPT_PROGRESS (PARAMS):
		nonlocal SCULPT_LOOP;
		INDEXES = PARAMS ["INDEXES"]
		SIZE = PARAMS ["SIZE"]
		LAST_LOOP = PARAMS ["LAST_LOOP"]

		if (SCULPT_LOOP == 1000 or LAST_LOOP == True):
			PERCENT = 100 * Fraction (INDEXES [1] / LAST_BYTE_INDEX)			
			if (PERCENT.denominator == 1):
				PERCENT = str (int (PERCENT))
			else:
				PERCENT = str (float (PERCENT))
			
			
			#BYTE_INDEX = "[AT BYTE INDEX:" + str (INDEXES[0]) + "]"
			PLATE_SIZE = "[REACHED BYTE INDEX:" + str(INDEXES[0]) + "]"
			PERCENT_STRING = "[" + PERCENT + "%]"
			
			print (
				"SCULPTING:",
				PLATE_SIZE,
				PERCENT_STRING
			)
			
			SCULPT_LOOP = 1;
		
		SCULPT_LOOP += 1

	STAGE = 1;
	LOOP_COUNT = 1;
	for ROUTINE in SCULPT_ROUTINES:
		print (f"LOOP '{ LOOP_COUNT }' OF '{ len (SCULPT_ROUTINES) }'")
	
		BYTES_PER_PLATE = ROUTINE ["BYTES PER PLATE"]
		BYTES = ROUTINE ["BYTES"]
		
		#
		#	SKIP_OVER = 0, STAGE = 1	->	DON'T SKIP
		#	SKIP_OVER = 1, STAGE = 1	->	SKIP
		#	SKIP_OVER = 2, STAGE = 1	->  SKIP
		#
		#	SKIP_OVER = 2, STAGE = 3	-> 	DON'T SKIP
		#
		if (STAGE > SKIP_OVER):
			PLACE_1 = perf_counter ()

			SCULPT.START ({
				"DRIVE PATH": DRIVE_PATH,
				
				"BYTES INDEXES": [ 0, LAST_BYTE_INDEX ],			
				"BYTES FOR PLATE": BYTES,
				
				"PROGRESS": SCULPT_PROGRESS
			})
			
			ELAPSED = perf_counter () - PLACE_1
			
			print ("Sculpt required", ELAPSED, "seconds.")
			
		else:
			print ("SKIPPING SCULPT, STAGE = ", STAGE)
			
		STAGE += 1;
		
		if (STAGE > SKIP_OVER):
			
		
			SCAN_LOOP = 1
			def SCAN_PROGRESS (PARAMS):
				nonlocal SCAN_LOOP;
			
				PLATE = PARAMS ["PLATE"]
				SCAN_SIZE = PARAMS ["SCAN SIZE"]
				INDEXES = PARAMS ["INDEXES"]
				LAST_SCAN = PARAMS ["LAST SCAN"]
				
				# BYTE_STRING_EQ
				
				if (PLATE != BYTES [0:SCAN_SIZE]):
					BYTES_PARTIAL = BYTES [0:SCAN_SIZE]
				
					print ("PLATE LEN:", len (PLATE))
					print ("BYTES LEN:", len (BYTES_PARTIAL))
					
					if (len (PLATE) != len (BYTES_PARTIAL)):
						assert (len (PLATE) != len (BYTES_PARTIAL))
					
					
					INDEX = 0;
					LAST_INDEX = len (PLATE) - 1
					while (INDEX <= LAST_INDEX):
						if (PLATE [ INDEX ] != BYTES_PARTIAL [INDEX]):
							print ("INEQUALITY AT INDEX:", INDEX, PLATE[INDEX], BYTES_PARTIAL[INDEX])
							
						INDEX += 1
					
					assert (PLATE == BYTES [0:SCAN_SIZE])
				
				
				if (SCAN_LOOP % 1000 == 0 or LAST_SCAN == True):
					PERCENT = 100 * Fraction (INDEXES [1] / LAST_BYTE_INDEX)
					if (PERCENT.denominator == 1):
						PERCENT = str (int (PERCENT))
					else:
						PERCENT = str (float (PERCENT))
					
					BYTE_INDEX = "[REACHED BYTE INDEX:" + str (INDEXES[0]) + "]"
					PERCENT_STRING = "[" + str (PERCENT) + "%]"
								
					SIZE = "[SCAN SIZE: " + str (SCAN_SIZE) + "]"			
								
					CONTENT = "[FIRST 16 BYTES: " + PLATE[0:16].hex () + "]"
								
					print (
						"SCANNING:",
						BYTE_INDEX,
						CONTENT,
						PERCENT_STRING
					)
					
				SCAN_LOOP += 1
				
			PLACE_1 = perf_counter ()	
				
			SCAN.START ({
				"DRIVE PATH": DRIVE_PATH, 
				
				"BYTES INDEXES":  [ 0, LAST_BYTE_INDEX ],	
				"BYTES PER PLATE": BYTES_PER_PLATE,
				
				"PROGRESS": SCAN_PROGRESS
			})
			
			ELAPSED = perf_counter () - PLACE_1
			
			print ("Scan required", ELAPSED, "seconds.")
		else:
			print ("SKIPPING SCAN, STAGE = ", STAGE)
			
		STAGE += 1

		LOOP_COUNT += 1
		


	return
