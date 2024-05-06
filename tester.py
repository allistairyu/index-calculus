from bsgs import bsgs
from index_calculus import main_func
import time

PARAM_P = 18443
B = 5
g = 37
h = 211

if __name__ == '__main__':
	start_time = time.time()
	main_func()
	print("index calc: --- %s seconds ---" % (time.time() - start_time))

	start_time = time.time()
	bsgs(g, h, PARAM_P)
	print("bsgs      : --- %s seconds ---" % (time.time() - start_time))

