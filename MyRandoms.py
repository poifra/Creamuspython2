from __future__ import division
from random import random
from math import log, e, tan

RAND_MAX = 4294967295
PYO_RAND_SEED = 1
def __pyorand():
	global PYO_RAND_SEED
	PYO_RAND_SEED = (PYO_RAND_SEED * 1664525 + 1013904223) % RAND_MAX
	return PYO_RAND_SEED

def __checkZero(val):
	if val <= 0:
		return 0.0001
	return val

def __normalize(val):
	if val < 0:
		return 0
	if val > 1:
		return 1
	return val

def uniform():
	return random()

def linearMin():
	a = random()
	b = random()
	return a if a < b else b

def linearMax():
	a = random()
	b = random()
	return b if a < b else b

def triangle():
	a = random()
	b = random()
	return ((a+b)*0.5)

def exponMin(x1=5):
	x1 = __checkZero(x1)
	val = -log(random())/x1
	return __normalize(val)

def exponMax(x1=5):
	x1 = __checkZero(x1)
	val = 1.0-(-log(random())/x1)
	return __normalize(val)

def biExpon(x1=5):
	polar = 0
	val = 0
	x1 = __checkZero(x1)

	s = random() * 2
	if s > 1:
		polar = -1
		s = 2 - s
	else:
		polar = 1

	val = 0.5*(polar*log(s)/x1)+0.5

	return __normalize(val)

def cauchy(x1=5):
	rnd = 0.5
	while rnd == 0.5:
		rnd = random()

	if (__pyorand() < RAND_MAX/2):
		d = -1
	else:
		d = 1

	val = 0.5*(tan(rnd)*x1*d)+0.5
	return __normalize(val)

def weibull(x1=0.5,x2=1.5):
	x2 = __checkZero(x2)
	rnd = 1/(1-random())
	val = x1*pow(log(rnd),1/x2)
	return __normalize(val)

def gaussian(x1=0.5,x2=5):
	rnd = sum([random() for _ in range(6)])
	val = x2*(rnd-3)*0.33+x1
	return __normalize(val)

def gaussian2(x1=0.5,x2=5):
	rnd = sum([random() for _ in range(6)])
	val = x2*(rnd-3)*0.33+x1
	return val

def poisson(x1=5,x2=2):
	poissonTab = 0
	lastPoissonX1 = -99.0
	poissonBuffer = [0 for _ in range(2000)]
	if x1 < 0.1: x1 = 0.1
	if x2 < 0.1: x2 = 0.1

	if x1 != lastPoissonX1:
		lastPoissonX1 = x1
		poissonTab = 0
		factorial = 1
		for i in range(1,13): #interval [1,12]
			factorial *= i
			tot = 1000*(pow(e,-x1)*pow(x1,i)/factorial)
			j = 0
			while j < tot:
				poissonBuffer[poissonTab] = i
				poissonTab += 1
				j += 1
	val = poissonBuffer[__pyorand() % poissonTab] /12*x2
	return __normalize(val)

def poisson_2(x1=5,x2=2):
	poissonTab = 0
	lastPoissonX1 = -99.0
	poissonBuffer = [0 for _ in range(2000)]
	if x1 < 0.1: x1 = 0.1
	if x2 < 0.1: x2 = 0.1

	if x1 != lastPoissonX1:
		lastPoissonX1 = x1
		poissonTab = 0
		factorial = 1
		for i in range(1,13): #interval [1,12]
			factorial *= i
			tot = 1000*(pow(e,-x1)*pow(x1,i)/factorial)
			j = 0
			while j < tot:
				poissonBuffer[poissonTab] = i
				poissonTab += 1
				j += 1
	val = poissonBuffer[__pyorand() % poissonTab] /12*x2
	return val

def walker(x1=0.5,x2=0.5):
	walkerVal = 0.5
	if x2 < 0.002: x2 = 0.002

	modulo = x2*1000
	d = __pyorand() % 100

	if d < 50:
		walkerVal += (__pyorand()%modulo)*0.001
	else:
		walkerVal -= (__pyorand()%modulo)*0.001

	if walkerVal > x1:
		walkerVal = x1
	elif walkerVal < 0:
		walkerVal = 0
	return walkerVal

def loopseg(x1=0.5,x2=0.5):
	walkerVal = 0.5
	loopChoice = loopCountPlay = loopTime = loopCountRec = loopStop = 0
	loopLen = (__pyorand() % 10) + 3
	loopBuffer = [0 for _ in range(15)]
	if loopChoice == 0:
		loopCountPlay = loopTime = 0
		if x2 < 0.002: x2 = 0.002

		modulo = x2*1000
		d = __pyorand()%100

		if d < 50:
			walkerVal += (__pyorand()%modulo)*0.001
		else:
			walkerVal -= (__pyorand()%modulo)*0.001

		if walkerVal > x1:
			walkerVal = x1
		elif walkerVal < 0:
			walkerVal = 0

		loopBuffer[loopCountRec] = walkerVal
		loopCountRec += 1

		if loopCountRec < loopLen:
			loopChoice = 0
		else:
			loopChoice = 1
			loopStop = (__pyorand()%4)+1

	else:
		loopCountRec = 0
		walkerVal = loopBuffer[loopCountPlay]
		loopCountPlay += 1

		if loopCountPlay < loopLen:
			loopChoice = 1
		else:
			loopCountPlay = 0
			loopTime += 1
		if loopTime == loopStop:
			loopChoice = 0
			loopLen = (__pyorand()%10)+3
	return walkerVal