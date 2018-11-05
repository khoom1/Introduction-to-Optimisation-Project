import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Process, Queue, Pool,cpu_count
import time

def argm(a):
	return [a[0],2*a[0]]

def tes(b):
	a = b
	
if __name__ == '__main__':
	pool1 = Pool(processes=cpu_count())
	resultx = np.zeros((10,1))
	
	begin = time.time()
	for i in range(10):
		resultx = pool1.apply(tes, args=(i,))
	#pool1.close()
	#pool1.join()
	end = time.time()
	print("Dual decomposition in parallel takes %fs." %(end-begin))
	print(resultx)
	
	
	pool2 = Pool()
	begin = time.time()
	a = pool2.imap(argm, [(i,1,1) for i in range(10)])
	end = time.time()
	print("Dual decomposition in parallel takes %fs." %(end-begin))
	#print(list(a))
	
	begin = time.time()
	for i in range(100):
		d = Process(target=tes,args=(i,))
	end = time.time()
	print("Dual decomposition in parallel takes %fs." %(end-begin))
	
	