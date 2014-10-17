# Adapted for numpy/ma/cdms2 by convertcdms.py
# kzcruhgt.py
# Apply the KZFilter to the CRU HGT dataset
#
# Jon Saenz, 20000308
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

import pyclimate.ncstruct 
import pyclimate.KZFilter
import numpy
import Scientific.IO.NetCDF 

kzf=pyclimate.KZFilter.KZFilter(3,3)


a=Scientific.IO.NetCDF.NetCDFFile("cru_hgt.nc")

dims=("time","Z","lat","lon")
onc=nccopystruct("kzcruhgt.tmp.nc",a,dims,dims,dims[1:])
onc.history=""
kzhgt=onc.createVariable("kzhgt",numpy.int16,dims)
kzhgt.longname="Filtered geopotential - KZ(%3d,%3d) - Cutoff frequency:%10.6f"\
		%(kzf.iterations,kzf.points,kzf.getcutofffrequency(),)

hgt=a.variables["hgt"]
it=a.variables["time"]
records=it.shape[0]
orec=0
for irec in xrange(records):
	hfield=numpy.array(hgt[irec],numpy.float64)
	filhgt=kzf.getfiltered(hfield)
	if filhgt!=None:
		kzhgt[orec]=filhgt.astype(numpy.int16)
		onc.variables["time"][orec]=it[irec]
		orec=orec+1
		onc.sync()

onc.close()

