from __future__ import division
import MyRandoms as mr
from inspect import isfunction, getmembers

def mean(lst):
	return str(sum(lst)/len(lst))

def median(lst):
	return str(sorted(lst)[int(len(lst)/2)])

def mode(lst):
	return str(max(set(lst), key=lst.count))

def testFCTS():
	rngInstance = mr.MyRandoms()
	results = {}
	for func in rngInstance.funcs.keys():
		results[func] = [rngInstance.call(func) for _ in range(100)]

	for k,v in results.items():
		print k, mean(v), median(v), mode(v)
		print v


if __name__=='__main__':
	testFCTS()