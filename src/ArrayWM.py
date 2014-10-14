#!/usr/local/bin/python
# Adapted for numpy/ma/cdms2 by convertcdms.py
#
# Handle Numeric arrays with missing values
# Jon Saenz, 20000410
# Jesus Fernandez, 20001116
import numpy.oldnumeric as Numeric

class MaskedArray:
	def __init__(self, data, miss, tol=0.0, tcode=Numeric.Float64):
		self.data=Numeric.array(data,tcode)
		self.missing=miss
		himask = Numeric.greater(self.data, miss + tol)
		lomask = Numeric.less(self.data, miss - tol)
		self.mask = Numeric.logical_or(himask, lomask)

	def mean(self):
		num = MaskedArray(Numeric.add.reduce(self.data * self.mask), self.missing)
		den = MaskedArray(Numeric.add.reduce(self.mask), self.missing)
		return num / den

	def setMissing(self, miss, tol=0.0):
		self.missing=miss
		himask = Numeric.greater(self.data, miss + tol)
		lomask = Numeric.less(self.data, miss - tol)
		self.mask = Numeric.logical_and(logical_or(himask, lomask),self.mask)

	def applyMissing(self):
		self.data = self.data * self.mask + logical_not(self.mask) * self.missing

	def sqrt(self):
		nonegative=Numeric.greater_equal(self.data, 0.0)
		valids = Numeric.logical_and(self.mask, nonegative)
		sqdata=Numeric.sqrt(self.data * valids) + self.missing*logical_not(valids)
		return MaskedArray(sqdata, self.missing)

	def toarray(self, tcode=Numeric.Float64):
		return self.data.astype(tcode)

	def __add__(self,marr):
		try: 
			valid=Numeric.logical_and(self.mask, marr.mask)
			c=valid*(self.data+marr.data)+Numeric.logical_not(valid)*self.missing
		except:
			valid=self.mask
			c=valid*(self.data+marr)+Numeric.logical_not(valid)*self.missing
		return MaskedArray(c, self.missing)

	def __div__(self,marr):
		nozerosb=not_equal(marr.data, 0.0)
		validb=Numeric.logical_and(marr.mask, nozerosb)
		valid=Numeric.logical_and(self.mask, validb)
		denomzeros2ones = marr.data + Numeric.logical_not(validb)
		c=valid*(self.data / denomzeros2ones)+Numeric.logical_not(valid)*self.missing
		return MaskedArray(c, self.missing)

	def __getitem__(self,idx):
		return self.data[idx]

	def __getslice__(self,idx1,idx2):
		return self.data[idx1:idx2]  
  	
	def __mul__(self,marr):
		return self.__rmul__(marr)

	def __neg__(self):
		c = -self.data*self.mask + Numeric.logical_not(self.mask)*self.missing
		return MaskedArray(c, self.missing)
	
	def __pow__(self,power):
		thezeros = Numeric.equal(self.data,0.0)
		haszeros = Numeric.add.reduce(ravel(thezeros))
		if haszeros and power < 0.0:
			valid = Numeric.logical_and(self.mask,Numeric.logical_not(thezeros))
			c = (self.data*valid+1.0*Numeric.logical_not(valid))**power
			c = c * valid + Numeric.logical_not(valid) * self.missing
		else:
			valid = self.mask
			c = valid * (self.data ** power) + Numeric.logical_not(valid) * self.missing
		return MaskedArray(c, self.missing)
	def __repr__(self):
		return `self.data`

	def __radd__(self,marr):
		return self.__add__(marr)

	def __rdiv__(self,marr):
		nozerosb=Numeric.not_equal(self.data, 0.0)
		validb=Numeric.logical_and(self.mask,nozerosb)
		try:
			valid=Numeric.logical_and(marr.mask, validb)
			denomzeros2ones = self.data + Numeric.logical_not(validb)
			c=valid*(marr.data / denomzeros2ones)+Numeric.logical_not(valid)*self.missing
		except:
			denomzeros2ones = self.data + Numeric.logical_not(validb)
			c=validb*(marr / denomzeros2ones)+Numeric.logical_not(validb)*self.missing
		return MaskedArray(c, self.missing)

	def __rmul__(self,marr):
		try: 
			valid=Numeric.logical_and(self.mask,marr.mask)
			c=valid*(self.data * marr.data)+Numeric.logical_not(valid)*self.missing
		except:
			c=self.mask*(self.data * marr)+Numeric.logical_not(self.mask)*self.missing
		return MaskedArray(c, self.missing)

	def __rsub__(self, marr):
		return (-self).__add__(marr)

	def __sub__(self, marr):
		return self.__add__(-marr) 

if __name__ == "__main__":
	a = Numeric.array(
		[[ 1.0, -67,     18.0, 9 ],
		 [ 6.7, 99.,      0.0, 45],
		 [ 0.0, 99.00001, 0.1, 20]]
	)
	ma = MaskedArray(a,99.)
	b = Numeric.array(
		[[91.0, 98,     17.0, 90],
		 [ 6.7, 99.,      0.0, 44],
		 [10.0, 99.00001, 0.5, 10]]
	)
	mb = MaskedArray(b,100,2)
