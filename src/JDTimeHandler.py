# JDTimeHandler.py

"""A General purpose JDTime handler 

  It is very useful to process the
  units attribute of the time variable of COARDS netCDF files
"""
# Jon Saenz, 20000214
# 
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
 
import pyclimate.JDTime 
import string
import pyclimate.pyclimateexcpt

pjd=pyclimate.JDTime
pex=pyclimate.pyclimateexcpt

class JDTimeHandler:
	"Encode/decode dates as floating point time values in netCDF files"
	def __init__(self,tstring,mydebug=0):
		"""Constructor for the class JDTimeHandler

		Each instance is created passing the units attribute
		of the time variable in the COARDS--Compliant netCDF file

		Arguments:

			'tstring' -- COARDS--Compliant netCDF time units string
		"""
		self.debug=mydebug
		if self.debug:
			print "Input string:", tstring
		# Allocate one instance of JDTime just once because it will
		# probably be used a lot, but it is not needed by now...
		self.jdt=pjd.JDTime()
		# Parse the units string
		# Usually, it should be something like
		# hours|days|minutes ... SINCE Y-[blank]M-[blank]D[blankH:M:S]
		# No support for not UTC time zones by now...
		tokens=string.split(tstring)
		if len(tokens)<3:
			raise pex.JDTHBrokenTString(tstring)
		self.scalefactor=self.getscalefactorfromunits(tokens[0])
		if string.upper(tokens[1])!="SINCE":
			raise pex.JDTHBrokenTString(tstring)
		try:
			datestr=self.buildcompliantdatestring(tokens[2:])
		except JDTHInvalidToken:
			raise pex.JDTHBrokenTString(tstring)
		if self.debug:
			print "Scale Factor:",self.scalefactor
			print "Rebuild Date String:",datestr
			print
		self.offset=self.getoffsetfromdate(datestr)

	def match(self,str,strref):
		"Match strings using plurals and no case"
		ustr=string.upper(str)[:len(strref)]
		uref=string.upper(strref)
		matched=(ustr==uref)
		return matched

	def getscalefactorfromunits(self,units):
		"""Get the scale factor from units

		The scfactor must be such that t*scfactor==(Julian) days

		Some time units like month/year are not very
		clearly defined in terms of days, so, they
		are not handled, because they should not be used
		In the case of month, this is clear (How many days are in a month?,
		28, 29, 30, 31???)

		For years, the same applies, 365, 366, tropical year?...
		Better not to use those units
		"""
		if self.match(units,"second"):
			scfactor=1./86400.
		elif self.match(units,"minute"):
			scfactor=1./1440.
		elif self.match(units,"hour"):
			scfactor=1./24.
		elif self.match(units,"day"):
			scfactor=1.
		elif self.match(units,"week"):
			scfactor=7.
		else:
			raise pex.JDTHBrokenTUnits(units)
		return scfactor

	def buildcompliantdatestring(self,tokens):
		"""Building a compliant date string

		The date string should be writen according to a strict
		grammar, ideally (remeber, no time zone handled...):

		'YYYY-MM-DD H:M:S'

		Like in 1956-08-03 00:36:25.6

		But users could be lazy and write things like

		'1985 - 5 - 1 2 : 3: 4.5'

		Or, even worse...

		'1985 - 5 -1 2'

		Thus, we should try to overcome these defects
		in the set of tokens... and create a fixed-leng date structure
		that will be easily used by the function that parses it.
		BTW, I am writing this AFTER 20000101, so, nobody should
		expect this function prepends 1900 to the year strings.
		In fact, somebody could be trying to use this
		functions to represent very ancient dates... (though
		I have not checked if they work correctly for those years)
		"""
		datefields=[0.,0.,0.,0.,0.,0.]
		itarget=0
		itok=0
		maxtok=len(tokens)
		# Process YMD fields, lazy with ending -'s
		while itok<len(tokens) and itarget<3:
			# Skip empty tokens
			if len(tokens[itok])==0:
				continue
			# If there is a ":", then, this corresponds
			# to HMS...
			if string.find(tokens[itok],":")!=-1:
				break
			# Some valid data can be linked to some '-'s
			subtoks=string.split(tokens[itok],"-")
			for tok in subtoks:
				if len(tok)==0:
					continue
				datefields[itarget]=string.atoi(tok)
				itarget=itarget+1
			itok=itok+1
		# OK, the YMD fields should be correctly parsed by now
		# We have only left previous while() because:
		# a) -> Tokens finished => we are having default vals
		# b) -> We have found a ":" => Process HMS fields
		# c) -> Date[0:2] are already filled => Process HMS
		# Process HMS fields, lazy with ending :'s
		dontupdate=0
		while itok<len(tokens) and itarget<6:
			if len(tokens[itok])==0:
				continue
			subtoks=string.split(tokens[itok],":")
			for tok in subtoks:
				if len(tok)==0:
					continue
				# As floats... because of the "second"
				# (seconds) field...
				if not dontupdate:
					datefields[itarget]=string.atof(tok)
					itarget=itarget+1
				else:
					# Raise an exception for non-zero
					# TZONE fields...
					if string.atof(tok)!=0:
						raise pex.JDTHInvalidToken(tok)
				# We have already finished the available slots,
				# and we are starting to process the TZONE
				# fields, so, allow zeros in this part
				if itarget==6:
					dontupdate=1
			itok=itok+1
		# If there is any information left, then, raise
		# an exception, non UTC times not handled
		# (Allow passing zeros for datezone information)
		if itok<len(tokens) and itarget==6:
			for token in tokens[itok:]:
				subtokens=string.split(token,":")
				for subtoken in subtokens:
					if len(subtoken)==0:
						continue
					if string.atof(subtoken)==0:
						continue
					else:
						raise pex.JDTHInvalidToken(tok)
		# OK, should have already finished...
		# Just a final check
		# For HMS, 0:0:0.0 seems reasonable, but
		# for YMD, valid values are requested, 0:0:0 is not
		# a valid date (year 0 DOES NOT EXIST, and so
		# is it with month 0 or day of the month 0
		if datefields[0]==0 or \
			datefields[1]==0 or \
			datefields[2]==0:
			raise pex.JDTHInvalidToken(tok)
		datestr="%4.4d-%2.2d-%2.2d %2.2d:%2.2d:%f"%(
				datefields[0],datefields[1],
				datefields[2],int(datefields[3]),
				int(datefields[4]),datefields[5])
		return datestr

	# Parse the well-behaved time string
	def getoffsetfromdate(self,datestr):
		self.jdt.year=string.atoi(datestr[0:4])
		self.jdt.month=string.atoi(datestr[5:7])
		self.jdt.day=string.atoi(datestr[8:10])
		self.jdt.hour=string.atoi(datestr[11:13])
		self.jdt.minute=string.atoi(datestr[14:16])
		self.jdt.second=string.atof(datestr[17:])
		jd0=pjd.date2jd(self.jdt)
		return jd0

	def getdatefields(self,tvalue,listlen=6):
		"""Get a date from the offset since the origin

		Get the fields of a date structure corresponding to
		the current value of time as defined by the
		units attribute of the time variable used in the constructor

		Arguments:

			'tvalue' -- time offset since te origin

		Optional argument:

			'listlen' -- Precision in the returned date. For 
				example, 1 returns the year, 3 the [year,month,day],
				etc... Defaults to 6 ([yr,mth,day,hour,min,sec]).
		"""
		if listlen<1:
			raise pex.JDTHListTooShort(listlen)
		jdval=tvalue*self.scalefactor+self.offset
		pjd.jd2date(jdval,self.jdt)
		temp=[self.jdt.year,self.jdt.month,self.jdt.day,
			self.jdt.hour,self.jdt.minute,self.jdt.second]
		return temp[:listlen]

	def gettimevalue(self,datefields,listlen=6):
		"""Returns the scaled offset since origin from the date

		"""
		if listlen<3:
			raise pex.JDTHListTooShort(listlen)
		if listlen>=1:
			self.jdt.year=int(datefields[0])
		if listlen>=2:
			self.jdt.month=int(datefields[1])
		if listlen>=3:
			self.jdt.day=int(datefields[2])
		if listlen>=4:
			self.jdt.hour=int(datefields[3])
		if listlen>=5:
			self.jdt.minute=int(datefields[4])
		if listlen>=6:
			self.jdt.second=datefields[5]
		jd=pjd.date2jd(self.jdt)
		return (jd-self.offset)/self.scalefactor

if __name__=="__main__":
	# Nobody should use this as an input, but... who knows?
	jdh=JDTimeHandler("hours since 1980 -10- 15 5",1)
	# Is it able to parse a well formatted date?
	jdh=JDTimeHandler("hour since 1981-10-15 0:0:19.89",1)
	# No hours and quite crazy, but it gets parsed anyway, risky,
	# do not try this at home......
	jdh=JDTimeHandler("day since 1982 10 15",1)
	jdh=JDTimeHandler("second since 1983 - 1- 1 1:",1)
	# This passes...., but I don't want to work too much on 
	# this bug, it would be very silly that a user set units this way
	jdh=JDTimeHandler("daysies since 1984 -10- 15 0:34",1)
	jdh=JDTimeHandler("week since 1985 -10- 15 06:1",1)
	jdh=JDTimeHandler("weeks since 1986 -10- 15 0 :3:12.4",1)
	# This passes and should not pass, because it is not correct,
	# but it is harmless, unless we start supporting timezones, which
	# is quite unlikely...
	jdh=JDTimeHandler("minutes since 1987 -10- 15 0:0 0:",1)
	jdh=JDTimeHandler("minute since 1988 -10- 15 0:0:0",1)
	# Should be able to process this, too, even though the user
	# should not use those units strings
	jdh=JDTimeHandler("hours since 1988 -10- 5 0:0  0:0",1)
	try :
		# No time zone allowed, so, this should not be parsed
		jdh=JDTimeHandler("hours since 1989 -10- 15 0:0:0 9",1)
	except:
		print "Exception!!"
		pass
	try:
		# These should not be parsed
		jdh=JDTimeHandler("hours since 0 -10- 15 0:0:0",1)
	except:
		print "Exception!!"
		pass
	try:
		# These should not be parsed
		jdh=JDTimeHandler("hours since 2000 - 0- 15 0:0:0",1)
	except:
		print "Exception!!"
		pass
	try:
		# These should not be parsed
		jdh=JDTimeHandler("hours since 10 -10- 0 0:0:0",1)
	except:
		print "Exception!!"
		pass
