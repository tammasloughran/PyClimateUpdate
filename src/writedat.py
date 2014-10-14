# Adapted for numpy/ma/cdms2 by convertcdms.py
# writedat.py

"""A simple ascii data writer

"""
# 
# Copyright (C) 2000, Jesus Fernandez, Jon Saenz and Juan Zubillaga
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
# jff20010402
# removed the from ... import sentence..
import numpy.oldnumeric as Numeric
import pyclimate.pyclimateexcpt

def _buildcomplex(c,fmt):
  return "%s,%s"%((fmt%c.real).strip(),(fmt%c.imag).strip())

def writedat(fname, matrix, header="", formatstring="%g"):
  """Dumps a one- or two-dimensional NumPy array into a file

  One-dimensional arrays are dumped as a column

  Arguments:

    'fname' -- Output file name

    'matrix' -- NumPy array to dump (one- or two-dimensional)

  Optional arguments:

    'header' -- Header lines for the file. Remember to provide
                the appropiate first character on each line 
                if you want them to be considered as comment.

    'formatstring' -- A python format string to specify the format
                      in which the array will be written. A single
                      blank space will be added between each record.
                      Defaults to "%g"

  """
  theshape=matrix.shape
  tcode=matrix.dtype.char
  iscomplex=(tcode==Numeric.Complex32 or tcode==Numeric.Complex64)
  formatstring = formatstring.strip()
  if len(theshape)>2:
    raise pyclimate.pyclimateexcpt.WrongWriteDimensions(len(theshape))
  ofile = open(fname, "w")
  if header:
    ofile.write(header)
    if header[-1]!='\n': ofile.write("\n")
  records=matrix.shape[0]
  if iscomplex:
    if len(matrix.shape) == 2:
      for i in range(records):
        ofile.write("%s" % _buildcomplex(matrix[i,0],formatstring))
        for j in range(1,matrix.shape[1]):
          ofile.write(" %s" % _buildcomplex(matrix[i,j],formatstring))
        ofile.write("\n")
    else:
      for i in range(records):
        ofile.write("%s\n" % _buildcomplex(matrix[i],formatstring))
  else:
    if len(matrix.shape) == 2:
      for i in range(records):
        ofile.write(formatstring%matrix[i,0])
        for j in range(1,matrix.shape[1]):
          ofile.write(" %s"%(formatstring%matrix[i,j],))
        ofile.write("\n")
    else:
      for i in range(records):
        ofile.write("%s\n"%(formatstring%matrix[i],))
  ofile.close()

# jff20021003
