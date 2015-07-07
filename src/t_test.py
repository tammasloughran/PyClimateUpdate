# Adapted for numpy/ma/cdms2 by convertcdms.py
# t_test.py
#
# A t-test on the difference of means.
# It is able to handle fields with missing data
# We are supposing that both fields have the same variance,
# which might not be a real feature of the case being analysed.
# It is up to the user to test it.
#
# This is all failry redundant in light of the existence of scipy.
#
# Copyright (C) 2002, Jon Saenz
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
import pyclimate.pyclimateexcpt

class t_test_dif_of_means:
    def __init__(self,afield,bfield,missing_value=None):
        self.x=numpy.array(afield)
        self.y=numpy.array(bfield)
        Nx=float(len(self.x))
        Ny=float(len(self.y))
        if self.Nx==0:
            raise pyclimate.pyclimateexcpt.ttestPoints(Nx)
        if self.Ny==0:
            raise pyclimate.pyclimateexcpt.ttestPoints(Ny)
        meanx = self.x.mean()
        meany = self.y.mean()
        stdx = self.x.std()
        stdy = self.y.std()
        sxy = numpy.sqrt(((Nx-1)*stdx**2) + ((Ny-1)*stdy**2)/(Nx+self.Ny-2))
        self.t = (meanx-meany)/(sxy*numpy.sqrt((1/Nx)+(1/Ny)))

    def tvalue(self):
        return self.t
