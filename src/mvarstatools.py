# Adapted for numpy/ma/cdms2 by convertcdms.py
# mvarstatools.py

"""Some statistical tools used in multivariate analysis

  Utility routines used in several other routines

  WARNING!!!!!

  These routines are designed on the assumption that the input
  dataset is arranged as a matrix NxM, with N=samples and M=channels
  This functions depend critically on the arrangement of the input
  datasets. This order has been chosen due to an easier implementation
  of the code:

  The datasets are arranged as arrays NxM, where N (rows)
  is the number of samples and M (rows in the array)
  is the number of channels (spatial grid cells, for instance)
"""
# Jon Saenz, while at UCLA, 19990816
# 
# Copyright (C) 2000, Jon Saenz, Jesus Fernandez and Juan Zubillaga
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
 
import numpy
import sys
import pyclimate.pyclimateexcpt
import pyclimate.tools

pex=pyclimate.pyclimateexcpt

def mm(array1,array2):
  return numpy.matrix(array1)*numpy.matrix(array2)

def center(dataset):
	"Returns a centered version (mean along _first_ axis removed) of an array"
	theaverage=(numpy.add.reduce(dataset))/float(len(dataset))
	return (numpy.array(dataset)-theaverage)

def standardize(dataset):
	"Standardized (centered and unit variance) version of an array"
	residual=center(dataset)
	std=numpy.sqrt(numpy.add.reduce(residual*residual)/float(len(residual)))
	return numpy.array(residual)/std

def covariancematrix(X,Y):
	"Compute the (S-Mode) covariance matrix of two datasets"
	if len(X)!=len(Y):
		raise pex.MVSTLengthException(len(X),len(Y))
	N=float(len(X))
	cX=center(X)
	cY=center(Y)
	covmat=mm(numpy.transpose(cX),cY)/N
	return covmat

def correlationmatrix(X,Y):
	"Compute the (S-Mode) correlation matrix of two datasets"
	if len(X)!=len(Y):
		raise pex.MVSTLengthException(len(X),len(Y))
	N=float(len(X))
	cX=standardize(X)
	cY=standardize(Y)
	corrmat=mm(numpy.transpose(cX),cY)/N
	return corrmat

def congruence(p1,p2):
	"""Get the congruence coefficient of two spatial patterns

  They must be provided as 1-dimensional arrays. If several
  dimensions are found it returns an array with the congruence
  along the first dimension.
	"""
	norm1=numpy.sqrt(numpy.add.reduce(p1*p1))
	norm2=numpy.sqrt(numpy.add.reduce(p2*p2))
	crossdot=numpy.add.reduce(p1*p2)
	return crossdot/norm1/norm2

def detrend(dataset,tvalues,order=1):
	"""Removes polinomial trends

  Given a linear input dataset, detrend it removing a polynomial of order
  N of type trend(t)=\sum_{i=0}^N a_i t^i

  Arguments:

    'dataset' -- Numpy array with the data to be detrended (along its _first_
                 dimension)

    'tvalues' -- Numpy array with the values of the time coordinate. Its 
                 length must be that of the first dimension of 'dataset'

  Optional arguments:

    'order' -- The order of the polinomial to be removed. Defaults to 1 (linear)

  The function returns the detrended (LINEAR) dataset and
  the parameters of the trend in a tuple.
  Of course, when removing a polynomial of the mentioned type, the
  mean is also removed !!!
	"""
	T=numpy.ones((len(dataset),)+(order+1,),numpy.float64)
	for iord in xrange(1,len(T[0])):
		T[:,iord]=T[:,iord-1]*tvalues
	V=mm(numpy.transpose(T),T)
	Tx=mm(numpy.transpose(T),dataset)
	A=mm(numpy.linalg.inv(V),Tx)
	trendterm=mm(T,A)
	residual=dataset-trendterm
	return residual,A


def totalvariance(field):
	"""Returns the total variance of an array

  Again, variances along the _first_ dimension of the array are calculated
  and the variances obtained are added together.
	"""
        zdot=center(pyclimate.tools.unshape(field)[0])
        var=numpy.add.reduce(numpy.add.reduce(zdot*zdot))/len(zdot)
        return var


