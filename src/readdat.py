# Adapted for numpy/ma/cdms2 by convertcdms.py
# readdat.py

"""A simple data reader

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
# 

import string
import numpy as Numeric

def _getnewlist():
	return []

def _makevector(matrix):
	totlen = Numeric.multiply.reduce(matrix.shape)
	matrix.shape = (totlen,)
	return matrix

def _parsewithcomplexes(str):
	# In case there is a ',' in the string, it is a complex number
	if string.find(str,",")>=0:
		toks=string.split(str,",")
		if len(toks)==2 and len(toks[0])==0:
			toks[0]="0."
		if len(toks)==2 and len(toks[1])==0:
			toks[1]="0.0"
		number=string.atof(toks[0])+string.atof(toks[1])*1j
	else:
		# Just a real
		number=string.atof(str)
	return number

def readdat(fname,typecode=None):
	"""Read a NumPy array from a file
	
	Comments are allowed just begining the comment lines with '#'.
	Blank lines are also allowed. All rows must have the same number 
	of columns.

	Arguments:

		'fname' -- Name of the file to load

	Optional arguments:

		'typecode' -- The precision of the array to be read.
	"""
	seq=[]
	ifile=open(fname,"r")
	for line in ifile.readlines():
		tok=string.split(line)
		if len(tok)==0:
			continue
		if tok[0][0]!="#":
			sublist=_getnewlist()
			for i in xrange(len(tok)):
				sublist.append(_parsewithcomplexes(tok[i]))
			seq.append(sublist)
	if typecode==None:
		a=Numeric.array(seq)
	else:
		a=Numeric.array(seq).astype(typecode)
	if 1 in a.shape:  # if it is a vector ...
		a = _makevector(a)
	return a

def readstdin(typecode=None):
	"""Read a NumPy array from standard input 
	
	Optional arguments:

		'typecode' -- The precision of the array to be read.
	"""
	try: c=sys.__dict__;c=None
	except: import sys
	seq=[]
        ifile=sys.stdin
        for line in ifile.readlines():
                tok=string.split(line)
                if len(tok)==0:
                        continue
                if tok[0][0]!="#":
                        sublist=_getnewlist()
                        for i in xrange(len(tok)):
                                sublist.append(_parsewithcomplexes(tok[i]))
                        seq.append(sublist)
        if typecode==None:
                a=Numeric.array(seq)
        else:
                a=Numeric.array(seq).astype(typecode)
        if 1 in a.shape:  # if it is a vector ...
                a = _makevector(a)
        return a

def read1Ddat(fname,typecode=None):
	"""Read a one-dimensional array from a file

	This is useful when the rows in the file do not have the same 
        number of columns. Comments (begining with '#') and blank lines
	are allowed.

	Arguments:

		'fname' -- Name of the file to load

	Optional arguments:

		'typecode' -- The precision of the array to be read.
	"""
	seq=[]
	ifile=open(fname,"r")
	for line in ifile.readlines():
		tok=string.split(line)
		if len(tok)==0:
			continue
		if tok[0][0]!="#":
			for i in xrange(len(tok)):
				seq.append(_parsewithcomplexes(tok[i]))
	if typecode==None:
		a=Numeric.array(seq)
	else:
		a=Numeric.array(seq).astype(typecode)
	return a

def readcol(fname,col=1,typecode=None):
	"""Read a column of an ASCII file and load it in a NumPy array

	Columns are human-numbered (start with 1 instead of 0)

	Arguments:

		'fname' -- Name of the file to load

	Optional arguments:

		'col' -- The column number to read. Defaults to 1 
			(the first one)

		'typecode' -- The precision of the array to be read.
	
	"""
	colm1=col-1
	seq=[]
	ifile=open(fname,"r")
	for line in ifile.readlines():
		tok=string.split(line[:-1])
		if len(tok)==0:
			continue
		if tok[0][0]!="#":
			seq.append(_parsewithcomplexes(tok[colm1]))
	ifile.close()
	if typecode==None:
		a=Numeric.array(seq)
	else:
		a=Numeric.array(seq).astype(typecode)
	return a

def readcols(fname,cols=[1],typecode=None):
	"""Read a number of columns of an ASCII file and load them in a NumPy array

	Columns are human-numbered (start with 1 instead of 0)

	Arguments:

		'fname' -- Name of the file to load

	Optional arguments:

		'cols' -- A sequence containing the numbers of the columns 
			to be read. Repeated column numbers are allowed. 
			Defaults to [ 1 ] (the first one)

		'typecode' -- The precision of the array to be read.
	
	"""
	seq=[]
	ifile=open(fname,"r")
	for line in ifile.readlines():
		tok=string.split(line[:-1])
		if len(tok)==0:
			continue
		if tok[0][0]!="#":
			thisseq=_getnewlist()
			for col in cols:
				colm1=col-1
				thisseq.append(_parsewithcomplexes(tok[colm1]))
			seq.append(thisseq)
	ifile.close()
	if typecode==None:
		a=Numeric.array(seq)
	else:
		a=Numeric.array(seq).astype(typecode)
	return a


