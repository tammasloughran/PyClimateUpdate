# Adapted for numpy/ma/cdms2 by convertcdms.py
# exdiffoperators.py
#
# Some examples on the use of differential operators in the sphere
# Jon Saenz, 20000215
from Scientific.IO.NetCDF import *
from numpy.oldnumeric import *

from pyclimate.diffoperators import *

# Print the areal average for each level
def thisprint(label,field):
	print label,
	ave=add.reduce(add.reduce(field,2),1)/float(field.shape[1]*field.shape[2])
	for data in ave:
		print " %10.4f"%(data,),
	print


# Open the input NetCDF dataset
inc=NetCDFFile("../test/cru_hgt.nc")

# Start iterating. Prepare some input variables
it=inc.variables["time"]
records=it.shape[0]
ihgt=inc.variables["hgt"]
shape=ihgt.shape[1:]
levels=ihgt.shape[1]

# Read the input records, get the geostrophic wind
lats=array(inc.variables["lat"][:],Float64)
lons=array(inc.variables["lon"][:],Float64)
R=6.37e6
hgrad=HGRADIENT(lats,lons,R)
hdiv=HDIVERGENCE(lats,lons,R)
# Constants for the geostrophic wind
g=9.81
omega=7.292e-5
kgeo=g/2./omega/sin(deg2rad(lats))
print "Average of geostrophic wind and divergence of geostrophic wind"
for irec in xrange(records):
	hgtfield=array(ihgt[irec],Float64)
	ugwind=zeros(shape,Float64)
	vgwind=zeros(shape,Float64)
	gdiv=zeros(shape,Float64)
	for ilev in xrange(levels):
		thegrad=hgrad.hgradient(hgtfield[ilev,:,:])
		ucomp=-kgeo[:,NewAxis]*thegrad[1]
		vcomp=kgeo[:,NewAxis]*thegrad[0]
		ugwind[ilev,:,:]=ucomp
		vgwind[ilev,:,:]=vcomp
		gdiv[ilev,:,:]=hdiv.hdivergence(ucomp,vcomp)
	thisprint("U:    ",ugwind)
	thisprint("V:    ",vgwind)
	thisprint("div v:",gdiv)

