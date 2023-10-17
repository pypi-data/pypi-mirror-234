




'''
	import BRUNCH.SCAN as SCAN
'''

'''
	PARAMS = {
		"PLATE": PLATE,
		"BYTES INDEXES": [
			PLATE_INDEX_START,
			PLATE_INDEX_START + SCAN_SIZE
		]
	}
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
		"BYTES PER PLATE" 
	],
    "properties" : {
		"DRIVE PATH": {
			"type": "string"
		},
        "BYTES INDEXES" : { 
			"type" : "array",
		},
        "BYTES PER PLATE" : {
			"type" : "number"
		}
    }
}

def START (CARGO):
	#print ("CARGO", CARGO)

	validate (
		instance = CARGO, 
		schema = SCHEMA
	)

	DRIVE_PATH = CARGO ["DRIVE PATH"]
	BYTES_PER_PLATE = CARGO ["BYTES PER PLATE"]
	BYTES_INDEXES = CARGO ["BYTES INDEXES"]
	
	#print ("VALID?")
	
	
	if ("PROGRESS" in CARGO):
		PROGRESS = CARGO ["PROGRESS"]
	
	
	#
	#	--
	#

	'''
		BYTES PER PLATE: 10
		BYTE INDEXES: [ 0, 28 ]
	
		 0 TO  9
		10 TO 19
		
		20 TO 29
	'''

	MEAL_INDEX_START = BYTES_INDEXES [0];
	MEAL_INDEX_END = BYTES_INDEXES [1];

	with open (DRIVE_PATH, "rb") as f:
		f.seek (MEAL_INDEX_START)
		#PLATE_INDEX_0 = f.tell ()
		
		print (f"OPENED DRIVE '{ DRIVE_PATH }' FOR SCANNING")
		
		LAST_SCAN = False
		PLATE = True;
		while PLATE:
			PLATE_INDEX_START = f.tell ()
					
			#print (PLATE_INDEX_START, BYTES_PER_PLATE, MEAL_INDEX_END)
					
			#
			#	CHECK IF A FULL PLATE WOULD 
			#	PUT THE SCANNER PAST THE LAST INDEX
			#
			if (
				(PLATE_INDEX_START + BYTES_PER_PLATE) > MEAL_INDEX_END
			):
				LAST_SCAN = True
				SCAN_SIZE = MEAL_INDEX_END - PLATE_INDEX_START + 1

				#print ("PAST LAST INDEX, SCAN_SIZE =", SCAN_SIZE)

				if (SCAN_SIZE <= 0):
					return;
				
			else:
				SCAN_SIZE = BYTES_PER_PLATE;
				
			#print ("SCAN SIZE:", SCAN_SIZE)
			
			PLATE = f.read (SCAN_SIZE)
			if (len (PLATE) == 0):
				print ("THERE WERE NO BYTES LEFT TO SCAN")
				return;	
			
			#print ("TELL:", f.tell ())
			
			PLATE_INDEX_END = f.tell () - 1
			
			PROGRESS ({
				"PLATE": PLATE,
				"SCAN SIZE": SCAN_SIZE,
				"LAST SCAN": LAST_SCAN,
				"INDEXES": [
					PLATE_INDEX_START,
					PLATE_INDEX_END
				]
			})	
			
			if (LAST_SCAN):
				print ()
				print ("SCAN IS DONE")
				print ()
				
				f.close ()
				
				return;
			
			
	
			 
		 
