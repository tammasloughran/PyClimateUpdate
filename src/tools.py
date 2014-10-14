# Adapted for numpy/ma/cdms2 by convertcdms.py
# tools.py

"""Some tools used in other modules

"""
#
# Jon Saenz, while at UCLA, 19990816
# 
# Copyright (C) 2000, Jon Saenz, Juan Zubillaga and Jesus Fernandez
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, version 2.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
# 
import numpy as Numeric
import math
import sys
import pyclimate.pyclimateexcpt
excpt = pyclimate.pyclimateexcpt

def pyclimateversion():
	"Returns the currently installed version of PyClimate as a string"
	return "1.2"

def unshape(arraynd, spacelast=1):
	"""Crashes all but the first dimension of an array in one.

  Arguments:

    'arraynd' -- N-dimensional NumPy array (N>=2)

    'spacelast' -- A bit indicating if the space dimensions are all but 
                   the first (this is the default; 'spacelast'=1) or all
                   but last
  
  Returns a tuple (array2d, oldshape)

    'array2d' -- 2-dimensional array with the first dimension as the 
                 input one and the remaining ones compresed in the 
                 second dimension.

    'oldshape' -- Is the shape (a tuple) of <arraynd>. It'll be needed to 
                  recover the shape with <deunshape()>.
  """
	arraynd = Numeric.array(arraynd)
	oldshape = arraynd.shape
	if spacelast:
		taillen = Numeric.multiply.reduce(oldshape[1:])
		arraynd.shape = (oldshape[0], taillen)
	else:
		headlen = Numeric.multiply.reduce(oldshape[:-1])
		arraynd.shape = (headlen, oldshape[-1])
	return arraynd, oldshape

def deunshape(array2d, oldshape):
	"""Recover the dimensions of an <unshape()>-ed array.

  Arguments:

    'array2d' -- 2-dimensional array which dimensions are to be recovered.

    'oldshape' -- The shape (a tuple) the array must be returned with.

  Returns the array with the specified shape.
  """
	array2d = Numeric.array(array2d)
	array2d.shape = oldshape
	return array2d 

def getneofs(lbd, percent=70):
	"""EOF variance percent stopping rule

  Argument:

    'lbd' -- Numpy 1D array containing the lambdas (eigenvalues) in decreasing
             order

  Optional Argument:

    'percent' -- Percentage of total variance to retain

  Returns the number of EOFs to retain to keep at least 'percent' of the 
  total variance of the field.
  """
	percentlbd = 100*lbd/Numeric.add.reduce(lbd)
	underlimit = Numeric.less_equal(
		Numeric.add.accumulate(percentlbd), 
		float(percent)
	)
	return 1 + Numeric.add.reduce(underlimit)

def correlation(xt, yt):
	"Returns the correlation of arrays"
	xanom = xt - Numeric.add.reduce(xt)/len(xt)
	yanom = yt - Numeric.add.reduce(yt)/len(yt)
	xstd = xanom / Numeric.sqrt(Numeric.add.reduce(xanom * xanom)) 
	ystd = yanom / Numeric.sqrt(Numeric.add.reduce(yanom * yanom))
	return Numeric.dot(xstd, ystd) 

def ttest(xa, xb, significance=0.05):
	"""Performs a t-test returning a mask for the significant values

  Arguments:

  'xa' -- an array with time as first dimension.

  'xb' -- another array like 'xa'. The lenght of the first dimension may differ
          but not the others.

  Optional arguments:

  'significance' -- is the significance level of the t-test

  This test is intended to establish if the mean values of 'xa' and 'xb'
  differ significantly with a given 'significance' level. The variances of 
  the two datasets are assumed to be the same.
  """
	import pyclimate.pydcdflib
	na = len(xa)
	nb = len(xb)
	dof = na + nb - 2
	avea = Numeric.add.reduce(xa)/float(na)
	aveb = Numeric.add.reduce(xb)/float(nb)
	xa = xa - avea
	xb = xb - aveb
	stder = Numeric.add.reduce(xa*xa) + Numeric.add.reduce(xb*xb)
	stder = stder * (1.0/na + 1.0/nb ) / float(dof)
	stder = Numeric.sqrt(stder)
	thets = (avea - aveb) / stder
	t = pyclimate.pydcdflib.CDFT()
	t.which = 2
	t.p = significance/2.0
	t.df = dof
	pyclimate.pydcdflib.pycdft(t)
	tlow = t.t
	t.p = 1.0 - significance/2.0
	pyclimate.pydcdflib.pycdft(t)
	thigh = t.t
	lowmask = Numeric.less(thets, tlow)
	highmask = Numeric.greater(thets, thigh)
	return Numeric.logical_or(lowmask,highmask)

def ftest(xa, xb, significance=0.05):
	"""Two-tailed F-test returning a mask for the significant values
 
  Arguments:

  'xa' -- an array with time as first dimension.

  'xb' -- another array like 'xa'. The lenght of the first dimension may differ
        but not the others.

  Optional arguments:

  'significance' -- is the significance level of the t-test
 
  This test is intended to establish if the variances of 'xa' and 'xb'
  differ signicatively with a given significance level.
  """                                          
	import pyclimate.pydcdflib
	na = len(xa)
	nb = len(xb)
	avea = Numeric.add.reduce(xa)/float(na)
	aveb = Numeric.add.reduce(xb)/float(nb)
	vara = Numeric.add.reduce((xa-avea)*(xa-avea))/float(na)
	varb = Numeric.add.reduce((xb-aveb)*(xb-aveb))/float(nb)
	thefs = vara / varb
	f = pyclimate.pydcdflib.CDFF()
	f.which = 2
	f.p = significance/2.0   # two--tailed
	f.dfn = na - 1
	f.dfd = nb - 1
	pyclimate.pydcdflib.pycdff(f)
	flow = f.f
	f.p = 1.0 - significance/2.0
	pyclimate.pydcdflib.pycdff(f)
	fhigh = f.f
	lowmask = Numeric.less(thefs, flow)
	highmask = Numeric.greater(thefs, fhigh)
	return Numeric.logical_or(lowmask,highmask)

class _TimeSeries:
	"""Object to extract statistical info from a sequence object

  This class is not officially released in PyClimate 1.2
  Use it at your own risk (as the rest of the package ;-). If you
  want to use it you'd better remove the leading underscore.
  """
	def __init__(self, seq):
		"""Constructor for TimeSeries object

		Argument:

		  'seq' -- Any python sequence. If it is multidimensional
		           the averaging operations will be performed over
		           the first dimension.
		"""
		self.data = Numeric.array(seq)
		self.shape = self.data.shape
		self.records = len(self.data)
		self.frecords = float(self.records)
		self.isunidimensional = len(self.shape)==1
	
	def center(self):
		"Centered (mean removed) version of the TimeSeries object"
		rval = self.data - self.mean()
		return TimeSeries(rval)

	def iqd(self):
		"Inter-quartilic distance"
		sdata = Numeric.sort(self.data,0)
		return Numeric.absolute(
			sdata[(self.records*3)/4]
			- sdata[self.records/4]
		) 

	def max(self):
		"Maximum"
		sdata = Numeric.sort(self.data,0)
		return sdata[-1]
	
	def median(self):
		"Median"
		sdata = Numeric.sort(self.data,0)
		return sdata[self.records/2]
	
	def min(self):
		"Minimum"
		sdata = Numeric.sort(self.data,0)
		return sdata[0]
	
	def q1(self):
		"First quartil"
		sdata = Numeric.sort(self.data,0)
		return sdata[self.records/4]
	
	def q3(self):
		"Third quartil"
		sdata = Numeric.sort(self.data,0)
		return sdata[(self.records*3)/4]
	
	def mean(self):
		"Mean"
		return Numeric.add.reduce(self.data)/self.frecords

	def mad(self):
		"Mean absolute deviation"
		return Numeric.add.reduce(Numeric.absolute(self.center().data))/self.frecords

	def standardize(self):
		"Standardized version of the TimeSeries object"
		std = self.std()
		mask = Numeric.not_equal(std,0)
		maskedstd = std + Numeric.logical_not(mask)
		rval = mask * (self.data - self.mean()) / maskedstd
		return TimeSeries(rval)

	def std(self):
		"standard deviation"
		return Numeric.sqrt(self.variance())

	def toarray(self):
		"Returns the TimeSeries object internal data as a NumPy array"
		return Numeric.array(self.data)

	def variance(self):
		"Variance"
		return Numeric.add.reduce(self.center().data * self.center().data)/self.frecords

	def correlation(self, TSobj):
		"Correlation with other TSObject"
		if len(TSobj) != self.records:
			raise excpt.SVDLengthException(len(TSobj),self.records)
		rval = self.standardize().data * TSobj.standardize().data
		return Numeric.add.reduce(rval)/self.frecords

	def kurtosis(self):
		"Kurtosis"
		rval = self.data - self.mean()
		rval = rval ** 4.
		rval = Numeric.add.reduce(rval) / self.frecords
		rval = rval / (self.variance()**2)
		rval = rval - 3.
		return rval

	def skewness(self):
		rval = self.data - self.mean()
		rval = rval ** 3.
		rval = Numeric.add.reduce(rval) / self.frecords
		rval = rval / (Numeric.sqrt(self.variance()**3))
		return rval

	def autocorrelation(self, lag=1):
		"Autocorrelation. A 'lag' can be specified (Defaults to 1)"
		a = TimeSeries(self.data[lag:])
		b = TimeSeries(self.data[:-lag])
		return a.correlation(b)

	def regression(self, TSobj):
		"Regression over another TSobject"
		if not self.isunidimensional:
			sys.stderr.write("Only one-dimensional arrays allowed for regression")
			sys.exit(1)
		if len(TSobj) != self.records:
			raise excpt.SVDLengthException(len(TSobj),self.records)
		rval = self.standardize().data * TSobj.center().data
		return Numeric.add.reduce(rval)/self.frecords

	def __getitem__(self,idx):
		"Index access to internal data"
		return self.data[idx] 

	def __getslice__(self,idx1,idx2):
		"Slice access to internal data"
		return self.data[idx1:idx2]

	def __len__(self):
		"Lenght of the internal data"
		return len(self.data)
