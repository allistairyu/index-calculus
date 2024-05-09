from bsgs import bsgs
from index_calculus import solve
import time

DL_P = 941
B = 5
g = 627

if __name__ == '__main__':
	for h in range(1, 21):
		start_time = time.time()
		res1 = solve(g, h, DL_P)
		print("index calc: --- %s seconds ---" % (time.time() - start_time))

		start_time = time.time()
		res2 = bsgs(g, h, DL_P)
		print("bsgs      : --- %s seconds ---" % (time.time() - start_time))

		if pow(g, res1, DL_P) != h:
			print("index calc failed")
		if pow(g, res2, DL_P) != h:
			print("bsgs failed")
		print(res1)
		print()
		print()

