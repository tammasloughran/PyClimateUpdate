# Adapted for numpy/ma/cdms2 by convertcdms.py
# NHArray.py

"""numpy Histogram Array

Multidimensional histogram array to perform Monte Carlo tests for
asessing statistical significance.

"""

# Copyright (C) 2002, Jon Saenz, Jesus Fernandez and Juan Zubillaga
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

import pyclimate.anumhist
import numpy

class NHArray:
  "numpy Histogram Array class"
  def __init__(self, xl, xu, nbins, elems):
    """Constructor for the NHArray class

    Arguments:

      'xl' -- Lower limit for the histograms

      'xu' -- Upper limit for the histograms

      'nbins' -- Number of bins (classes) of the histograms

      'elems' -- Number of histograms to be hold. Usually a multiply.reduce of
                 the shape of the data.
    """
    self.thestruct = pyclimate.anumhist.CreateNHArray(xl, xu, nbins, elems)

  def Update(self, field):
    "Adds a new multidimensional item 'field' to the histogram"
    pyclimate.anumhist.UpdateNHArray(
      self.thestruct,
      numpy.ravel(field).astype('d')
    )

  def GetRange(self, prob):
    "Returns the range enclosing a 1-'prob' probability"
    return pyclimate.anumhist.GetXRange(self.thestruct, prob)

  def GetDeltaX(self):
    "X increment per bin"
    return pyclimate.anumhist.GetDeltaX(self.thestruct)

  def __del__(self):
    "Destructor of the NHArray class"
    pyclimate.anumhist.FreeNHArray(self.thestruct)
