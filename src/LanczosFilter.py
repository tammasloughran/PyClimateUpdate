# Adapted for numpy/ma/cdms2 by convertcdms.py
# LanczosFilter.py

"""Multivariate Lanczos filter

"""
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
# Jon Saenz, 20000305
# Juan Zubillaga, 20000324
# Jon Saenz, 20000616
# Jesus Fernandez, 20000724 
#
# For notation and mathematical details, see Duchon, 1979, Journal of Applied 
# Meteorology, Lanczos filtering in one and two dimensions, volume 18, 
# pages=1016-1022

import numpy.oldnumeric as Numeric
import pyclimate.LinearFilter

import sys,math
import pyclimate.readdat

class LanczosFilter(pyclimate.LinearFilter.LinearFilter):
  """'LinearFilter' derived class for Lanczos filtering

  For notation and mathematical details, see Duchon, 1979, Journal of Applied 
  Meteorology, *Lanczos filtering in one and two dimensions*, volume 18, 
  pages 1016-1022.
  """
  def __init__(self,filtertype='bp',fc1=0.0,fc2=0.5,n=None):
    """Constructor for the class 'LanczosFilter'

    Initialize the variables to hold the needed data
    The filter works as follows, first, it gets the
    coefficients to be used to weight each record performing a
    recursive filtering on the impulse response function
    Next, filter the records by means of a running buffer which is
    weighted using the weights... and that's all

    Optional Arguments:

      'filtertype' -- String identifying the filter type. 'lp' for 
                      low-pass filter, 'hp' for high-pass filter and
                      'bp' for band-pass filter.

      'fc1' -- First cutoff frequency (in inverse time steps).
               Defaults to 0.0

      'fc2' -- Second cutoff frequency (in inverse time steps).
               Defaults to 0.5

      'n' -- Number of points for the filter. This number of points will
             be missed at the beginning and at the end of the raw record.
             Defaults to a number a 30% higher than that recomended for
             secure band-pass filtering by Duchon (1979).

    NOTE: With the default arguments the filter does NOT filter at all.
    It performs a band-pass filtering for all frequencies.
    
    NOTE 2: If the first and second cutoff frequencies are different 
    band-pass filtering is assumed even though 'lp' or 'hp' filtertype were 
    selected.
    """
    if fc1 != fc2:
      self.filtertype='bp'
    else:
      self.filtertype=filtertype
    # Accounts for the three types of filter
    self.fc1=fc1
    self.fc2=fc2
    if self.filtertype=='lp':
      self.fc1=0.0
    elif self.filtertype=='hp':
      self.fc2=0.0
    # Length of the buffer and the coefficients of the filter
    if n!=None:
       self.length=2*n+1
    else:
       # 30% higher than recommended for band-pass
       self.length=2*int(1.3*(1.3/abs(self.fc2-self.fc1)))+1
    # Get the filter coefficients
    self.coefs=self.getcoefs()
    # Position in the buffer to store the input datafield
    self.target=0
    # Output record id
    self.record=0


  def _place(self,k,n,pm1):
    return n+k*pm1
 
  def getcoefs(self):
    "Filter coefficients"
    n=self.length/2
    thepi=math.acos(-1.)
    ocoefs=Numeric.zeros(self.length,Numeric.Float64)
    # This is pretty singular...
    # sinc(0)=1!!; sin(2fx)/x = 2f!!
    k=0
    ocoefs[self._place(k,n,1)]=2*(self.fc2-self.fc1)*1.
    # Slight modification for the high pass
    if self.filtertype=='hp':
      ocoefs[self._place(k,n,1)]=1+ocoefs[self._place(k,n,1)]
    for ik in xrange(n):
      k=ik+1
      sigma=math.sin(thepi*k/n)*n/thepi/k
      firstfactor=(math.sin(2*thepi*self.fc2*k)-
                   math.sin(2*thepi*self.fc1*k))/thepi/k
      ocoefs[self._place(k,n,1)]=firstfactor*sigma
      ocoefs[self._place(k,n,-1)]=firstfactor*sigma
    return ocoefs

  def prettyprintcoefs(self):
    "Pretty-print the coefficients"
    print "# Lanczos: -> %4d coefficients"%(self.length,)
    print "# Coefficients:"
    for icoef in xrange(self.length):
      print "# C: %2d %12.4f"%(icoef,self.coefs[icoef])
    print "# Norm of the coefficients:",add.reduce(self.coefs)

if __name__=="__main__":
  def testequality(dataa,datab,label=""):
    print "Testing equality:"+label
    elems=multiply.reduce(Numeric.array(dataa.shape,Numeric.Float64))
    residual2=(dataa-datab)*(dataa-datab)
    while len(residual2.shape)>1:
      residual2=add.reduce(residual2)
    rmsdiff=sqrt(add.reduce(residual2)/float(elems))
    print "RMSdiff: %10.5f"%(rmsdiff,)

  # Now, filter real data and compare with calibration results.
  # Both high pass and low-pass versions
  pldata=Numeric.array(pyclimate.readdat.readcols("plnibpei.dat",[2,3,4,5,6,7]))
  years=Numeric.array(pyclimate.readdat.readcol("plnibpei.dat",1))
  npoints = 7
  lpf=LanczosFilter('lp',0.25, 0.25, npoints)
  hpf=LanczosFilter('hp',0.25, 0.25, npoints)
  bpf=LanczosFilter('bp',0.20, 0.40, npoints)
  lfset=[]
  lyears=[]
  hfset=[]
  hyears=[]
  bfset=[]
  byears=[]
  for irec in xrange(len(pldata)):
    ldata=lpf.getfiltered(pldata[irec])
    if ldata:
      lfset.append(ldata)
      lyears.append(years[irec-lpf.length/2])
    hdata=hpf.getfiltered(pldata[irec])
    if hdata:
      hfset.append(hdata)
      hyears.append(years[irec-hpf.length/2])
    bdata=bpf.getfiltered(pldata[irec])
    if bdata:
      bfset.append(bdata)
      byears.append(years[irec-bpf.length/2])
  # Create arrays from the filtered data
  hfdata=Numeric.array(hfset)
  lfdata=Numeric.array(lfset)
  bfdata=Numeric.array(bfset)
  hfyears=Numeric.array(hyears)
  lfyears=Numeric.array(lyears)
  bfyears=Numeric.array(byears)

  ofile=open("lfdata.tmp","w")
  elems=len(lfdata)
  for irec in xrange(elems):
    ofile.write(
      "%15.6f %16.6f %16.6f %16.6f %16.6f %16.6f %16.6f\n"%(
      lfyears[irec],
      lfdata[irec,0],
      lfdata[irec,1],
      lfdata[irec,2],
      lfdata[irec,3],
      lfdata[irec,4],
      lfdata[irec,5]))
  ofile.close()

  ofile=open("hfdata.tmp","w")
  elems=len(hfdata)
  for irec in xrange(elems):
    ofile.write(
      "%15.6f %16.6f %16.6f %16.6f %16.6f %16.6f %16.6f\n"%(
      hfyears[irec],
      hfdata[irec,0],
      hfdata[irec,1],
      hfdata[irec,2],
      hfdata[irec,3],
      hfdata[irec,4],
      hfdata[irec,5]))
  ofile.close()
  
  ofile=open("bfdata.tmp","w")
  elems=len(bfdata)
  for irec in xrange(elems):
    ofile.write(
      "%15.6f %16.6f %16.6f %16.6f %16.6f %16.6f %16.6f\n"%(
      bfyears[irec],
      bfdata[irec,0],
      bfdata[irec,1],
      bfdata[irec,2],
      bfdata[irec,3],
      bfdata[irec,4],
      bfdata[irec,5]))
  ofile.close()


  # Load the reference series
  hfrefyears=Numeric.array(pyclimate.readdat.readcol("plnibpei.hf.lanczos.ref"))
  lfrefyears=Numeric.array(pyclimate.readdat.readcol("plnibpei.lf.lanczos.ref"))
  bfrefyears=Numeric.array(pyclimate.readdat.readcol("plnibpei.bf.lanczos.ref"))
  hfrefdata=Numeric.array(pyclimate.readdat.readcols("plnibpei.hf.lanczos.ref", [2,3,4,5,6,7]))
  lfrefdata=Numeric.array(pyclimate.readdat.readcols("plnibpei.lf.lanczos.ref", [2,3,4,5,6,7]))
  bfrefdata=Numeric.array(pyclimate.readdat.readcols("plnibpei.bf.lanczos.ref", [2,3,4,5,6,7]))

  # Test if the datasets are equal
  testequality(hfrefyears,hfyears,"HFYEARS")
  testequality(lfrefyears,lfyears,"LFYEARS")
  testequality(bfrefyears,bfyears,"BFYEARS")
  testequality(hfrefdata,hfdata,"HFDATA")
  testequality(lfrefdata,lfdata,"LFDATA")
  testequality(bfrefdata,bfdata,"BFDATA")
