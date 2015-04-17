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
import numpy
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
        try:
            oldshape = arraynd.shape
        except AttributeError:
	    arraynd = numpy.array(arraynd)
	    oldshape = arraynd.shape
	if spacelast:
		taillen = numpy.multiply.reduce(oldshape[1:])
		arraynd = arraynd.reshape((oldshape[0], taillen))
	else:
		headlen = numpy.multiply.reduce(oldshape[:-1])
		arraynd = arraynd.reshape((headlen, oldshape[-1]))
	return arraynd, oldshape

def deunshape(array2d, oldshape):
	"""Recover the dimensions of an <unshape()>-ed array.

  Arguments:

    'array2d' -- 2-dimensional array which dimensions are to be recovered.

    'oldshape' -- The shape (a tuple) the array must be returned with.

  Returns the array with the specified shape.
  """
	array2d = numpy.array(array2d)
	array_reshaped = array2d.reshape(oldshape)
	return array_reshaped

def checkvalidnans(data):
    """Check that NaNs or mask in a dataset are valid for SVD.

    NaNs can only exist for all samples of a given channel. Data may be
    masked or simply have nans.

    Arguments:
    data -- dataset to check.

    Returns:
    has_nan -- True if data has NaNs in it.
    """
    try:
        nan_values = data.mask
        nan_values = numpy.isnan(data.data)|nan_values
    except AttributeError:
        nan_values = numpy.isnan(data)
    has_nan = numpy.invert(numpy.all(nan_values==False))
    if has_nan:
        nans_in_channel = nan_values.any(axis=0)
        all_are_nan = nan_values.all(axis=0)
        channel_valid = nans_in_channel==all_are_nan
        if not channel_valid.all():
            invalid_channels = numpy.where(channel_valid==False)
            raise InvalidNaNs(invalCid_channels)
    return has_nan

def removenans(data):
    """Removes columns that have valid NaNs from an unshaped array.

    unshape() and checkvalidnans() MUST be applied before using this function.

    Arguments:
    data -- unshaped array. May be a masked array or simply have NaNs.

    Returns:
    no_nan_data -- array withot NaNs.
    no_nan_cols -- columns that were not removed from the original matrix.
    """
    try:
        no_nan_cols = numpy.where(data.mask.any(axis=0)==False)[0]
    except AttributeError:
        no_nan_cols = numpy.where(numpy.isnan(data).any(axis=0)==False)[0]
    no_nan_data = data[:,no_nan_cols]
    return no_nan_data, no_nan_cols

def restorenans(data, shape, cols):
    """Restores nans to an array.

    Arguments:
    data -- input array.
    shape -- shape of output array.
    cols -- columns where data exists.

    Returns:
    with_nans -- data with NaNs.
    """
    with_nans = numpy.ma.ones(shape)*numpy.nan
    with_nans[cols,:] = data
    return with_nans

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
	percentlbd = 100*lbd/numpy.add.reduce(lbd)
	underlimit = numpy.less_equal(
		numpy.add.accumulate(percentlbd), 
		float(percent)
	)
	return 1 + numpy.add.reduce(underlimit)

def correlation(xt, yt):
	"Returns the correlation of arrays"
	xanom = xt - numpy.add.reduce(xt)/len(xt)
	yanom = yt - numpy.add.reduce(yt)/len(yt)
	xstd = xanom / numpy.sqrt(numpy.add.reduce(xanom * xanom)) 
	ystd = yanom / numpy.sqrt(numpy.add.reduce(yanom * yanom))
	return numpy.dot(xstd, ystd) 

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
	avea = numpy.add.reduce(xa)/float(na)
	aveb = numpy.add.reduce(xb)/float(nb)
	xa = xa - avea
	xb = xb - aveb
	stder = numpy.add.reduce(xa*xa) + numpy.add.reduce(xb*xb)
	stder = stder * (1.0/na + 1.0/nb ) / float(dof)
	stder = numpy.sqrt(stder)
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
	lowmask = numpy.less(thets, tlow)
	highmask = numpy.greater(thets, thigh)
	return numpy.logical_or(lowmask,highmask)

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
	avea = numpy.add.reduce(xa)/float(na)
	aveb = numpy.add.reduce(xb)/float(nb)
	vara = numpy.add.reduce((xa-avea)*(xa-avea))/float(na)
	varb = numpy.add.reduce((xb-aveb)*(xb-aveb))/float(nb)
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
	lowmask = numpy.less(thefs, flow)
	highmask = numpy.greater(thefs, fhigh)
	return numpy.logical_or(lowmask,highmask)

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
		self.data = numpy.array(seq)
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
		sdata = numpy.sort(self.data,0)
		return numpy.absolute(
			sdata[(self.records*3)/4]
			- sdata[self.records/4]
		) 

	def max(self):
		"Maximum"
		sdata = numpy.sort(self.data,0)
		return sdata[-1]
	
	def median(self):
		"Median"
		sdata = numpy.sort(self.data,0)
		return sdata[self.records/2]
	
	def min(self):
		"Minimum"
		sdata = numpy.sort(self.data,0)
		return sdata[0]
	
	def q1(self):
		"First quartil"
		sdata = numpy.sort(self.data,0)
		return sdata[self.records/4]
	
	def q3(self):
		"Third quartil"
		sdata = numpy.sort(self.data,0)
		return sdata[(self.records*3)/4]
	
	def mean(self):
		"Mean"
		return numpy.add.reduce(self.data)/self.frecords

	def mad(self):
		"Mean absolute deviation"
		return numpy.add.reduce(numpy.absolute(self.center().data))/self.frecords

	def standardize(self):
		"Standardized version of the TimeSeries object"
		std = self.std()
		mask = numpy.not_equal(std,0)
		maskedstd = std + numpy.logical_not(mask)
		rval = mask * (self.data - self.mean()) / maskedstd
		return TimeSeries(rval)

	def std(self):
		"standard deviation"
		return numpy.sqrt(self.variance())

	def toarray(self):
		"Returns the TimeSeries object internal data as a NumPy array"
		return numpy.array(self.data)

	def variance(self):
		"Variance"
		return numpy.add.reduce(self.center().data * self.center().data)/self.frecords

	def correlation(self, TSobj):
		"Correlation with other TSObject"
		if len(TSobj) != self.records:
			raise excpt.SVDLengthException(len(TSobj),self.records)
		rval = self.standardize().data * TSobj.standardize().data
		return numpy.add.reduce(rval)/self.frecords

	def kurtosis(self):
		"Kurtosis"
		rval = self.data - self.mean()
		rval = rval ** 4.
		rval = numpy.add.reduce(rval) / self.frecords
		rval = rval / (self.variance()**2)
		rval = rval - 3.
		return rval

	def skewness(self):
		rval = self.data - self.mean()
		rval = rval ** 3.
		rval = numpy.add.reduce(rval) / self.frecords
		rval = rval / (numpy.sqrt(self.variance()**3))
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
		return numpy.add.reduce(rval)/self.frecords

	def __getitem__(self,idx):
		"Index access to internal data"
		return self.data[idx] 

	def __getslice__(self,idx1,idx2):
		"Slice access to internal data"
		return self.data[idx1:idx2]

	def __len__(self):
		"Lenght of the internal data"
		return len(self.data)
