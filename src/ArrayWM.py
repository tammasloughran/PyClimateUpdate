#!/usr/local/bin/python
# Adapted for numpy/ma/cdms2 by convertcdms.py
#
# Handle numpy arrays with missing values
# Jon Saenz, 20000410
# Jesus Fernandez, 20001116
import numpy

class MaskedArray:
	def __init__(self, data, miss, tol=0.0, tcode=numpy.float64):
		self.data=numpy.array(data,tcode)
		self.missing=miss
		himask = numpy.greater(self.data, miss + tol)
		lomask = numpy.less(self.data, miss - tol)
		self.mask = numpy.logical_or(himask, lomask)

	def mean(self):
		num = MaskedArray(numpy.add.reduce(self.data * self.mask), self.missing)
		den = MaskedArray(numpy.add.reduce(self.mask), self.missing)
		return num / den

	def setMissing(self, miss, tol=0.0):
		self.missing=miss
		himask = numpy.greater(self.data, miss + tol)
		lomask = numpy.less(self.data, miss - tol)
		self.mask = numpy.logical_and(logical_or(himask, lomask),self.mask)

	def applyMissing(self):
		self.data = self.data * self.mask + logical_not(self.mask) * self.missing

	def sqrt(self):
		nonegative=numpy.greater_equal(self.data, 0.0)
		valids = numpy.logical_and(self.mask, nonegative)
		sqdata=numpy.sqrt(self.data * valids) + self.missing*logical_not(valids)
		return MaskedArray(sqdata, self.missing)

	def toarray(self, tcode=numpy.float64):
		return self.data.astype(tcode)

	def __add__(self,marr):
		try: 
			valid=numpy.logical_and(self.mask, marr.mask)
			c=valid*(self.data+marr.data)+numpy.logical_not(valid)*self.missing
		except:
			valid=self.mask
			c=valid*(self.data+marr)+numpy.logical_not(valid)*self.missing
		return MaskedArray(c, self.missing)

	def __div__(self,marr):
		nozerosb=not_equal(marr.data, 0.0)
		validb=numpy.logical_and(marr.mask, nozerosb)
		valid=numpy.logical_and(self.mask, validb)
		denomzeros2ones = marr.data + numpy.logical_not(validb)
		c=valid*(self.data / denomzeros2ones)+numpy.logical_not(valid)*self.missing
		return MaskedArray(c, self.missing)

	def __getitem__(self,idx):
		return self.data[idx]

	def __getslice__(self,idx1,idx2):
		return self.data[idx1:idx2]  
  	
	def __mul__(self,marr):
		return self.__rmul__(marr)

	def __neg__(self):
		c = -self.data*self.mask + numpy.logical_not(self.mask)*self.missing
		return MaskedArray(c, self.missing)
	
	def __pow__(self,power):
		thezeros = numpy.equal(self.data,0.0)
		haszeros = numpy.add.reduce(ravel(thezeros))
		if haszeros and power < 0.0:
			valid = numpy.logical_and(self.mask,numpy.logical_not(thezeros))
			c = (self.data*valid+1.0*numpy.logical_not(valid))**power
			c = c * valid + numpy.logical_not(valid) * self.missing
		else:
			valid = self.mask
			c = valid * (self.data ** power) + numpy.logical_not(valid) * self.missing
		return MaskedArray(c, self.missing)
	def __repr__(self):
		return `self.data`

	def __radd__(self,marr):
		return self.__add__(marr)

	def __rdiv__(self,marr):
		nozerosb=numpy.not_equal(self.data, 0.0)
		validb=numpy.logical_and(self.mask,nozerosb)
		try:
			valid=numpy.logical_and(marr.mask, validb)
			denomzeros2ones = self.data + numpy.logical_not(validb)
			c=valid*(marr.data / denomzeros2ones)+numpy.logical_not(valid)*self.missing
		except:
			denomzeros2ones = self.data + numpy.logical_not(validb)
			c=validb*(marr / denomzeros2ones)+numpy.logical_not(validb)*self.missing
		return MaskedArray(c, self.missing)

	def __rmul__(self,marr):
		try: 
			valid=numpy.logical_and(self.mask,marr.mask)
			c=valid*(self.data * marr.data)+numpy.logical_not(valid)*self.missing
		except:
			c=self.mask*(self.data * marr)+numpy.logical_not(self.mask)*self.missing
		return MaskedArray(c, self.missing)

	def __rsub__(self, marr):
		return (-self).__add__(marr)

	def __sub__(self, marr):
		return self.__add__(-marr) 

if __name__ == "__main__":
	a = numpy.array(
		[[ 1.0, -67,     18.0, 9 ],
		 [ 6.7, 99.,      0.0, 45],
		 [ 0.0, 99.00001, 0.1, 20]]
	)
	ma = MaskedArray(a,99.)
	b = numpy.array(
		[[91.0, 98,     17.0, 90],
		 [ 6.7, 99.,      0.0, 44],
		 [10.0, 99.00001, 0.5, 10]]
	)
	mb = MaskedArray(b,100,2)
