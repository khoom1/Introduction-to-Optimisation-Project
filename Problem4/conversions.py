#Functions to convert float to binary and binary to float
from ast import literal_eval
import numpy as np

def float2bin(number, places):
	#Round up to whole number
	whole = int(number)
	bin_whole = bin(whole)
	
	bin_num = bin(whole).replace("0b","") + "."
	
	#The remainding decimal
	dec = abs(number-whole)
	for i in range(places):
		dec = dec*2
		whole = str(int(dec))
		dec = dec - int(dec)
		bin_num += whole 
	
	return bin_num
	
def bin2float(bin_str, places):
	whole, dec = bin_str.split(".")
	whole = int(whole,2)
	if dec:
		dec = int(dec,2)
	else:
		dec = 0.0
	
	return whole + np.sign(whole)*dec/2.0**places
	
