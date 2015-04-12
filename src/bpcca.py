# Adapted for numpy/ma/cdms2 by convertcdms.py
# bpcca.py

"""
  Barnett-Preisendorfer Canonical Correlation Analysis.

  This module performs a previous EOF decomposition in order to
  retain only the most important modes and then applies CCA.
  The output are NumPy arrays containing the canonical patterns,
  the expansion coefficients and the correlations.
  For further details and notation:

  Bretherton et al. "An Intercomparison of Methods for Finding Coupled 
  Patterns in Climate Data", Journal of Climate, vol. 5 (1992), p541
"""

# Copyright (C) 2000, Jon Saenz, Jesus Fernandez and Juan Zubillaga

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

# jff20001107

import pyclimate.mvarstatools
import pyclimate.svdeofs 
import pyclimate.tools
import pyclimate.mctest
import pyclimate.NHArray
import pyclimate.pyclimateexcpt
import numpy

ptools = pyclimate.tools
mtools = pyclimate.mvarstatools
SVD = numpy.linalg.svd
NA = numpy.newaxis
def mm(array1,array2):
  return numpy.matrix(array1)*numpy.matrix(array2)

class BPCCA:
  MCTESTMASK_NBINS_DIVISOR = 10
  MCTESTMASK_RANGE_EXTENSION = 0.30
  def __init__(self, leftfield, rightfield, retainedeofs=None):
    """BPCCA constructor.

    Parameters:

      'leftfield' -- One of the fields (say left) entering the CCA
                     computation (Numpy array). Time is assumed to be 
                     its first dimension. The rest are kept as they are.

      'rightfield' -- The other field (say right). The first dimension
                      must be the same size as that in 'leftfield'.

      'retainedeofs' -- Tuple with two elements containing the number of
                        EOFs (*see module* 'svdeofs') to retain in the left
                        and right fields. If not provided, those retaining 
                        70% of the total field variance are selected.

    Atributes:

      The BPCCA object provides the following accesible atributes.
      They are only suposed to be accesible for obtaining aditional info,
      altering their values could be dangerous:

      'sPCA' -- Is s 'SVDEOFs' object with the PCA analysis of the left field.

      'zPCA' -- Idem for right field.
                      
    """
    self.s = leftfield
    self.z = rightfield
    self.retainedeofs = retainedeofs
    self.records = len(leftfield)
    self.sfield2d = len(leftfield.shape)==2
    if not self.sfield2d:
      leftfield, self.oldsshape = ptools.unshape(leftfield)
    self.zfield2d = len(rightfield.shape)==2
    if not self.zfield2d:
      rightfield, self.oldzshape = ptools.unshape(rightfield)
    # First the PCA pre-filter
    self.sPCA = pyclimate.svdeofs.SVDEOFs(numpy.array(leftfield, 'd'))
    self.zPCA = pyclimate.svdeofs.SVDEOFs(numpy.array(rightfield, 'd'))
    # Restriction to an EOFs subspace...
    if not retainedeofs:
      self.n1 = ptools.getneofs(self.sPCA.eigenvalues()) 
      self.n2 = ptools.getneofs(self.zPCA.eigenvalues())
    else:
      self.n1 = retainedeofs[0]
      self.n2 = retainedeofs[1]
    self.n0 = min(self.n1,self.n2)
    pcs = self.sPCA.pcs(1)[:,:self.n1]        # t x n1
    pcz = self.zPCA.pcs(1)[:,:self.n2]        # t x n2
    lbds = self.sPCA.eigenvalues()[:self.n1]  # n1
    lbdz = self.zPCA.eigenvalues()[:self.n2]  # n2
    eofs = self.sPCA.eofs(1)[:,:self.n1]      # ns x n1
    eofz = self.zPCA.eofs(1)[:,:self.n2]      # nz x n2
    covpcsz = mm(numpy.transpose(pcs), pcz)/float(len(pcs))
    self.left, self.corr, t_right = SVD(covpcsz,full_matrices=0)
    self.right = numpy.transpose(t_right)
    # Obtaining the patterns and coefficients...
    self.p_adjoint = mm(eofs/lbds[NA,:], self.left)     # ns x n0
    self.q_adjoint = mm(eofz/lbdz[NA,:], self.right)    # nz x n0
    self.p = mm(eofs, self.left)                        # ns x n0
    self.q = mm(eofz, self.right)                       # nz x n0
    self.a = mm(pcs, self.left)                         # t  x n0
    self.b = mm(pcz, self.right)                        # t  x n0

  def reconstructedFields(self, nccps):
    "Reconstructs the original fields with the desired number ('nccps') of canonical patterns"
    if nccps > self.n0:
      raise pyclimate.pyclimateexcpt.TooBigIntParameter("nccps",nccps,self.n0)
    srval = mm(self.a[:,:nccps], numpy.transpose(self.p[:,:nccps]))
    zrval = mm(self.b[:,:nccps], numpy.transpose(self.q[:,:nccps]))
    if not self.sfield2d: srval.shape = self.oldsshape
    if not self.zfield2d: zrval.shape = self.oldzshape
    return srval, zrval

  def varianceFractions(self):
    "Returns a tuple with the left and right patterns explained variance fraction"
    vars = numpy.add.reduce(numpy.multiply(self.p,self.p))
    varz = numpy.add.reduce(numpy.multiply(self.q,self.q))
    return (
      vars / self.sPCA.totalAnomalyVariance(), 
      varz / self.zPCA.totalAnomalyVariance()
    )

  def leftPatterns(self):
    "Returns (along the _last_ dimension) the left canonical patterns"
    if self.sfield2d:
      return numpy.array(self.p)
    else:
      return ptools.deunshape(self.p, self.oldsshape[1:]+self.p.shape[-1:])

  def rightPatterns(self):
    "Returns (along the _last_ dimension) the right canonical patterns"
    if self.zfield2d:
      return numpy.array(self.q)
    else:
      return ptools.deunshape(self.q, self.oldzshape[1:]+self.q.shape[-1:])

  def leftAdjointPatterns(self):
    "Returns (along the _last_ dimension) the left adjoint canonical patterns"
    if self.sfield2d:
      return numpy.array(self.p_adjoint)
    else:
      return ptools.deunshape(
        self.p_adjoint, 
        self.oldsshape[1:] + self.p_adjoint.shape[-1:]
      )

  def rightAdjointPatterns(self):
    "Returns (along the _last_ dimension) the right adjoint canonical patterns"
    if self.zfield2d:
      return numpy.array(self.q_adjoint)
    else:
      return ptools.deunshape(
        self.q_adjoint, 
        self.oldzshape[1:] + self.q_adjoint.shape[-1:]
      )

  def leftExpCoeffs(self):
    "Returns the left temporal expansion coefficients"
    return numpy.array(self.a)

  def rightExpCoeffs(self):
    "Returns the right temporal expansion coefficients"
    return numpy.array(self.b)

  def correlation(self):
    "Returns the canonical correlation values"
    return numpy.array(self.corr)

  def EOFspaceLeftPatterns(self):
    "Returns the left canonical patterns in EOF coordinates"
    return numpy.array(self.left)

  def EOFspaceRightPatterns(self):
    "Returns the right canonical patterns in EOF coordinates"
    return numpy.array(self.right)

  def MCTestMask(self,subsamples,length,prob=0.95,nbins=None,verbose=0):
    """Significance masks for the canonical patterns obtained through a Monte Carlo test.

    Parameters:

      'subsamples' -- Number of Monte Carlo subsamples to take

      'lenght' -- Length of each subsample (obviously less than the total
                  number od time records)

    Optional parameters:

      'prob' -- Significance level

      'nbins' -- Number of bins the histogramam range is divided. Defaults
                 to a number ensuring 10 subsamples per bin.
      
      'verbose' -- If set to true (non-zero value), a counter is dumped
                   to stdout to follow the runs of the test. Defaults to 0.

    Returns a tuple with the left and right masks with the significant
    grid points of the canonical patterns.
    
    The range for the histograms is calculated from the range of the 
    *master* canonical patterns by extending it a 30%. This extension
    can be controled by the class attribute MCTESTMASK_RANGE_EXTENSION
    which is set by default to 0.30
    """
    ldim = self.p.shape[0] * self.n0
    rdim = self.q.shape[0] * self.n0
    nbins = nbins or subsamples / self.MCTESTMASK_NBINS_DIVISOR
    # Initializing left numerical histogram array
    xlow = min(numpy.ravel(self.p))
    xup = max(numpy.ravel(self.p))
    extens = (xup-xlow) * self.MCTESTMASK_RANGE_EXTENSION    
    xlow = xlow - extens
    xup = xup + extens
    lnha = pyclimate.NHArray.NHArray(xlow, xup, nbins, ldim)
    # Initializing right numerical histogram array
    xlow = min(numpy.ravel(self.q))
    xup = max(numpy.ravel(self.q))
    extens = (xup-xlow) * self.MCTESTMASK_RANGE_EXTENSION    
    xlow = xlow - extens
    xup = xup + extens
    rnha = pyclimate.NHArray.NHArray(xlow, xup, nbins, rdim)
    if verbose: print "Monte Carlo test (%d runs)" % subsamples
    for isample in xrange(subsamples):
      if verbose and not isample % (subsamples/20): 
        print "  %d more runs to go..." % (subsamples-isample,)
      sublist = pyclimate.mctest.getrandomsubsample(length,self.records)
      subbpcca = BPCCA(
        numpy.take(self.s,sublist), 
        numpy.take(self.z,sublist),
        self.retainedeofs
      )
      congrusign = mtools.congruence(subbpcca.p, self.p)
      congrusign = -1 * numpy.less(congrusign,0) + numpy.greater(congrusign,0)
      lnha.Update(numpy.ravel(subbpcca.p * congrusign[NA,:]))
      rnha.Update(numpy.ravel(subbpcca.q * congrusign[NA,:]))
    lthres = lnha.GetRange(prob) 
    rthres = rnha.GetRange(prob) 
    ldelta = lnha.GetDeltaX()
    rdelta = lnha.GetDeltaX()
    rp = numpy.ravel(self.p)
    # the mask interval is stripped by [lr]delta to be conservative
    lmask = numpy.greater(numpy.ravel(self.p), lthres[:,0]+ldelta)
    lmask = lmask * numpy.less(numpy.ravel(self.p), lthres[:,1]-ldelta)
    rmask = numpy.greater(numpy.ravel(self.q), rthres[:,0]+rdelta)
    rmask = rmask * numpy.less(numpy.ravel(self.q), rthres[:,1]-rdelta)
    for i in range(len(numpy.ravel(self.p))):
      print "%7.2f <%7.2f> %7.2f | %d" % (lthres[i,0], rp[i],lthres[i,1], lmask[i])
    if not self.sfield2d:
      theshape = self.oldsshape[1:] + (self.n0,)
      print theshape
      lmask.shape = theshape
    else:
      theshape = (self.p.shape[0], self.n0)
      print theshape
      lmask.shape = theshape
    if not self.zfield2d:
      theshape = self.oldzshape[1:] + (self.n0,)
      print theshape
      rmask.shape = theshape
    else:
      theshape = (self.q.shape[0], self.n0)
      print theshape
      rmask.shape = theshape
    return lmask, rmask



  def MCTest(self,subsamples,length):
    """Monte Carlo test for the temporal stability of the canonical patterns.

    Parameters:

      'subsamples' -- Number of Monte Carlo subsamples to take

      'lenght' -- Length of each subsample (obviously less than the total
                  number od time records)

    Returns a tuple with the left and right NumPy arrays containing in each
    row the congruence coefficient of each subsample obtained patterns with 
    those obtained for the whole dataset.
    """
    theleftccoefs = numpy.zeros((subsamples,)+(self.n0,), 'd')  
    therightccoefs = numpy.zeros((subsamples,)+(self.n0,), 'd')  
    for isample in xrange(subsamples):
      sublist = pyclimate.mctest.getrandomsubsample(length,self.records)
      subbpcca = BPCCA(
        numpy.take(self.s,sublist), 
        numpy.take(self.z,sublist),
        self.retainedeofs
      )
      if self.n0 != 1:
        theleftccoefs[isample,:] = mtools.congruence(subbpcca.p, self.p)
        therightccoefs[isample,:] = mtools.congruence(subbpcca.q, self.q)
      else:
        theleftccoefs[isample,0] = mtools.congruence(subbpcca.p, self.p)[0]
        therightccoefs[isample,0] = mtools.congruence(subbpcca.q, self.q)[0]
    return theleftccoefs, therightccoefs

  def MCTestCorrelation(self, samples):
    """Monte Carlo test for the significance of the canonical correlations.

    The input data are randomly temporally disordered and CCA is performed
    obtaining a distribution of canonical correlations due to non actually
    correlated fields but (inherently with the same probability distribution
    as the original ones)

    Parameters:

      'samples' -- Number of Monte Carlo subsamples to take

    Returns a Numpy array which columns are the different canonical 
    correlations for each MC run.
    """
    thecorrs = numpy.zeros((samples,)+(self.n0,), 'd')  
    for isample in xrange(samples):
      sublists = numpy.random.permutation(self.records)
      sublistz = numpy.random.permutation(self.records)
      subbpcca = BPCCA(
        numpy.take(self.s,sublists), 
        numpy.take(self.z,sublistz),
        self.retainedeofs
      )
      if self.n0 != 1:
        thecorrs[isample,:] = subbpcca.corr[:]
      else:
        thecorrs[isample,0] = subbpcca.corr[:]
    return thecorrs

################################################################
# Backward compatibility function names. It's advisable to use #
# the new ones.                                                #
################################################################
  getvariancefractions = varianceFractions                     #
  getVarianceFractions = varianceFractions                     #
  leftpatterns = leftPatterns                                  #
  rightpatterns = rightPatterns                                #
  leftexpcoeffs = leftExpCoeffs                                #
  rightexpcoeffs = rightExpCoeffs                              #
                                                               #
bpcca = BPCCA                                                  #
################################################################
