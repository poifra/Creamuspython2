from __future__ import division
from random import random
from math import log

RAND_MAX = 4294967295
PYO_RAND_SEED = 1
def pyorand():
    PYO_RAND_SEED = (PYO_RAND_SEED * 1664525 + 1013904223) % RAND_MAX
    return PYO_RAND_SEED

def checkZero(val):
	if val <= 0:
		return 0.00001
	return val

def normalize(val):
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

def exponMin(x1):
	x1 = checkZero(x1)
	val = -log(random())/x1
	return normalize(val)

def exponMax(x1):
=	x1 = checkZero(x1)
	val = 1-log(random())/x1
	return normalize(val)

def biExpon(x1):
	polar = 0
	val = 0
	x1 = checkZero(x1)

	s = random() * 2
	if s > 1:
		polar = -1
		s = 2 - s
	else:
		polar = 1

	val = 0.5*(polar*log(s)/x1)+0.5

	return normalize(val)

def cauchy(x1):
	rnd = 0.5
	while rnd == 0.5:
		rnd = random()

	if (pyorand() < RAND_MAX/2):
		d = -1
	else:
		d = 1

	val = 0.5*(tan(rnd)*x1*d)+0.5
	return normalize(val)

def weibull(x1,x2):
	x2 = checkZero(x2)
	rnd = 1/(1-random())
	val = x1*pow(log(rnd),1/x2)
	return normalize(val)

def gaussian(x1,x2):
	rnd = sum([random() for _ in range(6)])
	val = x2*(rnd-3)*0.33+x1
	return normalize(val)

#TODO : initialize stuff that wasnt
def poisson(x1,x2):
	if x1 < 0.1: x1 = 0.1
	if x2 < 0.1: x2 = 0.1

	if x1 != lastPoissonX1:
		lastPoissonX1 = x1
		poissonTab = 0
		factorial = 1
		for i in range(1,13): #interval [1,12]
			factorial *= i
			tot = 1000*(pow(e,-x1)*pow(x1,i)/factorial)
			for j in range(tot):
				poissonBuffer[poissonTab] = i
				poissonTab += 1
	val = poissonBuffer[pyorand() % poissonTab] /12*x2
	return normalize(val)

def walker(x1,x2):
	if x2 < 0.002: x2 = 0.002

	modulo = x2*1000
	d = pyorand() % 100

	if d < 50:
		walkerVal += (pyorand()%modulo)*0.001
	else:
		walkerVal -= (pyorand()%modulo)*0.001

	if walkerVal > x1:
		walkerVal = x1
	else if walkerVal < 0:
		walkerVal = 0
	return walkerVal