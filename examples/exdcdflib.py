# exdcdflib.py
#
# Examples on the use of the pydcdflib module.

# save a lot of typing 
from pyclimate.pydcdflib import *

def prwhich(cdfob):
        print "Which: %2d"%(cdfob.which,)

def prpq(cdfob):
        print "P,Q: %15.6e %15.6e"%(cdfob.p,cdfob.q)

def prbound(cdfob):
        print "Bound: %15.6e"%(cdfob.bound,)


def betatest(beta):
        prwhich(beta)
        print "Status: %2d"%(pycdfbet(beta),)
        prpq(beta)
        print "X,Y: %15.6e %15.6e"%(beta.x,beta.y)
        print "A,B: %15.6e %15.6e"%(beta.a,beta.b)
        prbound(beta)

# Chi test
def chitest(ch,pycdffunc=pycdfchi,pnonc=0):
        prwhich(ch)
        print "Status: %2d"%(pycdffunc(ch),)
        prpq(ch)
        print "X,DF: %15.6e %15.6e"%(ch.x,ch.df)
        if pnonc:
                print "PNONC: %15.6e",ch.pnonc
        prbound(ch)

# Normal test
def nortest(nor):
        prwhich(nor)
        print "Status: %2d"%(pycdfnor(nor),)
        prpq(nor)
        print "X,mean,sd: %15.6e %15.6e %15.6e"%(nor.x,nor.mean,nor.sd)
        prbound(nor)


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

