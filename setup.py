
import sys, os
from numpy.distutils.core import setup, Extension

lib = os.path.join(os.path.join(sys.prefix, 'lib'), 'python'+sys.version[:3])
site_packages = os.path.join(lib, 'site-packages')

setup (name = "PyClimate",
       version = "1.2.2",

       description = "Analysis of Climate Variability",
       author = "Jon Saenz, Jesus Fernandez and Juan Zubillaga",
       author_email = "jsaenz@wm.lc.ehu.es",
       url = "http://www.pyclimate.org",

       package_dir = { 'pyclimate' : 'src'},
       packages = ["pyclimate"],
       ext_modules = [ Extension('pyclimate.JDTimec',
                                ['src/JDTime.c','src/JDTime_wrap.c']) ,
                       Extension('pyclimate.pydcdflibc',
                                ['src/pycdf.c','src/ipmpar.c',
                                 'src/pydcdflib_wrap.c',
                                 'src/dcdflib.c']) ,
                       Extension('pyclimate.KPDF',['src/KPDF.c']),
                       Extension('pyclimate.anumhist',['src/anumhist.c'])],
#	py_modules = ["pyclimate.JDTime","pyclimate.JDTimeHandler",
#                      "pyclimate.KZFilter",
#                      "pyclimate.diffoperators",
#                      "pyclimate.mvarstatools",
#                      "pyclimate.ncstruct"]
       )





