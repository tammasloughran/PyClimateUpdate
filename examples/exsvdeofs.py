# Adapted for numpy/ma/cdms2 by convertcdms.py
# exsvdeofs.py
#
# Example on the use of svdeofs.py
from numpy.oldnumeric import *
from pyclimate.svdeofs import *
from pyclimate.readdat import *
from pyclimate.mvarstatools import *

# The chemical.dat example at Jackson, 1991
print "#"*50
print "# Chemical example"
chdata=array(readcols("../test/chemical.dat",[1,2]))
z,lambdas,eofs=svdeofs(chdata)
varfrac=getvariancefraction(lambdas)
north=northtest(lambdas,len(chdata))
print "# Eigenvalues, Variance fraction, North_interval"
for ilambda in xrange(len(lambdas)):
	print "# Lambda_%1d:%10.3f %10.3f %10.4f [%10.3f %10.3f]"%(
		ilambda,lambdas[ilambda],varfrac[ilambda],
		north[ilambda],lambdas[ilambda]-north[ilambda],
		lambdas[ilambda]+north[ilambda])
chis,chiprobs=bartletttest(lambdas,len(chdata))
print "# Bartlett Test (Chi2,Chi2prob)"
for ichi in xrange(len(chis)):
	print "# %15.9f %15.10e"%(chis[ichi],chiprobs[ichi])
print "# Eigenvectors:"
for ivect in xrange(len(lambdas)):
	print "# EOF %1d:"%(ivect,),
	for icomp in xrange(len(lambdas)):
		print "%10.4f"%(eofs[icomp,ivect],),
	print
print "# Principal components:"
for itime in xrange(len(chdata)):
	print "%6d"%(itime,),
	for icomp in xrange(len(lambdas)):
		print " %10.4f"%(z[itime,icomp]),
	print
print "# Some extra information:"
print "# Norm of eigenvectors:"
for ivect in xrange(len(lambdas)):
	vect=array(eofs[:,ivect])
	print "%3d %10.4f"%(ivect,sqrt(add.reduce(vect*vect)))
print "# Norm of principal components:"
totalvar=add.reduce(lambdas)
for ipc in xrange(len(lambdas)):
	pc=array(z[:,ipc])
	res=pc-add.reduce(pc)/len(pc)
	thisvar=add.reduce(res*res)/float(len(pc))
	print "%3d %10.4f %10.4f"%(ipc,thisvar,thisvar/totalvar)

