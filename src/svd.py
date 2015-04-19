# Adapted for numpy/ma/cdms2 by convertcdms.py
# svd.py

"""SVD decomposition of two fields

"""
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
# 

import numpy
import sys
import pyclimate.mvarstatools
import pyclimate.pyclimateexcpt
import pyclimate.mctest
import pyclimate.tools
#import whrandom


mt=pyclimate.mvarstatools
excpt=pyclimate.pyclimateexcpt
mctest=pyclimate.mctest
tools=pyclimate.tools
def mm(array1,array2):
  return numpy.matrix(array1)*numpy.matrix(array2)

def svd(sfield,zfield):
	"""Given two fields, get the SVD of their covariance matrix.

  Arguments:

    'sfield' -- Input left field

    'zfield' -- Input right field

  Returns a tuple (P,S,Q) with:

    'P' -- The left singular vectors.
 
    'S' -- The covariance of each of the modes.

    'Q' -- The right singular vectors
	"""
    if len(sfield)!=len(zfield):
	raise excpt.SVDLengthException(len(sfield),len(zfield))
    sfield2d = len(sfield.shape)==2
    if not sfield2d:
        sfield, oldsshape = tools.unshape(sfield)
    snewshape = leftfield.shape
    shas_nan = tools.checkvalidnans(leftfield)
    if shas_nan:
        leftfield, scols = tools.removenans(leftfield)
    zfield2d = len(zfield.shape)==2
    if not zfield2d:
        zfield, oldzshape = tools.unshape(zfield)
    znewshape = rightfield.shape
    zhas_nan = tools.checkvalidnans(rightfield)
    if zhas_nan:
        rightfield, zcols = ptools.removenans(rightfield)
    csz=mt.covariancematrix(sfield,zfield)
    P,sigma,Qt=numpy.linalg.svd(csz,full_matrices=0)
    Q=numpy.transpose(Qt)
    # Returns:
    # P -> Left singular vectors
    # sigma -> Covariances of each of the modes
    # Q -> Right singular vectors (Already transposed!!!)
    if shas_nan:
        P = tools.restorenans(P, (self.snewshape[1],P.shape[1]), scols)
    if not sfield2d:
        P = tools.deunshape(P, oldsshape[1:]+P.shape[-1:])
    if zhas_nan:
        Q = tools.restorenans(Q, (znewshape[1],Q.shape[1]), zcols)
    if not zfield2d:
    	Q = tools.deunshape(Q, oldzshape[1:]+Q.shape[-1:])
    return P,sigma,Q

def SCF(sigmas):
        """Get the squared covariance fraction of the modes

  Argument:

    'sigmas' -- Covariances returned by svd()

  Returns a numpy array with the Squared covariance fraction
  """
	sigma2=sigmas*sigmas
	totalsc=numpy.add.reduce(sigma2)
	return (sigma2/totalsc)

def CSCF(sigmas):
	"""Cumulative squared covariance fraction

  Argument:

    'sigmas' -- Covariances returned by svd()

  Returns a numpy Array with the Cumulative squared covariance fraction
  """
	return (numpy.add.accumulate(SCF(sigmas)))

def numberofvectors(svectors):
	"""Number of eigenvectors according to our storage rules.

  Arguments:

    'svectors' -- Matrix of eigenvectors returned by svd() (P or Q)
  """
	return svectors.shape[-1]

def getvector(svectors,ivect):
	"""Get the ivect-eth singular vector.

  Arguments:

    'svectors' -- Matrix of eigenvectors returned by svd (P or Q)

    'ivect' -- The order of the eigenvector that must be returned

  Returns the ivect-ieth spatial pattern
  """
	return array(svectors[...,ivect])

def getcoefs(data,svectors):
	"""Temporal expansion coefficients

  Arguments:

    'data' -- Data to project onto the singular vectors, usually
              the same NumPy used to get the vectors.

    'svectors' -- Singular vectors (left or right) as returned by 'svd()'
  """
	coefs=mm(tools.unshape(data)[0], 
		tools.unshape(svectors,0)[0])
	return coefs

def getcoefcorrelations(scoefs, zcoefs):
	"Correlation between the temporal expansion coefficients"
	return numpy.diagonal(mt.correlationmatrix(scoefs, zcoefs))                 

def homogeneousmaps(data,svectors):
	"""Homogeneus correlation maps

  Arguments:

    'data' -- Data to be represented as homogeneous correlation

    'svectors' -- Correspondent singular vectors as returned by 'svd()'
  """
	coefs=getcoefs(data,svectors)
	data, oldshape = tools.unshape(data)
	cdata=mt.standardize(data)
	ccoefs=mt.standardize(coefs)
	themaps=mm(numpy.transpose(cdata),ccoefs)/len(ccoefs)
	themaps = tools.deunshape(themaps, oldshape[1:] + ccoefs.shape[-1:])
	return themaps

# The heterogeneous correlation maps are:
def heterogeneousmaps(xdata,ycoefs):
	"""Heterogeneous correlation maps

  Arguments:

    'xdata' -- Data to be represented as heterogeneous correlation

    'ycoefs' -- Temporal expansion coefs to correlate with 'xdata'. To get
                an heterogeneous map they must be left-'xdata' and right-'ycoefs'
                or right-'xdata' and left-'ycoefs'.
  """
	xdata, oldshape = tools.unshape(xdata)
	cdata=mt.standardize(xdata)
	ccoefs=mt.standardize(ycoefs)
	themaps=mm(numpy.transpose(cdata),ccoefs)/len(cdata)
	themaps = tools.deunshape(themaps, oldshape[1:] + ccoefs.shape[-1:])
	return themaps

def _getsubset(ldata,rdata,ielems):
	seq=mctest.getrandomsubsample(ielems,len(ldata))
        subl=numpy.take(ldata,seq,0)
        subr=numpy.take(rdata,seq,0)
        return subl,subr

def makemctest(Umaster,Vmaster,ldata,rdata,itimes,ielems):
	"""Monte Carlo test on the congruence of the singular vectors

  Arguments:

    'Umaster' -- Left singular vectors as returned by 'svd()'

    'Vmaster' -- Right singular vectors as returned by 'svd()'

    'ldata' -- Left data field

    'rdata' -- Right data field

    'itimes' -- Number of Monte Carlo runs

    'ielems' -- Number of records in each Monte Carlo subsample
  """
	vectors=Umaster.shape[-1]
	if Vmaster.shape[-1]!=vectors:
		raise excpt.SVDSubsetLengthException(vectors,len(Vmaster[0]))
	uccoefs=numpy.zeros((itimes,)+(vectors,),numpy.float64)
	vccoefs=numpy.zeros((itimes,)+(vectors,),numpy.float64)
        for itime in xrange(itimes):
                lsubset,rsubset=_getsubset(ldata,rdata,ielems)
                U,sigma,V=svd(lsubset,rsubset)
		for iv in xrange(vectors):
			uccoefs[itime,iv]=mt.congruence(U[...,iv],Umaster[...,iv])
			vccoefs[itime,iv]=mt.congruence(V[...,iv],Vmaster[...,iv])
	return uccoefs,vccoefs

