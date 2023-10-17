

'''
from BRUNCH.SCULPT.ROUTINES.ROUTINE_2 import ROUTINE_2
'''

def ROUTINE_2 ():
	BYTES_PER_PLATE = 512 * 512;

	BYTES = b''

	LOOP = 1
	while (LOOP <= (BYTES_PER_PLATE / 8)):
		BYTES += b'\xFF\xEF\xFF\xDF\xFF\xCF\xFF\xBF'
		LOOP += 1
		
	return BYTES;