# Adapted for numpy/ma/cdms2 by convertcdms.py
# svdeofs.py

"""EOF decomposition based on SVD

  Given a dataset as read from readdat, that is, a matrix NxM, with N the
  number of samples and M the number of channels or spatial samples, these
  functions and classes compute the unrotated EOF decomposition of the field, 
  the principal components and some utility routines.

  For better stability the computations are carried out by means of singular
  value decomposition.

"""
# 
# Copyright (C) 2000, Jon Saenz, Jesus fernandez and Juan Zubillaga
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
import pyclimate.pydcdflib
import pyclimate.mctest
import pyclimate.mvarstatools
import pyclimate.pyclimateexcpt
import pyclimate.tools
import sys

NA = numpy.newaxis
def mm(array1,array2):
  print 'mming:',array1.shape,array2.shape
  return numpy.matrix(array1)*numpy.matrix(array2)
SVD = numpy.linalg.svd
ptools = pyclimate.tools
pmvstools = pyclimate.mvarstatools
mctest = pyclimate.mctest
pex = pyclimate.pyclimateexcpt

# Derive the EOFs from a dataset by means of the SVD decomposition of the
# data matrix (See Jackson, 1991 and Preisendorfer, 1987), avoiding the
# problems associated to a singular correlation matrix
# dataset is an nxm array of data.
# n (rows) -> Samples
# m (columns) -> Data channels
# If p=min(n,m) the output dimensions are: pcs(nxp)
#                                          L  (pxp)
#                                          E  (mxp)
def svdeofs(dataset, pcscaling=0):
  """Calculates de EOF decomposition of a field.
  
  Arguments:

    'dataset' -- NumPy array containing the field to be decomposed. 
                 First dimension must be time.

    'pcscaling' -- sets the scale factor of the PCs: 0 means eigenvalues 
                   are PC variances and the EOFs are orthonormal. 1 means 
                   PCs with unit variance and orthogonal EOFs. (Defaults to 0)

  Returns a tuple containing: PCs, eigenvalues, EOFs

  If the field has more than one spatial dimension it can be processed anyway
  and each EOF can be recovered as *generalized columns*: EOFs[..., eofnumber]
  """
  residual = pmvstools.center(dataset)
  field2d = len(dataset.shape)==2
  if not field2d:
    residual, oldshape = ptools.unshape(residual)
  newshape = residual.shape
  has_nan = ptools.checkvalidnans(residual)
  if has_nan:
      residual, cols = ptools.removenans(residual)
  A,Lh,E = SVD(residual,full_matrices=0)
  # The eigenvalues from SVD routines are powered to 1/2, thus: square
  # the vector.
  # Moreover, in order to be able to compare these eigenvalues to the 
  # ones obtained from the direct eigenvalue problem with a non-singular
  # covariance matrix (i.e. dsyev() LAPACK routine),
  # the eigenvalues have to be divided by a 
  # constant factor, the number of the elements in the time series.
  # This way, the eigenvalues are variances!!
  # (Defined not taking into account that the centered data has 
  # one degree of freedom less)
  # First BUG Fixed (JFF 20001115):
  # A "-1" appeared here before version 1.1
  # (it has been removed for consistency)
  normfactor = float(len(residual))
  L = Lh*Lh/normfactor
  # E is returned transposed
  E = numpy.transpose(E)
  pcs = A*Lh
  if pcscaling == 0:
    # E orthonormal
    # pc variances are the eigenvalues L
    pass
  elif pcscaling == 1:
    # E orthogonal but not orthonormal
    # unity pc variances
    print E.shape,L.shape
    E = E * numpy.sqrt(L)[NA,:]
    pcs = pcs / numpy.sqrt(L)[NA,:]
  else:
    raise pex.ScalingError(pcscaling)
  if has_nan:
    E = ptools.restorenans(E, (newshape[1],E.shape[-1]), cols)
  if not field2d:
    E = ptools.deunshape(E, oldshape[1:]+E.shape[-1:])
  return pcs,L,E

def getgencol(a, ncol=0):
  return a[...,ncol]

def pcseriescorrelation(pcs, eofs, dataset):
  """\
  Calculates the correlation between the PCs and time series at each grid point.

  Arguments:

    'pcs' -- the PCs as returned by 'svdeofs'

    'eofs' -- the EOFs as returned by 'svdeofs'

    'dataset' -- the dataset

  Returns an array which *generalized columns* are the correlation fields of the
  original time series with each PC.
  """
  residual = pmvstools.center(dataset)
  datastd = numpy.add.reduce(residual*residual) / float(len(residual))
  datastd = numpy.sqrt(datastd)
  pcsstd = numpy.sqrt(numpy.add.reduce(pcs*pcs) / float(len(pcs)))
  return eofs * pcsstd / datastd[...,NA] 

def eofsasexplainedvariance(eofs,pcscaling=0,lambdas=None):
  #e# NewAxis y multidimensionalidad ALTAMENTE DUDOSA
  if pcscaling and not lambdas:
    print "The lambdas must be provided to"
    print "pyclimate.svdeofs.eofsasexplainedvariance(eofs,pcscaling,lambdas)"
    print "if the pcscaling is set to 1."
    sys.exit(1)
  if pcscaling == 0:
    rval = eofs * eofs
  if pcscaling == 1:
    rval = eofs * eofs * lambdas[NA,:] 
  if not pcscaling in [0,1]:
    raise pex.ScalingError(pcscaling)    
  totvar = numpy.add.reduce(rval, -1)
  return rval / totvar[...,NA]

def getvariancefraction(lambdas):
  return lambdas/numpy.add.reduce(lambdas)

def bartletttest(lambdas,samples):
  p = len(lambdas)
  theshape = (p-1,)
  chis = numpy.zeros(theshape,'d')
  pchis = numpy.zeros(theshape,'d')
  nu = samples - 1
  # This test will fail when lambda[i]<=0!!!
  mask = numpy.less_equal(lambdas,0.0)
  maskedlambdas = lambdas * numpy.logical_not(mask) + mask
  loglambdas = numpy.log(maskedlambdas)
  for k in xrange(p-1):
    cdf = .5*(p-k-1)*(p-k+2)
    if mask[k] == 1:
      # "Transformed" eigenvalues, set a probability of 1
      pchis = pchis * numpy.logical_not(mask) + mask
      chis[k] = 0.0
    else:
      chis[k] = nu * (
        (p-k) * numpy.log(numpy.add.reduce(maskedlambdas[k:])/(p-k))
        - numpy.add.reduce(loglambdas[k:])
      )
      pchis[k] = getchiprob(chis[k],cdf)
  return (chis,pchis)

def getchiprob(chival,dof):
  chi = pyclimate.pydcdflib.CDFChi()
  chi.which = 1
  chi.status = 0
  chi.x = float(chival)
  chi.df = dof
  pyclimate.pydcdflib.pycdfchi(chi)
  if chi.status == 0:
    prob = chi.p
  else:
    prob = 0
  return prob


def northtest(lambdas,tsamples):
  factor = numpy.sqrt(2./tsamples)
  errors = numpy.array(lambdas)*factor
  return errors

def mctesteofs(dataset,eofs,subsamples,length):
  """Monte Carlo test for the stability of the EOFs

  def mctesteofs(dataset,eofs,subsamples,length):  

  Test the leading master EOFs obtained from the complete sample and
  input in eofs by means of a Monte Carlo test based on making
  *subsamples* subsamples with *length* members in each 
  """
  eofnumber = eofs.shape[-1]
  theccoefs = numpy.zeros((subsamples,)+(eofnumber,),'d')
  for isample in xrange(subsamples):
    subslist = mctest.getrandomsubsample(length,len(dataset))
    subsample = numpy.take(dataset,subslist,0)
    z, lambdas, eofdot = svdeofs(subsample)
    for ieof in xrange(eofnumber):
      theccoefs[isample,ieof] = pmvstools.congruence(
          numpy.ravel(eofdot[...,ieof]),
          numpy.ravel(eofs[...,ieof])
      )
  return theccoefs

###########################################
# New class implementation of the EOF routines...
####################################################
class SVDEOFs:
  "Class implementation of the EOF routines"
  def __init__(self, dataset):
    """Contructor for 'SVDEOFs'

    Argument:

      'dataset' -- NumPy array containing the data to be decomposed. Time
                   must be the first dimension. Several channel dimensions 
                   are supported.
    """
    self.dataset = dataset
    self.originalshape = dataset[0].shape
    self.channels = numpy.multiply.reduce(numpy.array(self.originalshape))
    self.records = len(dataset)
    self.field2d = len(dataset.shape)==2
    residual = pmvstools.center(dataset)
    if not self.field2d:
      residual = ptools.unshape(residual)[0]
    newshape = residual.shape
    has_nan = ptools.checkvalidnans(residual)
    if has_nan:
        residual, cols = ptools.removenans(residual)
    A,Lh,E = SVD(residual,full_matrices=0)
    normfactor = float(len(residual))
    self.L = self.lambdas = Lh*Lh/normfactor
    self.neofs = len(self.L)
    self.flatE = numpy.transpose(E)
    if has_nan:
        self.flatE = ptools.restorenans(self.flatE,
                (newshape[1],self.flatE.shape[-1]), cols)
    self.E = ptools.deunshape(self.flatE, self.originalshape+(self.neofs,))
    self.P = A*Lh

  def pcs(self, pcscaling=0):
    """Returns the principal components as the columns of an array

    Optional argument:

      'pcscaling' -- Sets the scaling of the PCs. Set to 1 for standardized 
                     PCs. Defaults to 0.
    """
    if pcscaling == 0:
      # pc variances are the eigenvalues L
      return numpy.array(self.P)
    elif pcscaling == 1:
      # unity pc variances
      return self.P / numpy.sqrt(self.L)[NA,:]
    else:
      raise pex.ScalingError(pcscaling)
      sys.exit(1)

  def eofs(self, pcscaling=0):
    """Returns the empirical orthogonal functions

    Optional argument:

      'pcscaling' -- Sets the scaling of the EOFs. Set to 0 for orthonormal
                     EOFs. Set to 1 for non-dimensional EOFs. Defaults to 0.
    """
    if pcscaling == 0: 
      # E orthonormal
      if not self.field2d:
        return numpy.array(self.E)
      else:
        return numpy.array(self.flatE)
    if pcscaling == 1:
      # E orthogonal but not orthonormal
      rval = self.flatE * numpy.sqrt(self.L)[NA,:]
      if not self.field2d:
        return ptools.deunshape(rval, self.originalshape+(self.neofs,)) 
      else:
        return rval
    else:
      raise pex.ScalingError(pcscaling)
      sys.exit(1)
 
  def eigenvalues(self):
    "The decreasing variances associated to each EOF"
    return numpy.array(self.lambdas)

  def eofsAsCorrelation(self):
    "The EOFs scaled as the correlation of the PC with the original field"
    residual = pmvstools.center(self.dataset)
    datastd = numpy.add.reduce(residual*residual)/float(self.records)
    datastd = numpy.sqrt(datastd)
    pcsstd = numpy.add.reduce(self.P*self.P)/float(self.records)
    pcsstd = numpy.sqrt(pcsstd)
    return self.E * pcsstd / datastd[...,NA] 

  def eofsAsExplainedVariance(self):
    "The EOFs scaled as fraction of explained variance of the original field"
    #e# NewAxis y multidimensionalidad ALTAMENTE DUDOSA
    rval = self.E * self.E 
    totvar = numpy.add.reduce(rval, -1)
    return rval/totvar[...,NA]

  def varianceFraction(self):
    "The fraction of the total variance explained by each principal mode"
    return self.lambdas/numpy.add.reduce(self.lambdas)

  def totalAnomalyVariance(self):
    "The total variance associated to the field of anomalies"
    return numpy.add.reduce(self.lambdas)

  def reconstructedField(self, neofs):
    "Reconstructs the original field using 'neofs' EOFs"
    rval = mm(self.P[:,:neofs], numpy.transpose(self.flatE[:,:neofs]))
    rval.shape = self.dataset.shape
    return rval

  def unreconstructedField(self,neofs,X=None):
    """Returns the part of the field NOT reconstructed by 'neofs' EOFs

    Argument:

      'neofs' -- number of EOFs for reconstructing the field

    Optional argument:

      'X' -- The field to try to reconstruct. Defaults to the data field
             used to derive the EOFs.
    """
    myX = X or self.dataset
    rval = self.projectField(neofs, myX)
    rval = myX - mm(rval, numpy.transpose(self.flatE[:,:neofs]))
    return rval

  def projectField(self,neofs,X=None):
    "Projects a field 'X' onto the 'neofs' leading EOFs returning its coordinates in the EOF-space"
    myX = X or self.dataset
    Xdot, oshape = ptools.unshape(myX)
    return mm(Xdot[:,:],self.flatE[:,:neofs])

  def bartlettTest(self):
    """Performs the Bartlett test on the last p-k eigenvalues

    It is a test on the last p-k eigenvalues being the same. It relies
    on the statistic:

    '                                      / SUM lambda_j \      '     

    '  -nu SUM log(lambda_j) + nu(p-k) log| -------------- |     '

    '                                      \    p - k     /      '

    (SUMmation goes from j=k+1 to p) that is supposed to be distributed
    following the chi square distribution with nu=(p-k+1)(p-k+2)/2 degrees 
    of freedom.

    This method returns a tuple (chi,chiprob) with:

      'chi' -- A NumPy array with the Bartlett statistic for k = 1 to p.
               (length: p-1)

      'chiprob' -- the probability associated to that 'chi' value
    """
    p = self.neofs
    theshape = (p-1,)
    chis = numpy.zeros(theshape,'d')
    pchis = numpy.zeros(theshape,'d')
    nu = self.records-1
    # This test will fail when lambda[i]<=0!!!
    mask = numpy.less_equal(self.lambdas,0.0)
    maskedlambdas = self.lambdas*numpy.logical_not(mask)+mask
    loglambdas = numpy.log(maskedlambdas)
    for k in xrange(p-1):
      cdf = .5*(p-k-1)*(p-k+2)
      if mask[k] == 1:
        # "Transformed" eigenvalues, set a probability of 1
        pchis = pchis*numpy.logical_not(mask)+mask
        chis[k] = 0.0
      else:
        chis[k] = nu*((p-k)* \
          numpy.log(numpy.add.reduce(maskedlambdas[k:])/(p-k)) \
          -numpy.add.reduce(loglambdas[k:]))
        pchis[k] = getchiprob(chis[k],cdf)
    return (chis,pchis)

  def northTest(self):
    """Performs the North test returning the estimated sampling errors

    Details:

      North et al. (1982) *Sampling errors in the estimation of empirical
      orthogonal functions*, Monthly Weather Review 110:699-706
    """
    factor = numpy.sqrt(2.0/self.records)
    errors = numpy.array(self.lambdas)*factor
    return errors

  def MCTest(self,subsamples,length,neofs=None):
    """Monte Carlo test for the temporal stability of the EOFs.

    Parameters:

      'subsamples' -- Number of Monte Carlo subsamples to take

      'lenght' -- Length of each subsample (obviously less than the total
                  number od time records)

    Optional parameters:

      'neofs' -- Number of EOFs to perform the test on. Defaults to the
                 number selected by a 70% variance stopping rule (*See*
                 'pyclimate.tools.getneofs').

    Returns a NumPy array containing in each row the congruence coefficient of
    each subsample obtained patterns with those obtained for the whole dataset.
    """
    neofs = neofs or ptools.getneofs(self.lambdas)
    theccoefs = numpy.zeros((subsamples,neofs),'d')
    for isample in xrange(subsamples):
      subslist = mctest.getrandomsubsample(length,self.records)
      SVDEOFsobj = SVDEOFs(numpy.take(self.dataset,subslist))
      eofdot = SVDEOFsobj.eofs()[...,:neofs]
      thiseofs = self.eofs()[...,:neofs]
      for ieof in xrange(neofs):
        theccoefs[isample,ieof] = pmvstools.congruence(
          eofdot[...,ieof],thiseofs[...,ieof]
        )
    return theccoefs

if __name__ == "__main__":
  # Testing the equality of the new object oriented EOF calculus
  # and the old one.
  import pyclimate.asciidat
  def RMS(a,b):
    c = a-b
    c = c*c
    c = numpy.ravel(c)
    c = numpy.add.reduce(c)
    c = numpy.sqrt(c)
    return c
  print "Testing new class: SVDEOFs"
  print "--------------------------"
  dataset2d = pyclimate.asciidat.readdat("../test/chemical.dat")
  print "2D example"
  print "----------"
  p,l,e = svdeofs(dataset2d,0)
  P,L,E = svdeofs(dataset2d,1)
  EOFobj = SVDEOFs(dataset2d)
  print "RMS PCs scaling 0 : %f" % RMS(p, EOFobj.pcs())
  print "RMS PCs scaling 1 : %f" % RMS(P, EOFobj.pcs(1))
  print "RMS EOFs scaling 0: %f" % RMS(e, EOFobj.eofs())
  print "RMS EOFs scaling 1: %f" % RMS(E, EOFobj.eofs(1))
  print "RMS lambdas ......: %f" % RMS(l, EOFobj.lambdas)
  dataset3d = numpy.reshape(dataset2d,(5,3,2))
  print "3D example"
  print "----------"
  p,l,e = svdeofs(dataset3d,0)
  P,L,E = svdeofs(dataset3d,1)
  EOFobj = SVDEOFs(dataset3d)
  print "RMS PCs scaling 0 : %f" % RMS(p, EOFobj.pcs())
  print "RMS PCs scaling 1 : %f" % RMS(P, EOFobj.pcs(1))
  print "RMS EOFs scaling 0: %f" % RMS(e, EOFobj.eofs())
  print "RMS EOFs scaling 1: %f" % RMS(E, EOFobj.eofs(1))
  print "RMS lambdas ......: %f" % RMS(l, EOFobj.lambdas)

# jff20011005
