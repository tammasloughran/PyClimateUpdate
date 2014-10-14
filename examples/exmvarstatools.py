from pyclimate.mvarstatools import *
from pyclimate.readdat import *
data=array(readcols("../test/plnibpei.dat",[2,3,4,5,6,7]),Float64)
years=array(readcol("../test/plnibpei.dat",1))
cdata=center(data)
stddata=standardize(data)
covmat=covariancematrix(data,data)
corrmat=correlationmatrix(data,data)
detdata=zeros(data.shape,Float64)
for icol in xrange(data.shape[1]):
	detdata[:,icol],tcoefs=detrend(data[:,icol],years)
thecol=3
for iy in xrange(len(data)):
	strvalues="%6.1f "%(years[iy],)
	strvalues=strvalues+"%8.2f %8.2f %8.2f %8.2f"%(
		data[iy,thecol],cdata[iy,thecol],
		stddata[iy,thecol],detdata[iy,thecol])
	print strvalues
