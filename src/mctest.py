# Adapted for numpy/ma/cdms2 by convertcdms.py
# mctest.py

"""Some functions to get faster Monte Carlo tests

"""

# Copyright (C) 2000, Jon Saenz and Juan Zubillaga
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

import numpy.oldnumeric.random_array as RandomArray
import pyclimate.pyclimateexcpt

RA=RandomArray
pe=pyclimate.pyclimateexcpt

def getrandomsubsample(items,totalitems,sorted=0):
	"""Get a random selection of indices without repeating them.

  Arguments:

    'items' -- Number of samples in the subsample

    'totalitems' -- Number of samples in the whole sample

    'sorted' -- If non-zero, sort the subsample (Defaullt: 0)

  Returns a NumPy array of indices from the array [0...totalitems-1]

  Raises MCTestException if 'items' > 'totalitems'
  """
	if items>totalitems:
		raise pe.MCTestException(items,totalitems)
	seq=RA.permutation(totalitems)[:items]
	if sorted:
		seq.sort()
	return seq

def getrandomsubsample2(items,totalitems,sorted=0):
	"""Get a random selection of indices without repeating them.

  Arguments:

    'items' -- Number of samples in the subsample

    'totalitems' -- Number of samples in the whole sample

    'sorted' -- If non-zero, sort the subsample

  Returns a tuple of NumPy arrays of indices from the array [0...totalitems-1]
  and the elements which did not enter the selection [totalitems....]

  Raises MCTestException if 'items' > 'totalitems'
  """
	if items>totalitems:
		raise pe.MCTestException(items,totalitems)
	perm=RA.permutation(totalitems)
	seq=perm[:items]
	noseq=perm[items:]
	if sorted:
		seq.sort()
		noseq.sort()
	return (seq,noseq)

