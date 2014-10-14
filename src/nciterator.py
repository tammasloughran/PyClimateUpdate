# Adapted for numpy/ma/cdms2 by convertcdms.py
# nciterator.py

"""Multiple NetCDF files iterator

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

from netCDF4 import Dataset
import numpy as Numeric

class nciterator:
	"Multiple NetCDF files iterator"
	def __init__(self,namelist,tvarname):
		"""Constructor for the class 'nciterator'

		Arguments:

			'namelist' -- List of NetCDF file names to iterate over

			'tvarname' -- Name of the NetCDF time variable
		"""
		self.list=[]
		self.reclist=[]
		self.totalrecs=0
		for n in namelist:
			nc=Dataset(n,"r")
			self.list.append(nc)
			it=len(nc.variables[tvarname])
			self.totalrecs=self.totalrecs+it
			self.reclist.append(self.totalrecs)
		self.reclist=Numeric.array(self.reclist)

	def __len__(self):
		"Total iterator records"
		return self.totalrecs

	def getncitem(self,irec):
		"Returns an open NetCDFFile where the record 'irec' is located"
		if irec>=self.totalrecs:
			raise ValueError
		passed=Numeric.less_equal(self.reclist,irec)
		return Numeric.add.reduce(passed)

	def getncrec(self,irec,inc):
		"Returns the 'inc' NetCDFFile record corresponding to the 'irec' global record"
		if irec>=self.totalrecs:
			raise ValueError
		if inc>0:
			return irec-self.reclist[inc-1]
		else:
			return irec
		
	def getfield(self,varname,irec):
		"Returns a NumPy array with the 'varname' corresponding to the 'irec' global record"
		inc=self.getncitem(irec)
		localrec=self.getncrec(irec,inc)
		return	self.list[inc].variables[varname][localrec]

if __name__=="__main__":
	import glob
	files=glob.glob("MCsamples/wet*nc")
	files.sort()
	ncit=nciterator(files,"time")
	print len(ncit)
	print ncit.reclist

	recno=2
	print "recno:",recno
	print "INC:",ncit.getncitem(recno),0
	print "REC:", ncit.getncrec(recno,ncit.getncitem(recno)),0

	recno=3000
	print "recno:",recno
	print "INC:",ncit.getncitem(recno),1
	print "REC:", ncit.getncrec(recno,ncit.getncitem(recno)),0

	recno=2999
	print "recno:",recno
	print "INC:",ncit.getncitem(recno),0
	print "REC:", ncit.getncrec(recno,ncit.getncitem(recno)),2999

	recno=5999
	print "recno:",recno
	print "INC:",ncit.getncitem(recno),1
	print "REC:", ncit.getncrec(recno,ncit.getncitem(recno)),2999

	recno=6000
	print "recno:",recno
	print "INC:",ncit.getncitem(recno),2
	print "REC:", ncit.getncrec(recno,ncit.getncitem(recno)),0
	
	recno=9433
	print "recno:",recno
	print "INC:",ncit.getncitem(recno),3
	print "REC:", ncit.getncrec(recno,ncit.getncitem(recno)),0

	recno=12433
	print "recno:",recno
	print "INC:",ncit.getncitem(recno),3
	print "REC:", ncit.getncrec(recno,ncit.getncitem(recno)),0

