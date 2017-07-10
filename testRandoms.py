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
	results = {}
	for name,f in getmembers(mr,isfunction):
		if '__' in name:
			continue
		results[name] = [f() for _ in range(1000)]
	for k,v in results.items():
		print k+" mean="+mean(v)+" median="+median(v)+" mode="+mode(v)

if __name__=='__main__':
	testFCTS()