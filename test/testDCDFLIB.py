#!/usr/local/bin/python
#
# test the pydcdflib module.
# 
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
# 

# save a lot of typing (namespace will become dirty but this is a silly script)
from pyclimate.pydcdflib import *

# Print common fields
def prwhich(cdfob):
	print "Which: %2d"%(cdfob.which,)

def prpq(cdfob):
	print "P,Q: %15.6e %15.6e"%(cdfob.p,cdfob.q)

def prbound(cdfob):
	print "Bound: %15.6e"%(cdfob.bound,)


# Test the "BETA" calculator
# Print the status of beta before and after the computation
# After the first call, each call has to get approximately the same
# values of all the parameters, and we will know that our
# calls are (at least) inverses
def betatest(beta):
	prwhich(beta)
	print "Status: %2d"%(pycdfbet(beta),)
	prpq(beta)
	print "X,Y: %15.6e %15.6e"%(beta.x,beta.y)
	print "A,B: %15.6e %15.6e"%(beta.a,beta.b)
	prbound(beta)

# Binomial test
def binomialtest(binomial):
	prwhich(binomial)
	print "Status: %2d"%(pycdfbin(binomial),)
	prpq(binomial)
	print "S,N: %15.6e %15.6e"%(binomial.s,binomial.xn)
	print "Pr,Opr: %15.6e %15.6e"%(binomial.pr,binomial.ompr)
	prbound(binomial)

# Chi test
def chitest(ch,pycdffunc=pycdfchi,pnonc=0):
	prwhich(ch)
	print "Status: %2d"%(pycdffunc(ch),)
	prpq(ch)
	print "X,DF: %15.6e %15.6e"%(ch.x,ch.df)
	if pnonc:
		print "PNONC: %15.6e",ch.pnonc
	prbound(ch)

# F test
def ftest(fob,cdffunc=pycdff,nonc=0):
	prwhich(fob)
	print "Status: %2d"%(cdffunc(fob),)
	prpq(fob)
	print "F: %15.6e"%(fob.f,)
	print "DFN,DFD: %15.6e %15.6e"%(fob.dfn,fob.dfd)
	if nonc:
		print "PNONC: %15.6e"%(fob.pnonc,)
	prbound(fob)

# Gamma test
def gamtest(gam):
	prwhich(gam)
	print "Status: %2d"%(pycdfgam(gam),)
	prpq(gam)
	print "X,Shape,Scale: %15.6e %15.6e %15.6e"%(gam.x,gam.shape,gam.scale)
	prbound(gam)

# Negative binomial test
def nbntest(nbn):
	prwhich(nbn)
	print "Status: %2d"%(pycdfnbn(nbn),)
	prpq(nbn)
	print "S,XN,Pr,Ompr: %15.6e %15.6e %15.6e %15.6e"%(nbn.s,nbn.xn,
			nbn.pr,nbn.ompr)
	prbound(gam)

# Normal test
def nortest(nor):
	prwhich(nor)
	print "Status: %2d"%(pycdfnor(nor),)
	prpq(nor)
	print "X,mean,sd: %15.6e %15.6e %15.6e"%(nor.x,nor.mean,nor.sd)
	prbound(nor)

# Poison distribution
def poitest(poi):
	prwhich(poi)
	print "Status: %2d"%(pycdfpoi(poi),)
	prpq(poi)
	print "S: %15.6e"%(poi.s,)
	prbound(poi)

# T distribution
def ttest(t,pyf=pycdft,nonc=0):
	prwhich(t)
	print "Status: %2d"%(pyf(t),)
	prpq(t)
	print "T,DF: %15.6e %15.6e"%(t.t,t.df)
	if nonc:
		print "PNONC: %15.6e",t.pnonc
	prbound(t)


if __name__=="__main__":

	# Test the Beta function
	beta=CDFBet()
	print beta
	# Start with which=1 (P and Q from X,Y,A and B)
	beta.which=1
	beta.x=0.5
	beta.a=3.45
	beta.b=0.23
	# Initialize the value of P and Q to the correct values
	pycdfbet(beta)
	# Run the test for diferent values of which
	for beta.which in xrange(1,5):
		betatest(beta)


	# Test the Binomial distribution
	binomial=CDFBin()
	print binomial
	binomial.p=0.9
	binomial.s=100
	binomial.xn=10000
	binomial.pr=0.1
	binomial.which=2
	pycdfbin(binomial)
	for binomial.which in xrange(1,5):
		binomialtest(binomial)

	# Test the Chi^2 Calculator
	chi2=CDFChi()
	print chi2
	chi2.which=1
	chi2.p=0.95
	# Test of CDFPQ()
	cpq=CDFPQ()
	pycdfsetq(cpq,0.05)
	chi2.p=cpq.p
	print cpq.p,cpq.q
	chi2.x=2.
	chi2.df=2
	# Initialize the status of chi2
	pycdfchi(chi2)
	for chi2.which in xrange(1,4):
		chitest(chi2)

	# Table of Chi^2
	chtab=[]
	print "%6s"%"DF",
	for i in xrange(3):
		chi2=CDFChi()
		chi2.which=2
		chi2.p=0.9+i*0.05
		if i==2:
			chi2.p=0.999
		print "  %9.5f "%(chi2.p,),
		chtab.append(chi2)
	print
	for df in xrange(5,30):
		print "%6d"%(df,),
		for ch in chtab:
			ch.df=df
			pycdfchi(ch)
			print "%9.5f(%1d)"%(ch.x,ch.status),
		print

	# Non-central Chi^2
	chn=CDFChn()
	print chn
	chn.which=1
	chn.p=0.95
	chn.x=2.
	chn.df=2
	chn.pnonc=20.
	# Initialize the status of chn
	pycdfchn(chn)
	for chn.which in xrange(1,5):
		chitest(chn,pycdfchn,1)

	# F Distribution
	fob=CDFF()
	print fob
	fob.which=2
	fob.p=0.95
	fob.f=100000.
	fob.dfn=6.
	fob.dfd=5.
	pycdff(fob) # Initialize fob.f
	# The library crashes for fob.which==3
	for fob.which in [1,2,4]:
		ftest(fob)
	# F Table
	ftab=[]
	dfns=[ 5 , 10 , 100 , 500 ]
	print "DFns:",
	for df in dfns:
		fob=CDFF()
		fob.which=2
		fob.dfn=df
		print " %12d"%df,
		ftab.append(fob)
	print
	for dfd in xrange(5,21):
		for p in [0.95,0.99]:
			print "%5d(%5.2f)"%(dfd,p),
			for fob in ftab:
				fob.p=p
				fob.dfd=dfd
				status=pycdff(fob)
				print " %9.4f(%1d)"%(fob.f,status),
			print

		
	# Non-central F Distribution
	fob=CDFFnc()
	print fob
	fob.which=2
	fob.p=0.95
	fob.f=100000.
	fob.dfn=6.
	fob.dfd=5.
	fob.pnonc=5.34
	pycdffnc(fob) # Initialize fob.f
	for fob.which in xrange(1,6):
		ftest(fob,pycdffnc,1)

	# CDFGam()
	gam=CDFGam()
	print gam
	gam.which=1
	gam.p=0.95
	gam.x=0.78
	gam.shape=0.98
	gam.scale=10.
	pycdfgam(gam)
	for gam.which in xrange(1,5):
		gamtest(gam)

	
	# CDFnbn
	nbn=CDFNbn()
	print nbn
	nbn.p=0.1
	nbn.s=0.17
	nbn.xn=10000.
	nbn.pr=0.4
	nbn.which=2
	pycdfnbn(nbn)
	for nbn.which in xrange(1,5):
		nbntest(nbn)

	# Normal distribution
	nor=CDFNor()
	print nor
	nor.p=0.9
	nor.mean=0.5
	nor.sd=23.
	nor.which=2
	pycdfnor(nor)
	for nor.which in xrange(1,5):
		nortest(nor)

	# Table of the normal distribution
	nor.which=1
	nor.mean=0.0
	nor.sd=1.
	print "X    Integrate[N(0,1),{u=-\infty,x}]"
	for ix in xrange(31):
		nor.x=ix*0.15
		pycdfnor(nor)
		print "%6.3f %10.7f"%(nor.x,nor.p)

	# Poison
	poi=CDFPoi()
	print poi
	poi.which=2
	poi.p=0.9
	poi.xlam=0.23
	pycdfpoi(poi)
	for poi.which in xrange(1,4):
		poitest(poi)


	# T distribution
	t=CDFT()
	print t
	t.p=0.99
	t.df=10
	t.which=2
	pycdft(t)
	for t.which in xrange(1,4):
		ttest(t)

	# Table of t distribution
	ts=[ CDFT() , CDFT() , CDFT() ]
	for t in ts:
		t.which=2
	ts[0].p=0.95
	ts[1].p=0.99
	ts[2].p=0.999
	print "%6s %8.4f %8.4f %8.4f"%("DF",0.95,0.99,0.999)
	for df in xrange(5,101,5):
		print "%6d"%df,
		for t in ts:
			t.df = df
			pycdft(t)
			print "%8.4f"%t.t,
		print

	# Non-central T distribution
	t=CDFTnc()
	print t
	t.p=0.99
	t.df=10
	t.pnonc=10.
	t.which=2
	pycdftnc(t)
	for t.which in xrange(1,5):
		ttest(t,pycdftnc,1)

