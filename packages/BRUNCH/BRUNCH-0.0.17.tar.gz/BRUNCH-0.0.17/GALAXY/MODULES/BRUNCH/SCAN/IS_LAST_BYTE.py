


'''

'''

def IS_AFTER_END (f, LAST_BYTE_INDEX):
	try:
		f.seek (LAST_BYTE_INDEX)
		print ("FOUND LAST BYTE INDEX")		
	except Exception as E:
		print ("Exception1:", E)
		return True
		
	return False

def IS_BEFORE_END (f, LAST_BYTE_INDEX):
	try:
		f.seek (LAST_BYTE_INDEX)
		PLATE = f.read (2)
		if (len (PLATE) == 0):
			return False;
			
		print (f"COULD READ '{ len (PLATE) }' BYTES")
		
	except Exception as E:
		print ("Exception2:", E)
		pass;
				
	return True


def DEEM (PARAMS):
	print ("DEEM IF IS LAST BYTE")

	DRIVE_PATH = PARAMS ["drive path"]
	LAST_BYTE_INDEX = PARAMS ["last byte index"]

	with open (DRIVE_PATH, "rb") as f:
		if (IS_AFTER_END (f, LAST_BYTE_INDEX)):
			return [ False, "THE LAST BYTE DECLARED IS AFTER THE LAST BYTE" ]
		
		f.close ()
		
	print ("-> ISN'T AFTER END")
	
	with open (DRIVE_PATH, "rb") as f:
		if (IS_BEFORE_END (f, LAST_BYTE_INDEX)):
			return [ False, "THE LAST BYTE DECLARED IS BEFORE THE LAST BYTE" ]
			
		f.close ()
		
	print ("-> ISN'T BEFORE END")

	return [ True, "" ]