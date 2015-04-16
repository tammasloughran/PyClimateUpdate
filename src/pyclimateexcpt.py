"""PyClimate Exceptions, as classes

"""

# Copyright (C) 2000, Jon Saenz, Jesus Fernandez and Juan Zubillaga
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
# Jon Saenz, April 2001

import exceptions

##########################################################
# All PyClimate exceptions share this behaviour
# They can be written as strings and some values can be returned
#################################################
class PyClimateException(exceptions.Exception):
	"Mother class for all pyclimate exceptions"
	def __str__(self):
		if self.message:
			return "PyClimate Exception\n"+self.message
		else:
			return "PyClimate Exception\n"
	def GetExceptionValue(self):
		return self.value

##################################################
# This one was raised in KZFilter
##################################3
class KZEvenPoints(PyClimateException):
	def __init__(self,points):
		self.message="KZFilter Exception\nKZ filters can not use even"
		self.message=self.message+"points (%d)."%(points,)
		self.value=points

##################################################
# This one is raised by the t-test on the difference of means
##################################3
class ttestPoints(PyClimateException):
	def __init__(self,points):
		self.message="t-test Exception\n"
		self.message+="The number of records (%d) is too small"%(
				points,)
		self.value=points

#####################################################
# Related to JDTimeHandler
#################################################
class JDTHBrokenTString(PyClimateException):
	def __init__(self,tstring):
		self.message="JDTimeHandler Exception\nBroken time string:\n"
		self.message=self.message+tstring
		self.value=tstring

class JDTHBrokenTUnits(PyClimateException):
	def __init__(self,ustring):
		self.message="JDTimeHandler Exception\nBroken units string:\n"
		self.message=self.message+ustring
		self.value=ustring

class JDTHInvalidToken(PyClimateException):
	def __init__(self,tok):
		self.message="JDTimeHandler Exception\nInvalid token:\n"
		self.message=self.message+tok
		self.value=tok

class JDTHListTooShort(PyClimateException):
	def __init__(self,llen):
		self.message="JDTimeHandler Exception\nList too short: "
		self.message=self.message+"%d items"%(llen,)
		self.value=llen




####################################################
# This existed in svdeofs.py
#####################################################
class EOFScalingError(PyClimateException):
	def __init__(self,pcscaling):
		self.message="EOF Exception\nUnknown PC scaling requested"
		self.message=self.message+" (%d)."%(pcscaling,)
		self.value=pcscaling

###########################################################
# These ones existed in mvarstatools.py
###############################################################
class MVSTLengthException(PyClimateException):
	def __init__(self,ll,rl):
		self.message="MVST Exception\nBoth datasets are of different"
		self.message=self.message + " length"
		self.message=self.message+" (left=%d versus right=%d)"%(ll,rl)
		self.value=(ll,rl)


###########################################################
# These ones existed in svd.py
###############################################################
class SVDLengthException(PyClimateException):
	def __init__(self,ll,rl):
		self.message="SVD Exception\nBoth datasets are not of the same"
		self.message=self.message + " length"
		self.message=self.message+" (left=%d versus right=%d)"%(ll,rl)
		self.value=(ll,rl)

class SVDSubsetLengthException(PyClimateException):
	def __init__(self,ll,rl):
		self.message="SVD-MC Exception\nBoth subsets hold a different "
		self.message=self.message + " number of singular vectors for\n"
		self.message=self.message+" the Monte Carlo test:"
		self.message=self.message+"(left=%d versus right=%d)"%(ll,rl)
		self.value=(ll,rl)

class InvalidNaNs(PyClimateException):
        def __init__(self,channels):
                self.message = """There are invalid NaNs in the dataset.\n
                    NaNs can only exist for all samples of a given channel.\n
                    Channels that have invalid NaNs are:"""
                self.value = channels


###############################################
# ASCII IO
##############################################
class WrongWriteDimensions(PyClimateException):
	def __init__(self,lenshape):
		self.message="writedat Exception\n"
		self.message=self.message+"Only 1D and 2D arrays supported:"
		self.message=self.message+"(passed=%d)"%(lenshape,)
		self.value=lenshape

#############################################################
# This one was used in SVD, but is better reallocated to the Monte Carlo Test
# routines now
################################################################
class MCTestException(PyClimateException):
	def __init__(self,items,total):
		self.message="Monte Carlo Test Exception\nRequested subsample "
		self.message=self.message+"(%d) larger than the total "%(items,)
		self.message=self.message +"sample (%d)."%(total,)
		self.value=(items,total)

############################################
# CCA
####################################################
class TooBigIntParameter(PyClimateException):
	def __init__(self, paramname, wrongvalue, maxvalue):
		self.message="Integer value out of range Exception\n"
		self.message=self.message+"Passed parameter: %s = %d\n" % (paramname,wrongvalue)
		self.message=self.message+"Maximum value: %d" % maxvalue
		self.value=(wrongvalue, maxvalue)

################################################################
# ANALOG
#############################################################
class ANALOGNoMatchingShape(PyClimateException):
	def __init__(self,wrongshape,rightshape):
                self.message="ANALOG Exception\nProvided field shape do not match with the internal value:\n"
                self.message=self.message+"Provided field shape: " +`wrongshape`
                self.message=self.message +"\nANALOG object field shape: "+ `rightshape`
                self.value=(wrongshape,rightshape)  

class ANALOGNoMatchingLength(PyClimateException):
	def __init__(self,wrongshape,rightshape):
                self.message="ANALOG Exception\nProvided field length (time records) do not match the internal value:\n"
                self.message=self.message+"Provided field length: " +`wrongshape`
                self.message=self.message +"\nANALOG object field length: "+ `rightshape`
                self.value=(wrongshape,rightshape)  

######################################################################
# WHAT WILL WE DO WITH THESE CRAZY NAMES????
# These names are assigned for backward compatibility only, just to avoid
# breaking user code. No warranty of support or existence in future releases
# They will only work in case imports do not use different name-spaces
# (i.e. with from xxxx import * sentences)
#################################################################
svdNotSameLengthException = SVDLengthException
SVDielemsexception = MCTestException
SVDshouldbeequalsubsets = SVDSubsetLengthException
ScalingError = EOFScalingError
KZnothesepoints = KZEvenPoints
novalidtstring = JDTHBrokenTString
nohandledunits = JDTHBrokenTUnits
novalidtokens = JDTHInvalidToken
shortlistlen = JDTHListTooShort

#############################################
# Test the module by itself without loading 
# and reinstalling PyClimate during development time
#####################################################
def testallpyclimateexceptions():
	# This function is only defined during testing
	def testexception(message,eclassname,einstance):
		print "Do not panic!! I am testing my own exceptions ;-)"
		print message
		print "*"*len(message)
		try:
			raise einstance
		except eclassname,e:
			print e
			print "Exception value:",e.GetExceptionValue()
		print

	# Test them all...
	###################################################################
	# KZ exception
	testexception("Testing KZ exception",KZEvenPoints,KZEvenPoints(14))

	# Test EOF scaling exception
	testexception("Testing EOF scaling exception",EOFScalingError,
			EOFScalingError(123))

	# Test SVD exceptions
	testexception("Test former SVD exceptions - Length",SVDLengthException,
			SVDLengthException(29,3))
	testexception("Test former SVD exceptions - Subset Length",
			SVDSubsetLengthException,
			SVDSubsetLengthException(20,3))

	# Test Monte Carlo exceptions
	testexception("Test the MC exception",MCTestException,
	MCTestException(2,3))

	# Test ASCII IO exceptions
	testexception("Test the ASCII IO exception",WrongWriteDimensions,
	WrongWriteDimensions(3))

	# Test JDTimeHandler exceptions
	testexception("Test JDTHBrokenTString",JDTHBrokenTString,
			JDTHBrokenTString("This is a broken time string"))
	testexception("Test JDTHBrokenTUnits",JDTHBrokenTUnits,
			JDTHBrokenTUnits("This is a broken units string"))
	testexception("Test JDTHInvalidToken",JDTHInvalidToken,
			JDTHInvalidToken("nekot|token"))
	testexception("Test JDTHListTooShort",JDTHListTooShort,
			JDTHListTooShort(-343512))
	# Test CCA exceptions
	testexception("Test TooBigIntParameter",TooBigIntParameter,
			TooBigIntParameter("myparameter",5,4))
	# Test ANALOG exceptions
	testexception("Test ANALOGNoMatchingShape",ANALOGNoMatchingShape,
			ANALOGNoMatchingShape((2,4),(3,4)))


if __name__=="__main__":
	testallpyclimateexceptions()

