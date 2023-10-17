
'''
import BRUNCH.SCULPT as SCULPT

SCULPT.START ({
	"DRIVE PATH": DRIVE_PATH,
	
	"BYTES INDEXES": [ 0, 28 ],		
	"BYTES FOR PLATE": b'\xff\xfe\xfd\xfc\xfb\xfa\xf9\xf8\xf7\xf6',
	
	"PROGRESS": PROGRESS
})
'''


def PROGRESS (PARAMS):
	return;


#
#	https://python-jsonschema.readthedocs.io/en/latest/
#
from jsonschema import validate
SCHEMA = {
    "type" : "object",
	"required": [ 
		"DRIVE PATH",
		"BYTES INDEXES", 
		"BYTES FOR PLATE" 
	],
    "properties" : {
		"DRIVE PATH": {
			"type": "string"
		},
		
        "BYTES INDEXES" : { 
			"type" : "array",
		}
    }
}

def START (CARGO):
	validate (
		instance = CARGO, 
		schema = SCHEMA
	)

	DRIVE_PATH = CARGO ["DRIVE PATH"]
	
	BYTES_FOR_PLATE = CARGO ["BYTES FOR PLATE"]
	assert (type (BYTES_FOR_PLATE) == bytes)
	assert (len (BYTES_FOR_PLATE) >= 1)
	
	BYTES_PER_PLATE = len (BYTES_FOR_PLATE)
	BYTES_INDEXES = CARGO ["BYTES INDEXES"]
	
	MEAL_INDEX_START = BYTES_INDEXES [0];
	MEAL_INDEX_END = BYTES_INDEXES [1];

	if ("PROGRESS" in CARGO):
		PROGRESS = CARGO ["PROGRESS"]

	with open (DRIVE_PATH, "wb") as SELECTOR:
		SELECTOR.seek (MEAL_INDEX_START)
		
		print (f"OPENED DRIVE '{ DRIVE_PATH }' FOR SCULPTING")
		
		#LOOP = 1
		LAST_LOOP = False;
		PLATE = True;
		while PLATE:
			#if (LOOP % 1000 == 0):
			#	print ("SCULPTING")
			#LOOP += 1
		
			PLATE_INDEX_START = SELECTOR.tell ()
			
			#print ("PLATE INDEX START:", PLATE_INDEX_START)
			
			#
			#	CHECK IF A FULL PLATE WOULD 
			#	PUT THE SCANNER PAST THE LAST INDEX
			#
			if (
				(PLATE_INDEX_START + BYTES_PER_PLATE) > MEAL_INDEX_END
			):
				SCULPT_SIZE = MEAL_INDEX_END - PLATE_INDEX_START + 1
				
				LAST_LOOP = True
				
				if (SCULPT_SIZE <= 0):
					print ("SCULPT ENDED, SCULPT SIZE IS 0")
				
					return;
					
				SCULPTURE = BYTES_FOR_PLATE [0:SCULPT_SIZE]
					
			else:
				SCULPT_SIZE = BYTES_PER_PLATE
				SCULPTURE = BYTES_FOR_PLATE

			
			SELECTOR.write (SCULPTURE)
			PLATE_INDEX_END = SELECTOR.tell () - 1
			
			assert (len (SCULPTURE) == SCULPT_SIZE)
			
			PROGRESS ({
				"SIZE": SCULPT_SIZE,
				"LAST_LOOP": LAST_LOOP,
				"INDEXES": [
					PLATE_INDEX_START,
					PLATE_INDEX_END
				]
			})
			
			if (LAST_LOOP):
				print ("CLOSING SCULPT POINTER") 
			
				SELECTOR.close ()
			
				print ()
				print ("SCULPT IS DONE, LAST BYTE INDEX =", PLATE_INDEX_END)
				print ()
				
				
				
				return;