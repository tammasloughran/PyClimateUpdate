# Adapted for numpy/ma/cdms2 by convertcdms.py
# ncstruct.py

"""Copy the structure of a COARDS compliant netCDF file

"""
#
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
# 
# Added function create_bare_COARDS(), JS, June 2001


from netCDF4 import Dataset
import numpy
import string,sys
import time

# Return the global attributes of the netCDF dataset
def _global_attributes(inc):
  return inc.__dict__.keys()

# Return the keys of the variable attributes
def _variable_attributes(inc,varname):
  return inc.variables[varname].__dict__.keys()


# Copy the contents of a variable in the input file to the output variable
# MUST BE ALIGNED !!!, so that the copying of a record variable
# may be problematic. Not sure yet about if this works for multidimensional
# variables
def _copycontents(ovar,invar):
  # At least a dimension must have already been defined,
  # use it as a record variable and so on
  maxrec=invar.shape[0]
  for irec in xrange(maxrec):
    ovar[irec]=invar[irec]
  
def nccopystruct(name,inc,dims=None,vars=None,varcontents=None):
  """Duplicate the definition of the input netCDF file in the output file

  Arguments:

    'name' -- Name of the output file                                           

    'inc' -- Input netCDF object

  Optional arguments:

    'dims' -- Tuple (list) with the name of the dimensions to be copied.
              Defaults to 'None'.

    'vars' -- Tuple (list) with the name of the variables to be copied.
              Defaults to 'None'.

    'varcontents' -- Tuple (list) with the name of the variables whose          
                     contents are to be copied. They must have been previously  
                     defined in 'vars' or otherwise. Defaults to 'None'.
  """
  onc=Dataset(name,"w")
  # Copy the datasets global attributes and append a line to the
  # history attribute
  for key in _global_attributes(inc):
    if key=="history":
      args=sys.argv
      endwith="\n"+args[0]
      for arg in args[1:]:
        endwith=endwith+" "+arg
      endwith=endwith+" "+time.ctime(time.time())
      setattr(onc,key,getattr(inc,key)+endwith)
    else:
      setattr(onc,key,getattr(inc,key))
  # Copy each of the dimensions in the input array
  if dims:
    for dim in dims:
      onc.createDimension(dim,len(inc.dimensions[dim]))
  if vars:
    for var in vars:
      invar=inc.variables[var]
      ovar=onc.createVariable(var,invar.dtype,invar.dimensions)
      for key in _variable_attributes(inc,var):
        setattr(ovar,key,getattr(invar,key))
  if varcontents:
    for var in varcontents:
      invar=inc.variables[var]
      ovar=onc.variables[var]
      _copycontents(ovar,invar)
  return onc

def create_bare_COARDS(ncname,tdat=None,zdat=None,latdat=None,londat=None):
  """Create a bare COARDS compliant netCDF file with a minimum typing

  The created file may hold 4D variables as in the COARDS standard:
  'var[time,Z,lat,lon]', but the variables may hold less dimensions
  (like in a zonal average, for instance).

  Arguments:
  
    'ncname' -- is the name of the netCDF file to be created

  Optional arguments:

    'tdat' -- Tuple with first element the NumPy array of items to be held
              ('None' for a record variable) and with second element the 
              units attribute of the created time variable. If tdat itself is
              'None', no time variable will be created (This is the default).

    'zdat' -- Tuple with two elements. The first one is the NumPy array of 
              vertical levels. The last one is the units attribute of the 
              vertical levels. If 'zdat' is None, no vertical dimension is 
              created (Default).

    'latdat' -- NumPy array of latitudes. The units attribute is set
                to degrees_north. If 'None' (default), no latitudinal 
                dimension is created.

    'londat' -- NumPy array of longitudes. The units attribute 
                is set to degrees_east. If 'None' (default), no zonal dimension 
                is created.
  """
  onc=Dataset(ncname,"w")
  onc.Conventions="COARDS"
  onc.history="pyclimate.create_bare_COARDS"
  if (not tdat) and (not zdat) and (not latdat) and (not londat):
    return None
  if tdat:
    if not tdat[0]:
      onc.createDimension("time",tdat[0])
    else:
      onc.createDimension("time",len(tdat[0]))
    tvar=onc.createVariable("time",numpy.float64,("time",))
    tvar.long_name="Time variable"
    tvar.units=tdat[1]
    if tdat[0]:
      tvar[:]=tdat[0].astype(numpy.float64)
  if zdat:
    # Only time can be of "record type"
    onc.createDimension("level",len(zdat[0]))
    zvar=onc.createVariable("level",zdat[0].dtype.char,("level",))
    zvar.long_name="Vertical coordinate"
    zvar.units=zdat[1]
    zvar[:]=zdat[0]
  if latdat:
    onc.createDimension("lat",len(latdat))
    latvar=onc.createVariable("lat",latdat.dtype.char,("lat",))
    latvar.long_name="Meridional coordinate"
    latvar.units="degrees_north"
    latvar[:]=latdat[:]
  if londat:
    onc.createDimension("lon",len(londat))
    lonvar=onc.createVariable("lon",londat.dtype.char,("lon",))
    lonvar.long_name="Zonal coordinate"
    lonvar.units="degrees_east"
    lonvar[:]=londat[:]
  return onc
