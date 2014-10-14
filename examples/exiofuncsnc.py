# exiofuncsnc.py
# Examples on the use of NetCDF IO functions
from pyclimate.ncstruct import *
from Scientific.IO.NetCDF import * # Hinsen's netCDF extensions

inc=NetCDFFile("../test/cru_hgt.nc")
dims=("time","Z","lat","lon")
# Copy the attributes and variables, EXCEPT 'time' 
o=nccopystruct("outputdata.nc",inc,dims,dims,dims[1:])

# o is a netCDF object that can be writen to..
ovar=o.createVariable('nextvar',Float64,dims)

# Close the created data file. You can inspect it using ncdump...
o.close()
