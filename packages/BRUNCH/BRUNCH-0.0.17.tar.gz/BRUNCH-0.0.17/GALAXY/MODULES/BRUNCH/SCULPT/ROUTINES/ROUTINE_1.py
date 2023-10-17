

'''
from BRUNCH.SCULPT.ROUTINES.ROUTINES.1 import ROUTINE_1
'''

def ROUTINE_1 ():
	BYTES_PER_PLATE = 512 * 512;

	BYTES = b''

	LOOP = 1
	while (LOOP <= (BYTES_PER_PLATE / 8)):
		BYTES += b'\x00\x01\x00\x02\x00\x03\x00\x04'
		LOOP += 1
		
	return BYTES;