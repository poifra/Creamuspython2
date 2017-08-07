#encoding:utf-8
from __future__ import division
from random import random
from math import log, e, tan


'''
Various random generators, implemented from sources present in github.com/belangeo/pyo
'''
class MyRandoms:
	def __init__(self):
		self.RAND_MAX = 4294967295
		self.PYO_RAND_SEED = 1
		self.x1 = None
		self.x2 = None
		self.funcs = {
			"uniform" 	: self.__uniform,
			"linearMin" : self.__linearMin,
			"linearMax" : self.__linearMax,
			"triange" 	: self.__triangle,
			"exponMin" 	: self.__exponMin,
			"exponMax" 	: self.__exponMax,
			"biExpon" 	: self.__biExpon,
			"cauchy" 	: self.__cauchy,
			"weibull" 	: self.__weibull,
			"gaussian" 	: self.__gaussian,
			"gaussian2" : self.__gaussian2,
			"poisson" 	: self.__poisson,
			"poisson2" 	: self.__poisson_2,
			"walker" 	: self.__walker,
			"loopseg" 	: self.__loopseg
		}

	def call(self, funcName, **kwargs):
		argNum = len(kwargs.keys())
		if argNum == 1:
			self.x1 = kwargs['x1']
		elif argNum == 2:
			self.x1, self.x2 = kwargs['x1'], kwargs['x2']
		return self.funcs[funcName]()

	def addFunc(self,funcName, funcPtr):
		if funcName in self.funcs.keys():
			raise ValueError("Function name already taken.")
		else:
			self.funcs[funcName] = funcPtr

	def __pyorand(self):
		self.PYO_RAND_SEED = (self.PYO_RAND_SEED * 1664525 + 1013904223) % self.RAND_MAX
		return self.PYO_RAND_SEED

	def __checkZero(self, val):
		if val <= 0 or val == None:
			return 0.0001
		return val

	def __normalize(self, val):
		#this doesnt sound right
		if val < 0:
			return 0
		if val > 1:
			return 1
		return val

	def __uniform(self):
		return random()

	def __linearMin(self):
		a = random()
		b = random()
		return a if a < b else b

	def __linearMax(self):
		a = random()
		b = random()
		return b if a < b else b

	def __triangle(self):
		a = random()
		b = random()
		return ((a+b)*0.5)


	def __exponMin(self):
		'''
		expon_min
		self.x1: slope {0 = no slope -> 10 = sharp slope}
		'''
		self.x1 = self.__checkZero(self.x1)
		val = -log(random())/self.x1
		return self.__normalize(val)


	def __exponMax(self):
		'''
		expon_max
		self.x1: slope {0 = no slope -> 10 = sharp slope}
		'''
		self.x1 = self.__checkZero(self.x1)
		val = 1.0-(-log(random())/self.x1)
		return self.__normalize(val)


	def __biExpon(self):
		'''
		biexpon
		self.x1: bandwidth {0 = huge bandwidth -> 10 = narrow bandwidth}
		'''
		polar = 0
		val = 0
		self.x1 = self.__checkZero(self.x1)

		s = random() * 2
		if s > 1:
			polar = -1
			s = 2 - s
		else:
			polar = 1

		val = 0.5*(polar*log(s)/self.x1)+0.5

		return self.__normalize(val)

		
	def __cauchy(self):
		'''
		cauchy
		self.x1: bandwidth {0 = huge bandwidth -> 10 = narrow bandwidth}
		'''
		self.x1 = self.__checkZero(self.x1)
		rnd = 0.5
		while rnd == 0.5:
			rnd = random()

		if (self.__pyorand() < self.RAND_MAX/2):
			d = -1
		else:
			d = 1

		val = 0.5*(tan(rnd)*self.x1*d)+0.5
		return self.__normalize(val)



	def __weibull(self):
		'''
		weibull
		self.x1: mean location {0 -> 1}
		self.x2: shape {0.5 = linear min, 1.5 = expon min, 3.5 = gaussian}
		'''
		self.x1 = self.__checkZero(self.x1)
		self.x2 = self.__checkZero(self.x2)
		rnd = 1/(1-random())
		val = self.x1*pow(log(rnd),1/self.x2)
		return self.__normalize(val)


	def __gaussian(self):
		'''
		gaussian
		self.x1: mean location {0 -> 1}
		self.x2: bandwidth {0 = narrow bandwidth -> 10 = huge bandwidth}
		'''
		self.x1 = self.__checkZero(self.x1)
		self.x2 = self.__checkZero(self.x2)
		rnd = sum([random() for _ in range(6)])
		val = self.x2*(rnd-3)*0.33+self.x1
		return self.__normalize(val)

	def __gaussian2(self):
		"""same as gaussian but without normalization"""
		self.x1 = self.__checkZero(self.x1)
		self.x2 = self.__checkZero(self.x2)
		rnd = sum([random() for _ in range(6)])
		val = self.x2*(rnd-3)*0.33+self.x1
		return val

	def __poisson(self):
		"""
		poisson
		self.x1: gravity center {0 = low values -> 10 = high values}
		self.x2: compress/expand range {0.1 = full compress -> 4 full expand}
		"""
		poissonTab = 0
		lastPoisson = -99.0
		poissonBuffer = [0 for _ in range(2000)]
		if self.x1 < 0.1 or self.x1 == None: self.x1 = 0.1
		if self.x2 < 0.1 or self.x2 == None: self.x2 = 0.1

		if self.x1 != lastPoisson:
			lastPoisson = self.x1
			poissonTab = 0
			factorial = 1
			for i in range(1,13): #interval [1,12]
				factorial *= i
				tot = 1000*(pow(e,-self.x1)*pow(self.x1,i)/factorial)
				j = 0
				while j < tot:
					poissonBuffer[poissonTab] = i
					poissonTab += 1
					j += 1
		val = poissonBuffer[self.__pyorand() % poissonTab] /12*self.x2
		return self.__normalize(val)

	def __poisson_2(self):
		poissonTab = 0
		lastPoisson = -99.0
		poissonBuffer = [0 for _ in range(2000)]
		if self.x1 < 0.1 or self.x1 == None : self.x1 = 0.1
		if self.x2 < 0.1 or self.x2 == None : self.x2 = 0.1

		if self.x1 != lastPoisson:
			lastPoisson = self.x1
			poissonTab = 0
			factorial = 1
			for i in range(1,13): #interval [1,12]
				factorial *= i
				tot = 1000*(pow(e,-self.x1)*pow(self.x1,i)/factorial)
				j = 0
				while j < tot:
					poissonBuffer[poissonTab] = i
					poissonTab += 1
					j += 1
		val = poissonBuffer[self.__pyorand() % poissonTab] /12*self.x2
		return val

	def __walker(self):
		"""
		walker
		self.x1: maximum value {0.1 -> 1}
		self.x2: maximum step {0.1 -> 1}
		"""
		walkerVal = 0.5
		
		if self.x2 < 0.002 or self.x1 == None: self.x2 = 0.002
		if self.x2 < 0.002 or self.x2 == None: self.x2 = 0.002
		
		modulo = int(self.x2*1000)
		d = self.__pyorand() % 100

		if d < 50:
			walkerVal += (self.__pyorand()%modulo)*0.001
		else:
			walkerVal -= (self.__pyorand()%modulo)*0.001

		if walkerVal > self.x1:
			walkerVal = self.x1
		elif walkerVal < 0:
			walkerVal = 0
		return walkerVal

	def __loopseg(self):
		"""
		loopseg
		self.x1: maximum value {0.1 -> 1}
		self.x2: maximum step {0.1 -> 1}
		"""
		if self.x2 < 0.002 or self.x1 == None: self.x2 = 0.002
		if self.x2 < 0.002 or self.x2 == None: self.x2 = 0.002

		walkerVal = 0.5
		loopChoice = loopCountPlay = loopTime = loopCountRec = loopStop = 0
		loopLen = (self.__pyorand() % 10) + 3
		loopBuffer = [0 for _ in range(15)]
		if loopChoice == 0:
			loopCountPlay = loopTime = 0
			if self.x2 < 0.002: self.x2 = 0.002

			modulo = int(self.x2*1000)
			d = self.__pyorand()%100

			if d < 50:
				walkerVal += (self.__pyorand()%modulo)*0.001
			else:
				walkerVal -= (self.__pyorand()%modulo)*0.001

			if walkerVal > self.x1:
				walkerVal = self.x1
			elif walkerVal < 0:
				walkerVal = 0

			loopBuffer[loopCountRec] = walkerVal
			loopCountRec += 1

			if loopCountRec < loopLen:
				loopChoice = 0
			else:
				loopChoice = 1
				loopStop = (self.__pyorand()%4)+1

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
				loopLen = (self.__pyorand()%10)+3
		return walkerVal