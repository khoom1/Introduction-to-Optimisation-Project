#Functions to convert float to binary and binary to float
import numpy as np

def float2bin(number, places):
	#Round up to whole number
	whole = int(number)
	bin_whole = bin(whole)
	
	bin_num = bin(abs(whole)).replace("0b","") + "."
	if np.sign(number)==-1:
		bin_num = "-" + bin_num
	else:
		bin_num = "+" + bin_num
	
	#The remainding decimal
	dec = abs(number-whole)
	for i in range(places):
		dec = dec*2
		whole = str(int(dec))
		dec = dec - int(dec)
		bin_num += whole 
	
	return bin_num
	
def bin2float(bin_str):
	whole, dec = bin_str.split(".")
	num_decimals = len(bin_str)-len(whole)-1
	whole = int(whole,2)
	if dec:
		dec = int(dec,2)
	else:
		dec = 0.0
	
	if bin_str[0]=="-":
		sign=-1.0
	else:
		sign=1.0
	
	return whole + sign*dec/2.0**num_decimals
	
