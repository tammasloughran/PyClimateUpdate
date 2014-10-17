# Adapted for numpy/ma/cdms2 by convertcdms.py
# atmosphericmoisture.py

"""Functions related to the thermodynamics of atmospheric moisture

"""
# Copyright (C) 2002, Jon Saenz, Jesus Fernandez and Juan Zubillaga
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
# Jon Saenz, 2002

import numpy

###########################################################
# Some constants of general use
###########################################################
Rv=461.         # J/(K kg)
Rd=287.         # J/(K kg)
T0=273.15       # K
es0=611.        # Pa
epsilon=Rd/Rv

def saturation_pressure_over_ice(T):
	"""Saturation pressure (Pa) over ice

	See Bohren, Albrecht (2000), pages 197-200

	Arguments:

		'T' -- Temperature (K)
	"""
        return es0*numpy.exp(6293.*(1./T0-1./T)-0.555*numpy.log(T/T0))

def saturation_pressure_over_water(T):
       	"""Saturation pressure (Pa) over water

	See Bohren, Albrecht (2000), pages 197-200

	Arguments:

		'T' -- Temperature (K)
	"""
	return es0*numpy.exp(6808.*(1./T0-1./T)-5.09*numpy.log(T/T0))

def saturation_pressure(T):
       	"""Saturation pressure (Pa) from temperature

	Consider the cases over water and ice,
	according to the temperature involved
	Do not consider subcooled water at all.

	Arguments:

		'T' -- Temperature (K)
	"""
	aT = numpy.array(T)
	# Lengthy code to avoid using Python cycles and, still, have the
	# choice to select different formulations for ice and water surfaces
	icemask = numpy.less(aT,T0)
	watermask = numpy.logical_not(icemask)
	aTice = aT*icemask + watermask*T0
	aTwater = aT*watermask + icemask*T0
	spress = (saturation_pressure_over_water(aTwater)*watermask +
		saturation_pressure_over_ice(aTice)*icemask)
	return spress

def saturation_mixing_ratio(P, T):
	"""Saturation mixing ratio from temperature and pressure

	See Wallace and Hobbs

	Arguments:

		'P' -- Presure (Pa)

		'T' -- Temperature (K)
	"""
        es=saturation_pressure(T)
        return Rd/Rv*es/(P-es)

def rh2w(rh,P,T):
	"""Get the mixing ratio from the relative humidity

	Arguments:

		'rh' -- Relative humidity (%)
		
		'P' -- Pressure (Pa)

		'T' -- Temperature (K)
	"""
        return saturation_mixing_ratio(P,T)*rh/100.

def rh2shum(rh,P,T):
	"""Get the specific humidity from the relative humidity

	Arguments:

		'rh' -- Relative humidity (%)
		
		'P' -- Pressure (Pa)

		'T' -- Temperature (K)
	"""
        w=rh2w(rh,P,T)
        return w/(1.+w)


def dewpointdepression2rh(dpdp,P,T):
	"""Get the relative humidity from the dew-point depression

	Arguments:

		'dpdp' -- Dew point depression (K)
		
		'P' -- Pressure (Pa)

		'T' -- Temperature (K)
	"""
        Td=T-dpdp
        return 100*saturation_mixing_ratio(P,Td)/saturation_mixing_ratio(P,T)

def q2e(q,P):
	"""Get the partial vapour pressure from specific humidity

	Arguments:

		'q' -- Specific humidity

		'P' -- Pressure (Pa)
	"""
	return q*P/(epsilon*(1-q)+q)
