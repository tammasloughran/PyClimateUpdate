# Adapted for numpy/ma/cdms2 by convertcdms.py
# KZFilter.py

"""Multivariate Kolmogorov-Zurbenko filter

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
# Jesus Fernandez, 20000724

import numpy as Numeric
import pyclimate.LinearFilter

import sys,math
import pyclimate.readdat
import pyclimate.pyclimateexcpt

pex = pyclimate.pyclimateexcpt

class KZFilter(pyclimate.LinearFilter.LinearFilter):
  # Initialize the variables to hold the needed data
  # Don't allow an even number of points
  # The filter works as follows, first, it gets the
  # coefficients to be used to weight each record performing a
  # recursive filtering on the impulse response function
  # Next, filter the records by means of a running buffer which is
  # weighted using the weights... and that's all
  def __init__(self,points,iterations,lowpass=1):
    """Constructor for the class 'KZFilter'

    Arguments:

      'points' -- Total number of points for running average of the filter. 
                  It must be an odd integer.

      'iterations' -- Number of iterations of the average to improve the
                      damping of the secondary maxima.

    Optional arguments:

      'lowpass' -- Bit parameter indicating wether the filter is a
                   low-pass (default, 1) or a high-pass (0).
    """
    # Is the number even?
    if not points%2:
      raise pex.KZEvenPoints(points)

    # Length of the buffer and the coefficients of the filter
    self.length=(iterations-1)*(points-1)+points
    # Iterations of the filter
    self.iterations=iterations
    # Points in each average
    self.points=points
    # Get the filter coefficients
    self.coefs=self.getcoefs()
    if not lowpass:
      allpass=Numeric.zeros((self.length,),Numeric.float64)
      allpass[self.length/2]=1.
      self.coefs[:]=allpass[:]-self.coefs[:]
    # Position in the buffer to store the input datafield
    self.target=0
    # Output record id
    self.record=0

  def getcoefs(self):
    "Coefficients of the filter"
    oldcoef=Numeric.zeros(self.length,Numeric.float64)
    newcoef=Numeric.zeros(self.length,Numeric.float64)
    oldcoef[0]=1
    lfiltro=1
    for i1 in range(self.iterations):   # veces la media movil
      for j1 in range(lfiltro+(self.points-1)):# puesta a 0 de los "n
        newcoef[j1]=0
      for  j1 in range(self.points):    # Calculo del siguiente filtro
        for  n1 in range(lfiltro):
          newcoef[j1+n1]=newcoef[j1+n1]+oldcoef[n1]
      lfiltro=lfiltro+(self.points-1) # Actualizacion anchura de filtro
      for j1 in range(lfiltro):       # Actualizacion de los "viejos"
        oldcoef[j1]=newcoef[j1]       # preparando siguiente iteracion
    total=0
    for i in range(lfiltro):
      total=total+newcoef[i]
    newcoef=newcoef/total
    return newcoef

  def getcutofffrequency(self):
    "Get the cutoff frequency out of the iterations and points of the filter"
    exp1=0.5/self.iterations
    mypi=math.acos(-1)
    cf=math.sqrt(6.)/mypi*math.sqrt((1-math.pow(0.5,exp1))/(self.points*self.points-math.pow(0.5,exp1)))
    return cf

  def prettyprintcoefs(self):
    "Pretty-print the coefficients"
    print "# KZ(%2d,%2d): -> %4d coefficients"%(self.points,
        self.iterations,self.length)
    print "# Coefficients:"
    for icoef in xrange(self.length):
      print "# %2d %12.4f"%(icoef,self.coefs[icoef])
    print "# Norm of the coefficients:",add.reduce(self.coefs)
    print "# Cutoff frequency: %12.5f"%(self.getcutofffrequency(),)



if __name__=="__main__":
  def testequality(dataa,datab,label=""):
    print "Testing equality:"+label
    elems=multiply.reduce(Numeric.array(dataa.shape,Numeric.float64))
    residual2=(dataa-datab)*(dataa-datab)
    while len(residual2.shape)>1:
      residual2=add.reduce(residual2)
    rmsdiff=sqrt(add.reduce(residual2)/float(elems))
    print "RMSdiff: %10.5f"%(rmsdiff,)

  # Check the number of coefficients and so on for a selection
  # of filters
  kzf=KZFilter(3,3)
  kzf.prettyprintcoefs()
  kzf=KZFilter(5,2)
  kzf.prettyprintcoefs()
  kzf=KZFilter(5,5)
  kzf.prettyprintcoefs()

  # Check whether the system works for different shapes of data
  # 2-D data..
  a=Numeric.array([[0.9,0.8],[0.7,0.6]])
  for i in xrange(50):
    af=kzf.getfiltered(a)
    if af:
      print "2-D Done: %3d"%(i,)

  # Univariate data
  a=Numeric.array([0.9,0.8,0.7,0.6]*10)
  kzf=KZFilter(5,5,0)
  for i in xrange(50):
    af=kzf.getfiltered(a)
    if af:
      print "1-D Done: %3d"%(i,)

  # BIG data with multiple dimensions.......
  records=25
  data=ones((records,5,6,10,10,2),Numeric.float64)
  kzf=KZFilter(5,3)
  irec=0
  while irec<records:
    af=kzf.getfiltered(data[irec])
    if af:
      print "BIG Done: %3d"%(irec,)
    irec=irec+1

  # Now, filter real data and compare with calibration results.
  # Both high pass and low-pass versions
  pldata=Numeric.array(pyclimate.readdat.readcols("plnibpei.dat",[2,3,4,5,6,7]))
  years=Numeric.array(pyclimate.readdat.readcol("plnibpei.dat",1))
  lpf=KZFilter(5,3)
  hpf=KZFilter(5,3,0)
  lfset=[]
  lyears=[]
  hfset=[]
  hyears=[]
  for irec in xrange(len(pldata)):
    ldata=lpf.getfiltered(pldata[irec])
    if ldata:
      lfset.append(ldata)
      lyears.append(years[irec-lpf.length/2])
    hdata=hpf.getfiltered(pldata[irec])
    if hdata:
      hfset.append(hdata)
      hyears.append(years[irec-lpf.length/2])
  # Create arrays from the filtered data
  hfdata=Numeric.array(hfset)
  lfdata=Numeric.array(lfset)
  hfyears=Numeric.array(hyears)
  lfyears=Numeric.array(lyears)
  ofile=open("lfdata.tmp","w")
  elems=len(lfdata)
  for irec in xrange(elems):
    ofile.write(
      "%15.6f %16.6f %16.6f %16.6f %16.6f %16.6f %16.6f\n"%(
      lfyears[irec],lfdata[irec,0],lfdata[irec,1],
      lfdata[irec,2],lfdata[irec,3],lfdata[irec,4],
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

  # Load the reference series
  hfrefyears=Numeric.array(pyclimate.readdat.readcol("plnibpei.hf.ref"))
  lfrefyears=Numeric.array(pyclimate.readdat.readcol("plnibpei.lf.ref"))
  hfrefdata=Numeric.array(pyclimate.readdat.readcols("plnibpei.hf.ref", [2,3,4,5,6,7]))
  lfrefdata=Numeric.array(pyclimate.readdat.readcols("plnibpei.lf.ref", [2,3,4,5,6,7]))

  # Test if the datasets are equal
  testequality(hfrefyears,hfyears,"HFYEARS")
  testequality(lfrefyears,lfyears,"LFYEARS")
  testequality(hfrefdata,hfdata,"HFDATA")
  testequality(lfrefdata,lfdata,"LFDATA")
