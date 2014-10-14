# Adapted for numpy/ma/cdms2 by convertcdms.py
# exjdtime.py
# Examples on the use of the Julian Day computations
# and NetCDF time handler (JDTimeHandler)
from pyclimate.JDTime import *
from pyclimate.JDTimeHandler import *
from Scientific.IO.NetCDF import *
from numpy.oldnumeric import *


# Instance of Julian Day structure
jdt=JDTime()
date0=(1958,1,15)
jdt.year, jdt.month,jdt.day=date0 # Other fields initialized to 0
jd0=date2jd(jdt)

# Create an exact monthly interval in an output netCDF file
onc=NetCDFFile('times.nc','w')
onc.createDimension('time',None)
ovar=onc.createVariable('time',Float64,('time',))
ovar.units='hours since %4.4d-%2.2d-%2.2d 0:0:0'%date0
tstep=monthlystep()*24.
for orec in xrange(200):
    ovar[orec]=orec*tstep
onc.close()
# For input, assuming the same definition for the units attribute
# and show the use of JDTimeHandler
inc=NetCDFFile('times.nc')
ivar=inc.variables['time']
jdth=JDTimeHandler(ivar.units)
for irec in xrange(ivar.shape[0]):
    jd2date((ivar[irec]/24.+jd0),jdt)
    dtfields=jdth.getdatefields(ivar[irec],3)
    print "%4.4d-%2.2d-%2.2d %4.4d-%2.2d-%2.2d"%(jdt.year,
       jdt.month,jdt.day,dtfields[0],dtfields[1],dtfields[2])
inc.close()
