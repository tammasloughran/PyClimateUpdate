# Adapted for numpy/ma/cdms2 by convertcdms.py
# pyclimatetest.py
#
# Test most of the functions in pyclimate
#
# For version 1.0
#
# Jon Saenz, 20001015
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
#
import sys
import os
import getopt
#import Scientific.IO.NetCDF
from netCDF4 import Dataset
import numpy

# Now, import pyclimate's features
####################################
import pyclimate.readdat
import pyclimate.ncstruct
import pyclimate.JDTime
import pyclimate.JDTimeHandler
import pyclimate.pydcdflib
import pyclimate.mvarstatools
import pyclimate.svdeofs
import pyclimate.svd
import pyclimate.KZFilter
import pyclimate.LanczosFilter
import pyclimate.diffoperators
import pyclimate.KPDF
import pyclimate.pyclimateexcpt
import pyclimate.asciidat
import pyclimate.tools
import pyclimate.bpcca
import pyclimate.analog
import pyclimate.NHArray

# Some global estetical definitions
##########################################
TOLERANCE=1.0e-15
ERROR_FLAG="X"
OK_FLAG=" "
SEPARATOR1="="*60
SEPARATOR2="="*60

def usage(pname):
  print "%s [-h] [-o] [-g]"%(pname,)
  print "-h Show this message"
  print "-o Overwrite the reference files"
  print "-g Get the reference file using urllib even if it exists"
  sys.exit(1)

def reduceall(a):
  ndims = len(a.shape)
  for idim in range(ndims):
    a = numpy.add.reduce(a)
  return a

# If overwriting, create the variables...
# Otherwise, compute the Root-Mean-Square Error
def compareRMSvals(nc,varname,val,ovwr,dims,optlabel=""):
  if ovwr:
    var=nc.createVariable(varname,val.dtype.char,dims)
    var[:]=val[:]
  else:
    ref=nc.variables[varname][:]
    try:
      residual=ref-val
    except:
      return
    itimes=len(residual.shape)
    res2=residual*residual
    nshape=numpy.array(val.shape)
    N=numpy.multiply.reduce(nshape)
    rms=numpy.sqrt(numpy.add.reduce(numpy.ravel(res2))/N)
    if rms>TOLERANCE:
      statusflag=ERROR_FLAG
    else:
      statusflag=OK_FLAG
    print "%s RMS Error |%-30s| : %12.3e %s"%(statusflag,varname,rms,optlabel)
    sys.stdout.flush()

# Compute the Root-Mean-Square Error
# WITHOUT storing in nor comparing with the NetCDF reference file.
def comparememoryvals(label,val,val1,optlabel=""):
  residual=numpy.ravel(val1)-numpy.ravel(val)
  N=len(residual)
  res2=residual*residual
  temp=numpy.add.reduce(res2)
  rms=abs(numpy.sqrt(temp/N))
  if rms>TOLERANCE:
    statusflag=ERROR_FLAG
  else:
    statusflag=OK_FLAG
  print "%s RMS Error |%-30s| : %12.3e %s"%(statusflag,label,rms,optlabel)
  sys.stdout.flush()


# If overwriting, create the variables...
# Otherwise, compute the congruence coefficient
# Computes all crossed congruences along the LAST axis!!! (EOF storage type)
def compareGvals(nc,varname,val,ovwr,dims,optlabel=""):
  if ovwr:
    var=nc.createVariable(varname,val.dtype.char,dims)
    var[:]=val[:]
  else:
    ref=nc.variables[varname][:]
    eofs=val.shape[-1]
    for ieof in xrange(eofs):
      eofref=ref[...,ieof]
      eofval=ref[...,ieof]
      normref=numpy.sqrt(reduceall(eofref*eofref))
      normval=numpy.sqrt(reduceall(eofval*eofval))
      dotprod=reduceall(eofref*eofval)
      gcoeff=dotprod/normref/normval
      dg=1.-abs(gcoeff)
      if dg>TOLERANCE:
        statusflag=ERROR_FLAG
      else:
        statusflag=OK_FLAG
      print "%s G_%2.2d_%2.2d   |%-30s| : %12.3e  dG:%12.5e %s"%(
        statusflag,ieof,ieof,varname,gcoeff,dg,optlabel
      )
      sys.stdout.flush()

# Test the ASCII IO functions
def testIOASCII(ovw,nc):
  R=pyclimate.readdat
  A=pyclimate.asciidat
  fname="datawithcomplex.dat"
  data1=R.readdat(fname)
  A.writedat("pepe.tmp",data1,"# I am pepe")
  data1dot=A.readdat(fname)
  data1dotdot=A.readdat("pepe.tmp")
  item=0
  comparememoryvals("ASCII-READDAT %2d"%(item,),data1,data1dot)
  item=item+1
  comparememoryvals("ASCII-READDAT %2d"%(item,),data1,data1dotdot)
  dataf=R.readdat(fname,numpy.float32)
  datafdot=A.readdat(fname,numpy.float32)
  A.writedat("pepe2.tmp",dataf)
  item=item+1
  comparememoryvals("ASCII-READDAT %2d"%(item,),dataf,datafdot)
  datafdot=A.readdat("pepe2.tmp",numpy.float32)
  item=item+1
  comparememoryvals("ASCII-READDAT %2d"%(item,),dataf,datafdot)
  os.system("rm pepe*tmp")
  datac=R.readdat(fname,numpy.complex64)
  datab=R.readdat(fname,numpy.int16)
  data2=R.readcol(fname,2,numpy.int16)
  data2c=R.readcol(fname,2,numpy.complex128)
  data2cdot=A.readcol(fname,2,numpy.complex128)
  item=item+1
  comparememoryvals("ASCII-READDAT %2d"%(item,),dataf,datafdot)
  data13=R.readcols(fname,(1,3))
  data13f=R.readcols(fname,(1,3),numpy.float32)
  data13fdot=A.readcols(fname,(1,3),numpy.float32)
  item=item+1
  comparememoryvals("ASCII-READDAT %2d"%(item,),data13f,data13fdot)
  if ovw:
    nc.createDimension("datarows",len(data1))
    nc.createDimension("datacols",len(data1[0]))
    nc.createDimension("two",2)
  compareRMSvals(nc,"data1r",data1.real,ovw,("datarows","datacols"))
  compareRMSvals(nc,"data1i",data1.imag,ovw,("datarows","datacols"))
  compareRMSvals(nc,"dataf",dataf,ovw,("datarows","datacols"))
  compareRMSvals(nc,"datacr",datac.real,ovw,("datarows","datacols"))
  compareRMSvals(nc,"dataci",datac.imag,ovw,("datarows","datacols"))
  compareRMSvals(nc,"datab",datab,ovw,("datarows","datacols"))
  compareRMSvals(nc,"data2",data2,ovw,("datarows",))
  compareRMSvals(nc,"data2r",data2c.real,ovw,("datarows",))
  compareRMSvals(nc,"data2i",data2c.imag,ovw,("datarows",))
  compareRMSvals(nc,"data13r",data13.real,ovw,("datarows","two"))
  compareRMSvals(nc,"data13i",data13.imag,ovw,("datarows","two"))
  compareRMSvals(nc,"data13f",data13f,ovw,("datarows","two"))

def title(text,ovw):
  print
  if ovw:
    print "Generating references for routines:",text
  else:
    print "Testing routines:",text
  print SEPARATOR1

def testIOnc(ovw):
  inc=Dataset("cru_hgt.nc")
  dims=("time","Z","lat","lon")
  vars=dims
  vars1=dims[1:]
  onc=pyclimate.ncstruct.nccopystruct("temp.nc",inc,dims,vars,vars1)
  onc.close()
  if not ovw:
    print
    print "*"*60
    print "The test of ncstruct.py is not automated"
    print "If it does not throw any exception, it is probably"
    print "working properly. If you want to be sure, "
    print "please, check using ncdump that temp.nc and cru_hgt.nc"
    print "have equal structures."
    print "You can also use temp.cdl.ref with diff and ncdump"
    print "*"*60
    print

def date2array(a):
  return numpy.array([a.year,a.month,a.day,a.hour,a.minute,a.second])

def assigndate(jd,dtuple,jday):
  jd.year=dtuple[0]
  jd.month=dtuple[1]
  jd.day=dtuple[2]
  jd.hour=dtuple[3]
  jd.minute=dtuple[4]
  jd.second=dtuple[5]
  ttuple=dtuple[:5]+(int(dtuple[5]),)
  tstr="day%4.4d%2.2d%2.2d_%2.2d%2.2d%2.2d"%ttuple
  return numpy.array([pyclimate.JDTime.date2jd(jd),jday]),tstr

def testJDTime(nc,ovw):
  if ovw:
    nc.createDimension("singleval",1)
    nc.createDimension("doubleval",2)
    nc.createDimension("datefield",6)
  mstep=numpy.array([pyclimate.JDTime.monthlystep()])
  compareRMSvals(nc,"mstep",mstep,ovw,("singleval",))
  a=pyclimate.JDTime.JDTime()
  # 1999-02-12 is JD= 2451222
  jd=2451222.0
  pyclimate.JDTime.jd2date(jd,a)
  aar=date2array(a)
  compareRMSvals(nc,"day19990212",aar,ovw,("datefield",))
  ainv=numpy.array([pyclimate.JDTime.date2jd(a),2451222.])
  compareRMSvals(nc,"day19990212JD",ainv,ovw,("doubleval",))
  # Several dates from Calendar FAQ,
  # quasar.as.utexas.edu/Billinfo/JulianDatesG.html
  # Duffet-Smith, 1990
  # And Jean Meeus, 1991
  ##########################################
  # noon UTC 1 Jan AD 2000, JD-> 2451545
  # 15:00 UTC 1 Jan AD 2000, JD-> 2451545.125
  jdt=pyclimate.JDTime.JDTime()
  ainv,tstr=assigndate(jdt,(2000,1,1,12,0,0),2451545.)
  compareRMSvals(nc,tstr,ainv,ovw,("doubleval",))
  ainv,tstr=assigndate(jdt,(2000,1,1,15,0,0),2451545.125)
  compareRMSvals(nc,tstr,ainv,ovw,("doubleval",))
  jdarr,tstr=assigndate(jdt,(1752,9,14,12,0,0),2361222)
  compareRMSvals(nc,tstr,jdarr,ovw,("doubleval",))
  jdarr,tstr=assigndate(jdt,(1858,11,16,12,0,0),2400000)
  compareRMSvals(nc,tstr,jdarr,ovw,("doubleval",))
  jdarr,tstr=assigndate(jdt,(1,1,1,12,0,0),1721426)
  compareRMSvals(nc,tstr,jdarr,ovw,("doubleval",))
  jdarr,tstr=assigndate(jdt,(1996,9,3,12,0,0),2450330)
  compareRMSvals(nc,tstr,jdarr,ovw,("doubleval",))
  jdarr,tstr=assigndate(jdt,(1989,12,31,0,0,0),2450330)
  compareRMSvals(nc,tstr,jdarr,ovw,("doubleval",))
  # This time is quite messy.
  # We extrapolate the Gregorian calendar, thus, 
  # -4713-11-24 (Gregorian)==-4712-01-01 (Julian)
  jdarr,tstr=assigndate(jdt,(-4713,11,24,12,0,0),0)
  compareRMSvals(nc,tstr,jdarr,ovw,("doubleval",))
  jdarr,tstr=assigndate(jdt,(1600,1,1,0,0,0),2305447.5)
  compareRMSvals(nc,tstr,jdarr,ovw,("doubleval",))
  jdarr,tstr=assigndate(jdt,(1988,1,27,0,0,0),2447187.5)
  compareRMSvals(nc,tstr,jdarr,ovw,("doubleval",))

def testJDTimeHandler(nc,ovw):
  inc=Dataset("cru_hgt.nc")
  itime=inc.variables["time"]
  irecords=itime.shape[0]
  jdth=pyclimate.JDTimeHandler.JDTimeHandler(itime.units)
  arrdates=numpy.zeros((irecords,6),numpy.float64)
  for irec in xrange(irecords):
    iy,im,id,ih,imin,isec=jdth.getdatefields(itime[irec],6)
    arrdates[irec,:]=numpy.array([iy,im,id,ih,imin,isec],numpy.float64)
  if ovw:
    nc.createDimension("hgtrecords",irecords)
  compareRMSvals(nc,"hgtdate",arrdates,ovw,("hgtrecords","datefield"))
  # Up to now, the inspection of the reference file allows us to
  # see whether we are decoding correctly the date
  # fields in the time variable. Let's go to see if we encode them
  # properly
  arrjds=numpy.zeros((irecords,2),numpy.float64)
  for irec in xrange(irecords):
    arrjds[irec,0]=jdth.gettimevalue(arrdates[irec])
    arrjds[irec,1]=itime[irec]
  compareRMSvals(nc,"hgttimes",arrjds,ovw,("hgtrecords","doubleval"))
  res=arrjds[:,0]-arrjds[:,1]
  rms=numpy.sqrt(numpy.add.reduce(res*res)/len(res))
  if rms>TOLERANCE:
    statusflag=ERROR_FLAG
  else:
    statusflag=OK_FLAG
  print "%s RMS Error |%-30s| : %12.3e seconds"%(statusflag,"t-t'",rms*3600)
  print
  print "*"*40
  print "The last result (t-t') may be grater than zero. It does"
  print "not mean that pyclimate is working unproperly. It just"
  print "measures the expected accuracy of JDTimeHandler()"
  print "during 50 years, with the changes due to truncation"
  print "errors derived from different ways to compute t and t'"
  print "A result of order 1e-4 or lower seems OK"
  print "*"*40
  print
  inc.close()

def dcdflibtest(dcd,nc,ov,whichstr,init=0):
  print "Performing test of",whichstr
  Ps=numpy.array([0.9,0.95,0.99,0.995])
  dofs=numpy.array([5.,10.,15.,20.,25.,30.])
  Xs=numpy.arange(0.5,4.05,0.5)
  if ov and init:
    nc.createDimension("probs",len(Ps))
    nc.createDimension("dofs",len(dofs))
    nc.createDimension("Xs",len(Xs))
    nc.createVariable("Ps",numpy.float64,("probs",))[:]=Ps[:]
    nc.createVariable("dofs",numpy.float64,("dofs",))[:]=dofs[:]
    nc.createVariable("Xs",numpy.float64,("Xs",))[:]=Xs[:]
  if whichstr=="Chi**2":
    f=dcd.CDFChi()
    f.which=2
    thetable=numpy.zeros((len(Ps),len(dofs)),numpy.float64)
    for ip in xrange(len(Ps)):
      for idof in xrange(len(dofs)):
        f.p=Ps[ip]
        f.df=dofs[idof]
        dcd.pycdfchi(f)
        if f.status!=0:
          print "Failed",whichstr,"with status",
          print f.status
          return
        thetable[ip,idof]=f.x
    varname="chitable"
    dims=("probs","dofs")
  elif whichstr=="Normal":
    f=dcd.CDFNor()
    f.which=1
    f.mean=0.0
    f.sd=1.
    thetable=numpy.zeros((len(Xs),2),numpy.float64)
    for ix in xrange(len(Xs)):
      f.x=Xs[ix]
      dcd.pycdfnor(f)
      if f.status!=0:
        print "Failed",whichstr,"with status",
        print f.status
        return
      thetable[ix,0]=f.p
      thetable[ix,1]=f.q
    varname="normaltable"
    dims=("Xs","two")
  elif whichstr=="T":
    f=dcd.CDFT()
    f.which=2
    thetable=numpy.zeros((len(Ps),len(dofs)),numpy.float64)
    for ip in xrange(len(Ps)):
      f.p=Ps[ip]
      for id in xrange(len(dofs)):
        f.df=dofs[id]
        dcd.pycdft(f)
        if f.status!=0:
          print "Failed",whichstr,"with status",
          print f.status
          return
        thetable[ip,id]=f.t
    varname="ttable"
    dims=("probs","dofs")
  else:
    print "Unable to handle this distribution!!",whichstr
    print "TEST SKIPPED!!",whichstr
  compareRMSvals(nc,varname,thetable,ov,dims)

# Test the access to DCDFLIB.C
def testpydcdflib(nc,ov):
  dcd=pyclimate.pydcdflib # Save some typing
  print 
  print "*"*60
  print "This set of tests for the access to DCDFLIB are not very"
  print "exhaustive, because their only aim is to test whether"
  print "the compilation of the C sources and the floating point"
  print "model of the target machine and the selections in ipmpar.c"
  print "are correct. If these results are accurate, you can"
  print "probably be certain that your version of pydcdflib"
  print "is correct. In any case, the source testDCDFLIB.py"
  print "executes a really exhaustive set of tests over all the"
  print "functions in DCDFLIB with all the combinations of parameters"
  print "and you can check the results with testDCDFLIB.ref using diff"
  print "*"*60
  print
  dcdflibtest(dcd,nc,ov,"Chi**2",1)
  dcdflibtest(dcd,nc,ov,"Normal")
  dcdflibtest(dcd,nc,ov,"T")


def testEOFs(nc,ov):
  # First case: Chemical.dat example, at Jackson, 1991
  eof=pyclimate.svdeofs
  chemdata=pyclimate.readdat.readdat("chemical.dat")
  Zs,lambdas,Es=eof.svdeofs(chemdata)
  varfrac=eof.getvariancefraction(lambdas)
  north=eof.northtest(lambdas,len(chemdata))
  if ov:
    nc.createDimension("c_samples",len(chemdata))
    nc.createDimension("c_channels",len(chemdata[0]))
  compareGvals(nc,"chem_pc",Zs,ov,("c_samples","c_channels"))
  compareGvals(nc,"chem_eofs",Es,ov,("c_channels","c_channels"))
  compareRMSvals(nc,"chem_lambdas",lambdas,ov,("c_channels",))
  compareRMSvals(nc,"chem_varfrac",varfrac,ov,("c_channels",))
  compareRMSvals(nc,"chem_north",north,ov,("c_channels",))
  # Now, a less trivial case...
  inc=Dataset("cru_hgt.nc")
  hgtdata=numpy.array(inc.variables["hgt"][:,:,:,:],numpy.float64)
  hgtdata2=hgtdata[:,:,:,:]
  oldshape=hgtdata.shape
  newshape=(oldshape[0],oldshape[1]*oldshape[2]*oldshape[3])
  hgtdata.shape=newshape
  Zs,lambdas,Es=eof.svdeofs(hgtdata)
  Es = numpy.array(Es) # to get a contiguous array
  pcfieldcorr=eof.pcseriescorrelation(Zs,Es,hgtdata)
  Es.shape=oldshape[1:]+Es.shape[-1:]
  pcfieldcorr.shape=Es.shape
  varfrac=eof.getvariancefraction(lambdas)
  north=eof.northtest(lambdas,len(hgtdata))
  # and multichannel
  Zs_mult,lambdas_mult,Es_mult=eof.svdeofs(hgtdata2)
  varfrac_mult=eof.getvariancefraction(lambdas_mult)
  north_mult=eof.northtest(lambdas_mult,len(hgtdata2))  
  pcfieldcorr_mult=eof.pcseriescorrelation(Zs_mult,Es_mult,hgtdata2)
  if ov:
    nc.createDimension("h_samples",len(hgtdata2))
    nc.createDimension("h_channelz",hgtdata2.shape[1])
    nc.createDimension("h_channellat",hgtdata2.shape[2])
    nc.createDimension("h_channellon",hgtdata2.shape[3])
    nc.createDimension("neofs",Es.shape[-1])
    compareGvals(nc,"hgt_pc",Zs_mult,ov,("h_samples","neofs"))
    compareGvals(nc,"hgt_eofs",Es_mult,ov,("h_channelz","h_channellat","h_channellon","neofs"))
    compareRMSvals(nc,"hgt_lambdas",lambdas_mult,ov,("neofs",))
    compareRMSvals(nc,"hgt_varfrac",varfrac_mult,ov,("neofs",))
    compareRMSvals(nc,"hgt_north",north_mult,ov,("neofs",))
    compareRMSvals(nc,"hgt_pccorr",pcfieldcorr_mult,ov,("h_channelz","h_channellat","h_channellon","neofs"))
  else:
    compareGvals(nc,"hgt_pc",Zs,ov,("h_samples","neofs"))
    compareGvals(nc,"hgt_eofs",Es,ov,("h_channelz","h_channellat","h_channellon","neofs"))
    compareRMSvals(nc,"hgt_lambdas",lambdas,ov,("neofs",))
    compareRMSvals(nc,"hgt_varfrac",varfrac,ov,("neofs",))
    compareRMSvals(nc,"hgt_north",north,ov,("neofs",))
    compareRMSvals(nc,"hgt_pccorr",pcfieldcorr,ov,("h_channelz","h_channellat","h_channellon","neofs"))
  inc.close()

def testnewEOFs(nc,ov):
  print "For this test, G_i_j means congruence coefficient, and should"
  print "be one or minus one for a successful run"
  print
  # First case: Chemical.dat example, at Jackson, 1991
  chemdata=pyclimate.readdat.readdat("chemical.dat")
  eofobj=pyclimate.svdeofs.SVDEOFs(chemdata)
  varfrac=eofobj.varianceFraction()
  north=eofobj.northTest()
  if ov:
    pass     # Variables are created by testEOFs()
  else:
    compareGvals(nc,"chem_pc",eofobj.pcs(),ov,("c_samples","c_channels"))
    compareGvals(nc,"chem_eofs",eofobj.eofs(),ov,("c_channels","c_channels"))
    compareRMSvals(nc,"chem_lambdas",eofobj.lambdas,ov,("c_channels",))
    compareRMSvals(nc,"chem_varfrac",varfrac,ov,("c_channels",))
    compareRMSvals(nc,"chem_north",north,ov,("c_channels",))
  # Now, a less trivial case in multichannel...
  inc=Dataset("cru_hgt.nc")
  hgtdata=numpy.array(inc.variables["hgt"][:,:,:,:],numpy.float64)
  eofobj=pyclimate.svdeofs.SVDEOFs(hgtdata)
  pcfieldcorr=eofobj.eofsAsCorrelation()
  varfrac=eofobj.varianceFraction()
  north=eofobj.northTest()
  if ov:
    pass     # Variables are created by testEOFs()
  else:
    compareGvals(nc,"hgt_pc",eofobj.pcs(),ov,("h_samples","neofs"))
    compareGvals(nc,"hgt_eofs",eofobj.eofs(),ov,("h_channelz","h_channellat","h_channellon","neofs"))
    compareRMSvals(nc,"hgt_lambdas",eofobj.lambdas,ov,("neofs",))
    compareRMSvals(nc,"hgt_varfrac",varfrac,ov,("neofs",))
    compareRMSvals(nc,"hgt_north",north,ov,("neofs",))
    compareRMSvals(nc,"hgt_pccorr",pcfieldcorr,ov,("h_channelz","h_channellat","h_channellon","neofs"))
  inc.close()


def testSVD(nc,ov):
  s=pyclimate.svd
  inc=Dataset("cru_hgt.nc")
  # Geopotential height in a reduced domain around the Iberian Peninsula
  hgtdata=numpy.array(inc.variables["hgt"][:,1,:,:],numpy.float64)
  oldshape=hgtdata.shape
  newshape=(oldshape[0],oldshape[1]*oldshape[2])
  hgtdata.shape=newshape
  # Precipitation over the northern Iberian Peninsula
  pldata=pyclimate.readdat.readcols("plnibpei.dat",[2,3,4,5,6,7])
  U,sigmas,V=s.svd(hgtdata,pldata)
  hcoefs=s.getcoefs(hgtdata,U)
  pcoefs=s.getcoefs(pldata,V)
  scf=s.SCF(sigmas)
  cscf=s.CSCF(sigmas)
  holmaps=s.homogeneousmaps(hgtdata,U)
  hormaps=s.homogeneousmaps(pldata,V)
  helmaps=s.heterogeneousmaps(hgtdata,pcoefs)
  hermaps=s.heterogeneousmaps(pldata,hcoefs)
  # and multichannel
  hgtdata.shape=oldshape
  U_mult,sigmas_mult,V_mult=s.svd(hgtdata,pldata)
  U_mult.shape = (U_mult.shape[0]*U_mult.shape[1], U_mult.shape[2])
  hcoefs_mult=s.getcoefs(hgtdata,U_mult)
  pcoefs_mult=s.getcoefs(pldata,V_mult)
  scf_mult=s.SCF(sigmas_mult)
  cscf_mult=s.CSCF(sigmas_mult)
  holmaps_mult=s.homogeneousmaps(hgtdata,U_mult)
  holmaps_mult.shape = (holmaps_mult.shape[0]*holmaps_mult.shape[1], holmaps_mult.shape[2])
  hormaps_mult=s.homogeneousmaps(pldata,V_mult)
  helmaps_mult=s.heterogeneousmaps(hgtdata,pcoefs_mult)
  helmaps_mult.shape = (helmaps_mult.shape[0]*helmaps_mult.shape[1], helmaps_mult.shape[2])
  hermaps_mult=s.heterogeneousmaps(pldata,hcoefs_mult)
  # Well, compare everything...
  if ov:
    nc.createDimension("svdsamples",len(pldata))
    nc.createDimension("plsites",len(pldata[0]))
    nc.createDimension("hsites",U.shape[0])
    nc.createDimension("singvalues",len(sigmas))
    compareRMSvals(nc,"svdsigmas",sigmas,ov,("singvalues",))
    compareRMSvals(nc,"svdscf",scf,ov,("singvalues",))
    compareRMSvals(nc,"svdcscf",cscf,ov,("singvalues",))
    compareGvals(nc,"hcoefs",hcoefs,ov,("svdsamples","singvalues"))
    compareGvals(nc,"pcoefs",pcoefs,ov,("svdsamples","singvalues"))
    compareGvals(nc,"svdU",U,ov,("hsites","singvalues"))
    compareGvals(nc,"svdV",V,ov,("plsites","singvalues"))
    compareGvals(nc,"holmaps",holmaps,ov,("hsites","singvalues"))
    compareGvals(nc,"hormaps",hormaps,ov,("plsites","singvalues"))
    compareGvals(nc,"helmaps",helmaps,ov,("hsites","singvalues"))
    compareGvals(nc,"hermaps",hermaps,ov,("plsites","singvalues"))
  else:  
    compareRMSvals(nc,"svdsigmas",sigmas_mult,ov,("singvalues",))
    compareRMSvals(nc,"svdscf",scf_mult,ov,("singvalues",))
    compareRMSvals(nc,"svdcscf",cscf_mult,ov,("singvalues",))
    compareGvals(nc,"hcoefs",hcoefs_mult,ov,("svdsamples","singvalues"))
    compareGvals(nc,"pcoefs",pcoefs_mult,ov,("svdsamples","singvalues"))
    compareGvals(nc,"svdU",U_mult,ov,("hsites","singvalues"))
    compareGvals(nc,"svdV",V_mult,ov,("plsites","singvalues"))
    compareGvals(nc,"holmaps",holmaps_mult,ov,("hsites","singvalues"))
    compareGvals(nc,"hormaps",hormaps_mult,ov,("plsites","singvalues"))
    compareGvals(nc,"helmaps",helmaps_mult,ov,("hsites","singvalues"))
    compareGvals(nc,"hermaps",hermaps_mult,ov,("plsites","singvalues"))
  inc.close()

def testCCA(nc,ov):
  c=pyclimate.bpcca
  inc=Dataset("cru_hgt.nc")
  # Geopotential height in a reduced domain around the Iberian Peninsula
  hgtdata=numpy.array(inc.variables["hgt"][:,:,:,:],numpy.float64)
  hgtdata2 = numpy.array(hgtdata[:,:,:,:])    # for multichannel test
  oldshape=hgtdata.shape
  newshape=(oldshape[0],oldshape[1]*oldshape[2]*oldshape[3])
  hgtdata.shape=newshape
  # Precipitation over the northern Iberian Peninsula
  pldata=pyclimate.readdat.readcols("plnibpei.dat",[2,3,4,5,6,7])
  cc=c.BPCCA(hgtdata,pldata,(4,2))
  ccap=cc.leftPatterns()
  ccap.shape=oldshape[1:]+ccap.shape[-1:]
  ccaq=cc.rightPatterns()
  ccaa=cc.leftExpCoeffs()
  ccab=cc.rightExpCoeffs()
  ccacorr=cc.correlation()
  ccapfrac, ccaqfrac=cc.getVarianceFractions()
  # and multichannel
  cc2=c.bpcca(hgtdata2,pldata,(4,2))
  ccap_mult=cc2.leftPatterns()
  ccaq_mult=cc2.rightPatterns()
  ccaa_mult=cc2.leftExpCoeffs()
  ccab_mult=cc2.rightExpCoeffs()
  ccacorr_mult=cc2.correlation()
  ccapfrac_mult, ccaqfrac_mult=cc2.getVarianceFractions() 
  # Well, compare everything...
  if ov:
    nc.createDimension("ccasamples",len(pldata))
    nc.createDimension("hsitesz",hgtdata2.shape[1])
    nc.createDimension("hsiteslat",hgtdata2.shape[2])
    nc.createDimension("hsiteslon",hgtdata2.shape[3])
    nc.createDimension("cancorr",len(ccacorr))
    compareRMSvals(nc,"ccacorr",ccacorr_mult,ov,("cancorr",))
    compareRMSvals(nc,"ccapfrac",ccapfrac_mult,ov,("cancorr",))
    compareRMSvals(nc,"ccaqfrac",ccaqfrac_mult,ov,("cancorr",))
    compareGvals(nc,"ccap",ccap_mult,ov,("hsitesz","hsiteslat","hsiteslon","cancorr"))
    compareGvals(nc,"ccaq",ccaq_mult,ov,("plsites","cancorr"))
    compareGvals(nc,"ccaa",ccaa_mult,ov,("ccasamples","cancorr"))
    compareGvals(nc,"ccab",ccab_mult,ov,("ccasamples","cancorr"))
  else:
    compareRMSvals(nc,"ccacorr",ccacorr,ov,("cancorr",))
    compareRMSvals(nc,"ccapfrac",ccapfrac,ov,("cancorr",))
    compareRMSvals(nc,"ccaqfrac",ccaqfrac,ov,("cancorr",))
    compareGvals(nc,"ccap",ccap,ov,("hsitesz","hsiteslat","hsiteslon","cancorr"))
    compareGvals(nc,"ccaq",ccaq,ov,("plsites","cancorr"))
    compareGvals(nc,"ccaa",ccaa,ov,("ccasamples","cancorr"))
    compareGvals(nc,"ccab",ccab,ov,("ccasamples","cancorr"))
  inc.close()

def testdiffoperators(nc,ov):
  do=pyclimate.diffoperators
  inc=Dataset("cru_hgt.nc")
  lats=numpy.array(inc.variables["lat"][:],'d')
  rlats=do.deg2rad(lats)
  lons=numpy.array(inc.variables["lon"][:],numpy.float64)
  rlons=do.deg2rad(lons)
  grad=do.HGRADIENT(lats,lons)
  div=do.HDIVERGENCE(lats,lons)
  curl=do.VCURL(lats,lons)
  hdata=numpy.array(inc.variables["hgt"][0,1,:,:],numpy.float64)
  g=9.81
  omega=7.292e-5
  kgeo=g/2/omega/numpy.sin(rlats)
  # Geostrophic wind
  thegrad=grad.hgradient(hdata)
  u=-kgeo[:,numpy.NewAxis]*thegrad[1]
  v=kgeo[:,numpy.NewAxis]*thegrad[0]
  # Gradient of the geostrophic wind (mostly harmless...)
  thediv=div.hdivergence(u,v)
  # Curl of the geostrophic wind
  thecurl=curl.vcurl(u,v)
  if ov:
    nc.createDimension("lat",len(rlats))
    nc.createDimension("lon",len(rlons))
    nc.createVariable("lat",numpy.float32,("lat",))[:]=lats.astype('f')
    nc.variables["lat"].units="degrees_north"
    nc.createVariable("lon",numpy.float32,("lon",))[:]=lons.astype('f')
    nc.variables["lon"].units="degrees_east"
    nc.createVariable("hgt",numpy.float32,("lat","lon"))
    nc.variables["hgt"][:,:]=hdata.astype(numpy.float32)
  compareRMSvals(nc,"uwind",u,ov,("lat","lon"))
  compareRMSvals(nc,"vwind",v,ov,("lat","lon"))
  compareRMSvals(nc,"DIVuv",thediv,ov,("lat","lon"))
  compareRMSvals(nc,"vorticity",thecurl,ov,("lat","lon"))
  inc.close()

def testfilters(nc,ov):
  kz=pyclimate.KZFilter
  la=pyclimate.LanczosFilter
  data2D=pyclimate.readdat.readdat("ctiao.dat")
  inc=Dataset("cru_hgt.nc")
  data3D=numpy.array(inc.variables["hgt"][:,2,0:3,4:6],numpy.float64)
  # Instances of filters
  filters={}
  filters["kzh"]=kz.KZFilter(3,3,0)
  filters["kzl"]=kz.KZFilter(5,3,1)
  filters["ll"]=la.LanczosFilter("lp",0.1,0.1,10)
  filters["lh"]=la.LanczosFilter("hp",0.3,0.3,10)
  filters["lb"]=la.LanczosFilter("bp",0.1,0.3,10)
  if ov:
    nc.createDimension("kzhcoefs",len(filters["kzh"].coefs))
    nc.createDimension("kzlcoefs",len(filters["kzl"].coefs))
    nc.createDimension("llcoefs",len(filters["ll"].coefs))
    nc.createDimension("lhcoefs",len(filters["lh"].coefs))
    nc.createDimension("lbcoefs",len(filters["lb"].coefs))
  compareRMSvals(nc,"KZ-h",filters["kzh"].coefs,ov,("kzhcoefs",))
  compareRMSvals(nc,"KZ-l",filters["kzl"].coefs,ov,("kzlcoefs",))
  compareRMSvals(nc,"L-h",filters["lh"].coefs,ov,("lhcoefs",))
  compareRMSvals(nc,"L-b",filters["lb"].coefs,ov,("lbcoefs",))
  compareRMSvals(nc,"L-l",filters["ll"].coefs,ov,("llcoefs",))
  # Well, perform filtering of data sets
  keys=filters.keys()
  keys.sort()
  datasets=[data2D,data3D]
  datanames=["data2D","data3D"]
  for kf in keys:
    f=filters[kf]
    for id in xrange(len(datasets)):
      # The dataset has changed it shape, reset the filter
      f.reset()
      data=datasets[id]
      result=[]
      for irec in xrange(len(data)):
        fdata=f.getfiltered(data[irec])
        if fdata is not None:
          result.append(fdata)
      result=numpy.array(result)
      varname=kf+"_"+datanames[id]
      if ov:
        nc.createDimension("dimX_"+varname,len(result))
        nc.createDimension("dimY_"+varname,len(result[0]))
        if id==1:
          nc.createDimension("dimZ_"+varname,len(result[0,0]))
      dims=("dimX_"+varname,"dimY_"+varname)
      if id==1:
        dims=dims+("dimZ_"+varname,)
      compareRMSvals(nc,varname,result,ov,dims)
  inc.close()


def testKPDF(nc,ov):
  # Save some typing
  
  KPDF=pyclimate.KPDF
  # Global definitions for this module
  Xs=numpy.arange(-5,5.01,0.5) # X-Y grid
  Ys=numpy.arange(-5,5.01,0.5)
  # Define the netCDF dimensions to store the values
  if ov:
    nc.createDimension("PDFdimx",len(Xs))
    nc.createDimension("PDFdimy",len(Ys))
  # Univariate PDFs
  cti=pyclimate.readdat.readcol("ctiao.dat",1)
  pdf=KPDF.UPDFEpanechnikov(cti,Xs,1.)
  compareRMSvals(nc,"pdfCTIEpanechnikov",pdf,ov,("PDFdimx",))
  pdf=KPDF.UPDFBiweight(cti,Xs,1.)
  compareRMSvals(nc,"pdfCTIBiweight",pdf,ov,("PDFdimx",))
  pdf=KPDF.UPDFTriangular(cti,Xs,1.)
  compareRMSvals(nc,"pdfCTITriangular",pdf,ov,("PDFdimx",))
  opth=numpy.array([KPDF.UPDFOptimumBandwidth(cti)])
  compareRMSvals(nc,"UPDFOptimumBandwidthCTI",opth,ov,("singleval",))
  # Multivariate PDFs (2D)
  # Read the CTI/AO dataset, covariance matrix and sqrt(det(S))
  ctiao=pyclimate.readdat.readdat("ctiao.dat") # Read
  S=pyclimate.mvarstatools.covariancematrix(ctiao,ctiao)
  Sm1=numpy.linalg.inv(S)
  sqrtdetS=numpy.sqrt(numpy.linalg.det(S))
  # Start computing the 2D-PDFs
  PDFshape=(len(Xs),len(Ys))
  grid=KPDF.MPDF2DGrid2Array(Xs,Ys)
  pdfvect=KPDF.MPDFEpanechnikov(ctiao,grid,1.,Sm1,sqrtdetS)
  pdfvect.shape=PDFshape
  compareRMSvals(nc,"pdf2DFEpanechnikov",pdfvect,ov,("PDFdimx","PDFdimy"))
  pdfvect=KPDF.MPDFGaussian(ctiao,grid,1.,Sm1,sqrtdetS)
  pdfvect.shape=PDFshape
  compareRMSvals(nc,"pdf2DFGaussian",pdfvect,ov,("PDFdimx","PDFdimy"))
  pdfvect=KPDF.MPDFEpanechnikov(ctiao,grid,1.)
  pdfvect.shape=PDFshape
  compareRMSvals(nc,"pdf2DEpanechnikov",pdfvect,ov,("PDFdimx","PDFdimy"))
  pdfvect=KPDF.MPDFGaussian(ctiao,grid,1.)
  pdfvect.shape=PDFshape
  compareRMSvals(nc,"pdf2DGaussian",pdfvect,ov,("PDFdimx","PDFdimy"))
  opth=numpy.array([KPDF.MPDFOptimumBandwidth(ctiao)])
  compareRMSvals(nc,"MPDFOptimumBandwidthCTIAO",opth,ov,("singleval",))

def rms4D(err):
  theshape=numpy.array(err.shape)
  N=numpy.multiply.reduce(theshape)
  rms=numpy.sqrt(numpy.add.reduce(numpy.add.reduce(numpy.add.reduce(numpy.add.reduce(err*err))))/N)
  return rms

def testnewdiffoperators(nc,ovwr):
  # The original version of the differential operators was
  # extensively tested during previous releases,
  # we only need to test the new features:
  # 1) Periodic Boundary conditions in longitude
  # 2) Several dimensions at a time according to COARDS conventions
  # ...
  # Let's go ahead...
  #
  # First... we need to open a more general test data set
  # with global coverage (geopotential), vectorial
  # fields (like speed) and several dimensions...
  inc=Dataset("testDO.nc")
  hvar=inc.variables["hgt"]
  uvar=inc.variables["u"]
  vvar=inc.variables["v"]
  lats=numpy.array(inc.variables["lat"][:],numpy.float64)
  lons=numpy.array(inc.variables["lon"][:],numpy.float64)
  ########## this shifted lons will be used later
  lons_shift=lons.tolist()
  lons_shift.reverse()
  lons_shift=-1.0*numpy.array(lons_shift,numpy.float64)
  if ovwr:
    nc.createDimension("DO_1_1_time",hvar.shape[0])
    nc.createDimension("DO_1_1_lev",hvar.shape[1])
    nc.createDimension("DO_1_1_lat",hvar.shape[2])
    nc.createDimension("DO_1_1_lon",hvar.shape[3])
  dims=("DO_1_1_time","DO_1_1_lev","DO_1_1_lat","DO_1_1_lon")
  #####################################################################
  # Finally, test whether the results are the same for several
  # dimensions and combinations of PBC and dimensions
  ######################################################################
  print "Testing D.O. with several dimensions with and without PBC..."
  for pbc in [0,1]:
    ######################################################################
    ######################################################################
    print
    print "Testing D.O. with 0 to 360 degrees longitudes..."
    ######################################################################
    ######################################################################
    ####################
    # Test the gradient operator
    ###########################
    hgrad=pyclimate.diffoperators.HGRADIENT(lats,lons,1,pbc)
    nx=numpy.zeros((2,2)+hvar.shape[2:],'d')
    ny=numpy.zeros((2,2)+hvar.shape[2:],'d')
    n3x=numpy.zeros((2,2)+hvar.shape[2:],'d')
    n3y=numpy.zeros((2,2)+hvar.shape[2:],'d')
    # First of all, compute the operators layer by layer, as done
    # in previous version of PyClimate, and which has already
    # been tested
    for irec in xrange(2):
      for ilev in xrange(2):
        field=numpy.array(hvar[irec,ilev],'d')
        thegrad=hgrad.hgradient(field)
        nx[irec,ilev,:,:]=thegrad[0]
        ny[irec,ilev,:,:]=thegrad[1]
      field=numpy.array(hvar[irec],'d')
      thegrad=hgrad.hgradient(field)
      n3x[irec]=thegrad[0]
      n3y[irec]=thegrad[1]
    field=numpy.array(hvar[:,:,:,:],'d')
    n4x,n4y=hgrad.hgradient(field)
    if pbc:
      namex="DONablax_1_1_PBC"
      namey="DONablay_1_1_PBC"
    else:
      namex="DONablax_1_1_NPBC"
      namey="DONablay_1_1_NPBC"
    if ovwr:
      compareRMSvals(nc,namex,nx.astype('f'),ovwr,dims)
      compareRMSvals(nc,namey,ny.astype('f'),ovwr,dims)
    else:
      compareRMSvals(nc,namex,n3x.astype('f'),ovwr,dims," 3D")
      compareRMSvals(nc,namey,n3y.astype('f'),ovwr,dims," 3D")
      compareRMSvals(nc,namex,n4x.astype('f'),ovwr,dims," 4D")
      compareRMSvals(nc,namey,n4y.astype('f'),ovwr,dims," 4D")
    #############################################
    # Test the divergence
    ###########################################
    hdiv=pyclimate.diffoperators.HDIVERGENCE(lats,lons,1,pbc)
    d=numpy.zeros((2,2)+hvar.shape[2:],'d')
    d3=numpy.zeros((2,2)+hvar.shape[2:],'d')
    # First of all, compute the operators layer by layer, as done
    # in previous version of PyClimate, and which has already
    # been tested
    for irec in xrange(2):
      for ilev in xrange(2):
        ufield=numpy.array(uvar[irec,ilev],'d')
        vfield=numpy.array(vvar[irec,ilev],'d')
        thediv=hdiv.hdivergence(ufield,vfield)
        d[irec,ilev,:,:]=thediv
      ufield=numpy.array(uvar[irec],'d')
      vfield=numpy.array(vvar[irec],'d')
      thediv=hdiv.hdivergence(ufield,vfield)
      d3[irec]=thediv
    ufield=numpy.array(uvar[:,:,:,:],'d')
    vfield=numpy.array(vvar[:,:,:,:],'d')
    d4=hdiv.hdivergence(ufield,vfield)
    if pbc:
      name="DODivergence_1_1_PBC"
    else:
      name="DODivergence_1_1_NPBC"
    # Save them as float, the reference file is growing
    # "too" much
    if ovwr:
      compareRMSvals(nc,name,d.astype('f'),ovwr,dims)
    else:
      compareRMSvals(nc,name,d3.astype('f'),ovwr,dims," 3D")
      compareRMSvals(nc,name,d4.astype('f'),ovwr,dims," 4D")
    #############################################
    # Test the curl
    ###########################################
    vcurl=pyclimate.diffoperators.VCURL(lats,lons,1,pbc)
    c=numpy.zeros((2,2)+hvar.shape[2:],'d')
    c3=numpy.zeros((2,2)+hvar.shape[2:],'d')
    # First of all, compute the operators layer by layer, as done
    # in previous version of PyClimate, and which has already
    # been tested
    for irec in xrange(2):
      for ilev in xrange(2):
        ufield=numpy.array(uvar[irec,ilev],'d')
        vfield=numpy.array(vvar[irec,ilev],'d')
        thecurl=vcurl.vcurl(ufield,vfield)
        c[irec,ilev,:,:]=thecurl
      ufield=numpy.array(uvar[irec],'d')
      vfield=numpy.array(vvar[irec],'d')
      thecurl=vcurl.vcurl(ufield,vfield)
      c3[irec]=thecurl
    ufield=numpy.array(uvar[:,:,:,:],'d')
    vfield=numpy.array(vvar[:,:,:,:],'d')
    c4=vcurl.vcurl(ufield,vfield)
    if pbc:
      name="DOVCurl_1_1_PBC"
    else:
      name="DOVCurl_1_1_NPBC"
    # Save them as float, the reference file is growing
    # "too" much
    if ovwr:
      compareRMSvals(nc,name,c.astype('f'),ovwr,dims)
    else:
      compareRMSvals(nc,name,c3.astype('f'),ovwr,dims," 3D")
      compareRMSvals(nc,name,c4.astype('f'),ovwr,dims," 4D")
    ######################################################################
    ######################################################################
    print
    print "Testing D.O. with 360 degrees shifted longitudes..."
    ######################################################################
    ######################################################################
    ####################
    # Test the gradient operator
    ###########################
    hgrad_shift=pyclimate.diffoperators.HGRADIENT(lats,lons_shift,1,pbc)
    nx_shift=numpy.zeros((2,2)+hvar.shape[2:],'d')
    ny_shift=numpy.zeros((2,2)+hvar.shape[2:],'d')
    n3x_shift=numpy.zeros((2,2)+hvar.shape[2:],'d')
    n3y_shift=numpy.zeros((2,2)+hvar.shape[2:],'d')
    # First of all, compute the operators layer by layer, as done
    # in previous version of PyClimate, and which has already
    # been tested
    for irec in xrange(2):
      for ilev in xrange(2):
        field=numpy.array(hvar[irec,ilev],'d')
        thegrad_shift=hgrad_shift.hgradient(field)
        nx_shift[irec,ilev,:,:]=thegrad_shift[0]
        ny_shift[irec,ilev,:,:]=thegrad_shift[1]
      field=numpy.array(hvar[irec],'d')
      thegrad_shift=hgrad_shift.hgradient(field)
      n3x_shift[irec]=thegrad_shift[0]
      n3y_shift[irec]=thegrad_shift[1]
    field=numpy.array(hvar[:,:,:,:],'d')
    n4x_shift,n4y_shift=hgrad_shift.hgradient(field)
    if pbc:
      namex="DONablax_1_1_PBC"
      namey="DONablay_1_1_PBC"
    else:
      namex="DONablax_1_1_NPBC"
      namey="DONablay_1_1_NPBC"
    comparememoryvals(namex,n3x,n3x_shift," 3D")
    comparememoryvals(namey,n3y,n3y_shift," 3D")
    comparememoryvals(namex,n4x,n4x_shift," 4D")
    comparememoryvals(namey,n4y,n4y_shift," 4D")
    #############################################
    # Test the divergence
    ###########################################
    hdiv_shift=pyclimate.diffoperators.HDIVERGENCE(lats,lons_shift,1,pbc)
    d_shift=numpy.zeros((2,2)+hvar.shape[2:],'d')
    d3_shift=numpy.zeros((2,2)+hvar.shape[2:],'d')
    # First of all, compute the operators layer by layer, as done
    # in previous version of PyClimate, and which has already
    # been tested
    for irec in xrange(2):
      for ilev in xrange(2):
        ufield=numpy.array(uvar[irec,ilev],'d')
        vfield=numpy.array(vvar[irec,ilev],'d')
        thediv_shift=hdiv_shift.hdivergence(ufield,vfield)
        d_shift[irec,ilev,:,:]=thediv_shift
      ufield=numpy.array(uvar[irec],'d')
      vfield=numpy.array(vvar[irec],'d')
      thediv_shift=hdiv_shift.hdivergence(ufield,vfield)
      d3_shift[irec]=thediv_shift
    ufield=numpy.array(uvar[:,:,:,:],'d')
    vfield=numpy.array(vvar[:,:,:,:],'d')
    d4_shift=hdiv_shift.hdivergence(ufield,vfield)
    if pbc:
      name="DODivergence_1_1_PBC"
    else:
      name="DODivergence_1_1_NPBC"
    comparememoryvals(name,d,d_shift)
    comparememoryvals(name,d3,d3_shift," 3D")
    comparememoryvals(name,d4,d4_shift," 4D")
    #############################################
    # Test the curl
    ###########################################
    vcurl_shift=pyclimate.diffoperators.VCURL(lats,lons_shift,1,pbc)
    c_shift=numpy.zeros((2,2)+hvar.shape[2:],'d')
    c3_shift=numpy.zeros((2,2)+hvar.shape[2:],'d')
    # First of all, compute the operators layer by layer, as done
    # in previous version of PyClimate, and which has already
    # been tested
    for irec in xrange(2):
      for ilev in xrange(2):
        ufield=numpy.array(uvar[irec,ilev],'d')
        vfield=numpy.array(vvar[irec,ilev],'d')
        thecurl_shift=vcurl_shift.vcurl(ufield,vfield)
        c_shift[irec,ilev,:,:]=thecurl_shift
      ufield=numpy.array(uvar[irec],'d')
      vfield=numpy.array(vvar[irec],'d')
      thecurl_shift=vcurl_shift.vcurl(ufield,vfield)
      c3_shift[irec]=thecurl_shift
    ufield=numpy.array(uvar[:,:,:,:],'d')
    vfield=numpy.array(vvar[:,:,:,:],'d')
    c4_shift=vcurl_shift.vcurl(ufield,vfield)
    if pbc:
      name="DOVCurl_1_1_PBC"
    else:
      name="DOVCurl_1_1_NPBC"
    comparememoryvals(name,c,c_shift)
    comparememoryvals(name,c3,c3_shift," 3D")
    comparememoryvals(name,c4,c4_shift," 4D")
  ## OK, the input data set is not needed anymore, close it
  inc.close()
  return

def testfasterMCtests(nc,ovwr):
  print "We are not saving anything now, to save some electronic trees"
  print "Just testing whether the functions run..."
  print 
  print "*"*50
  print "Monte Carlo test on EOFs..."
  print "*"*50
  eof=pyclimate.svdeofs
  inc=Dataset("cru_hgt.nc")
  hgtdata=numpy.array(inc.variables["hgt"][:,1,:,:],numpy.float64)
  oldshape=hgtdata.shape
  newshape=(oldshape[0],oldshape[1]*oldshape[2])
  hgtdata.shape=newshape
  Zs,lambdas,Es=eof.svdeofs(hgtdata)
  trashcan=eof.mctesteofs(hgtdata,Es[:,:2],10,len(hgtdata)/2)
  for i in xrange(trashcan.shape[0]):
    for j in xrange(trashcan.shape[1]):
      print "%9.3e"%(trashcan[i,j],),
    print
  inc.close()
  print "*"*50
  print "...WORK!!"
  print "*"*50
  ##############################
  print "*"*50
  print "Monte Carlo test on SVD..."
  print "*"*50
  s=pyclimate.svd
  inc=Dataset("cru_hgt.nc")
  # Geopotential height in a reduced domain around the Iberian Peninsula
  hgtdata=numpy.array(inc.variables["hgt"][:,1,:,:],numpy.float64)
  oldshape=hgtdata.shape
  newshape=(oldshape[0],oldshape[1]*oldshape[2])
  hgtdata.shape=newshape
  # Precipitation over the northern Iberian Peninsula
  pldata=pyclimate.readdat.readcols("plnibpei.dat",[2,3,4,5,6,7])
  U,sigmas,V=s.svd(hgtdata,pldata)
  N=10
  vs=2
  ccU,ccV=s.makemctest(U[:,:vs],V[:,:vs],hgtdata,pldata,N,len(pldata)/2)
  for i in xrange(N):
    for j in xrange(vs):
      print " %9.3e %9.3e"%(ccU[i,j],ccV[i,j]),
    print
  print "*"*50
  print "...WORK!!"
  print "*"*50
  inc.close()
  return

def testanalogs(nc,ov):
  SMOOTHING=2
  BASESAMPLES=10
  inc=Dataset("cru_hgt.nc")
  hgtdata=numpy.array(inc.variables["hgt"][:,:,:,:],numpy.float64)
  hgtbase=numpy.array(hgtdata[-BASESAMPLES:,:,:,:])
  hgtdata=numpy.array(hgtdata[:-BASESAMPLES,:,:,:])
  ANA=pyclimate.analog.EOFANALOG(hgtdata,neofs=4,pcscaling=1)
  AAVE=pyclimate.analog.ANALOGAverager(ANA,hgtbase,smoothing=SMOOTHING)
  recfield=AAVE.returnWeightedAverage()
  theweights=numpy.array(AAVE.weights)
  if ov:
    nc.createDimension("analog_h_basesamples",BASESAMPLES)
    nc.createDimension("analog_h_poolsamples",len(hgtdata)-BASESAMPLES)
    nc.createDimension("analog_smoothing",SMOOTHING)
  compareRMSvals(nc,"hgt_analog",recfield,ov,("analog_h_basesamples","h_channelz","h_channellat","h_channellon"))
  compareRMSvals(nc,"hgt_analog_weights",theweights,ov,("analog_h_basesamples","analog_smoothing"))
  inc.close()

def testNHArray(nc,ov):
  inc=Dataset("cru_hgt.nc")
  hgtdata=numpy.array(inc.variables["hgt"][:,1,:,:],numpy.float64)
  inc.close()
  samples = len(hgtdata)
  channels = numpy.multiply.reduce(hgtdata.shape[1:])
  bins = 20
  nha = pyclimate.NHArray.NHArray(5170, 5800, bins, channels)
  for i in range(len(hgtdata)):
    nha.Update(hgtdata[i])
  theranges = nha.GetRange(0.05)
  if ov:
    nc.createDimension("nharray_channels", channels)
    nc.createDimension("nharray_range_dim", 2)
  compareRMSvals(nc,"nharray_005ranges",theranges,ov,("nharray_channels","nharray_range_dim"))
  return locals()

def testPyClimate_01_01(nc,ovwr):
  print SEPARATOR2
  print "* Testing new features in PyClimate 1.1"
  print SEPARATOR2
  print 

  # Testing exceptions (JS)
  print "Testing new exception classes"
  pyclimate.pyclimateexcpt.testallpyclimateexceptions()

  # New version of the differential operators
  #print "Testing extended (3D, 4D, PBC) differential operators" # (JS)
  title("diffoperators - 1.1",ovwr)
  testnewdiffoperators(nc,ovwr)

  # Test the MC test for SVD and EOFs
  title("Faster MC tests.",ovwr)
  testfasterMCtests(nc,ovwr) # (JS)

  # Test CCA (jf)
  title("CCA",ovwr)  
  testCCA(nc,ovwr) 

def testPyClimate_01_02(nc,ovwr):
  print SEPARATOR2
  print "* Testing new features in PyClimate 1.2"
  print SEPARATOR2
  print
  title("New EOFs, based on objects",ovwr)
  testnewEOFs(nc,ovwr)
  title("Analogs",ovwr)
  testanalogs(nc,ovwr)
  title("NHArray",ovwr)
  return testNHArray(nc,ovwr)

if __name__=="__main__":
  overwrite=0
  doget=0
  # Parse the command line arguments
  try:
    opts,args=getopt.getopt(sys.argv[1:],"hog")
  except getopt.GetoptError:
    usage(sys.argv[0])
  if len(args)!=0:
    usage(sys.argv[0])
  for opt in opts:
    if opt[0]=="-h":
      usage(sys.argv[0])
    if opt[0]=="-o":
      overwrite=1
    if opt[0]=="-g":
      doget=1
  if overwrite and doget:
    print "Unable overwrite the file while getting it"
    print "Make a better selection of command line options"
    sys.exit(1)

  # If we must overwrite the reference file, we need to
  # create it, first, otherwise, just open it for reading
  refname="reference.cdf"
  if overwrite:
    nc=Dataset(refname,"w")
    nc.version=sys.version
    nc.platform=sys.platform
    if 'byteorder' in dir(sys):
      nc.byteorder=sys.byteorder
    else:
      nc.byteorder="Unknown, Python older than 2.0??"
  else:
    # If there is no local copy of the file, get it from
    # its URL
    if os.access(refname,os.F_OK)==0 or doget:
      thedir="http://starship.python.net/crew/jsaenz/pyclimate/"
      thedir=thedir+"references/"
      theurl=thedir+pyclimate.tools.pyclimateversion()+"/"+refname
      print "There is no local copy of:",refname
      print "Do you want me to get it from"
      print theurl,"?[no]/yes"
      print "Warning: It is about 1.6 Mb"
      answer=sys.stdin.readline()
      if len(answer)==1:
        answer="n"
      if answer[0]=="y" or answer[0]=="Y":
        import urllib
        try:
          urllib.urlretrieve(theurl,refname)
        except IOError:
          print "Unable to retrieve:",theurl
          print "Sorry, I can not proceed with the test"
          print "Retrieve:",theurl," manually"
          sys.exit(1)
      else:
        print "Sorry, I can not proceed with the test",
        print "without the reference file"
        print "Retrieve:",theurl," manually"
        sys.exit(1)
    nc=Dataset(refname)
    print "Reference NetCDF File %s created by:"%(refname,)
    if 'version' in dir(nc):
      print "Version:",nc.version
    else:
      print "Version:","Unknown"
    if 'platform' in dir(nc):
      print "Platform:",nc.platform
    else:
      print "Platform:","Unknown"
    if 'byteorder' in dir(nc):
      print "Byteorder:",nc.byteorder
    else:
      print "Byteorder:","Unknown"

  print 
  print "In these tests, G_i_j means congruence coefficient, and should"
  print "be one or minus one for a successful run"
  print

  # Test IO routines
  title("IO",overwrite)
  testIOASCII(overwrite,nc)
  title("NCSTRUCT",overwrite)
  testIOnc(overwrite)

  # Test JDTime and JDTimeHandler
  title("JDTime",overwrite)
  testJDTime(nc,overwrite)
  title("JDTimeHandler",overwrite)
  testJDTimeHandler(nc,overwrite)

  # Test pydcdflib, the access to DCDFLIB
  title("DCDFLIB.C",overwrite)
  testpydcdflib(nc,overwrite)

  # We don't see any need to specifically test mvarstatools.py, because:
  # 1) It is in fact tested through the test of svd*.py
  # 2) It is simple portable Python code which has already
  #    been tested, and it is not easy to find a reason why they 
  #    should fail.
  # Thus, we don't test them and skip to the next test, EOFs
  title("EOFs",overwrite)
  testEOFs(nc,overwrite)
  title("SVD of Z and P",overwrite)
  testSVD(nc,overwrite)

  # Test digital filters
  title("Digital filters",overwrite)
  testfilters(nc,overwrite)

  # Differential operators
  title("diffoperators",overwrite)
  testdiffoperators(nc,overwrite)

  # Kernel-based probability density functions
  title("KPDF",overwrite)
  testKPDF(nc,overwrite)

  # Test new features in PyClimate 1.1
  testPyClimate_01_01(nc,overwrite)

  # Test new features in PyClimate 1.2
  debgg = testPyClimate_01_02(nc,overwrite)

  nc.close()
  if overwrite:
    print 
    print "!"*60
    print "!"*15+"Reference file has been overwriten"
    print "!"*15+"Please re-run the tests without the -o flag"

