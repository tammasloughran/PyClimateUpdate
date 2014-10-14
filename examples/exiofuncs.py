# exiofuncs.py
# Examples on the use of the ASCII IO funcs
from pyclimate.readdat import *
fname="../test/datawithcomplex.dat"

# Read the whole file, and return it as a Float32
print readdat(fname,Float32)

# Read the first column and coerce conversion to Complex32
print readcol(fname,3,Complex32)

# Read the 3rd, 4th and 1st columns as Complex64
print readcols(fname,(3,4,1),Complex64)

# Read the first 4 columns as Int16
print readcols(fname,arange(1,5),Int16)

