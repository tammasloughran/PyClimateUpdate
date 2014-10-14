/*

  JDTime.h

     The functions in this file are just implementation in C of the
     algorithms from: "Practical Astronomy With Your Calculator"
     by Peter Duffett-Smith, Third edition, Cambridge University Press.

     Originally, some code was writen by:
     Svetoslav Ivantchev, July 1998, UPV, svet@wm.lc.ehu.es

     Since then, it has been changed, some functions stripped because we
     didn't need them and we have created some new ones that we really
     HAD TO have. The JDTime date structure which holds all the fields
     in a date has been created and some functions that correctly
     handle those complete structures and conversion functions
     to and from doubles (Julian Days) have been created.
     This way, this code has been adapted to climatological
     uses and a Python interface has been built by:
     Jon Saenz, February 1999, jsaenz@wm.lc.ehu.es

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
*/
#ifndef __JDTime__
#define __JDTime__ 1

/*****************
Public interface
The rest of the functions are defined as static in the C file
******************/
/* Broken-down time--struct (as time.h's "struct tm" but simpler, we will 
always use UTC, and no timezone/daylight saving info needed) */
typedef struct {
  int year;
  int month;
  int day;
  int hour;
  int minute;
  double second;
} JDTime, *JDTimePtr ;

/* From a broken down date, get the corresponding time coordinate 
(Julian Day)*/
/* Time coordinate is a double by the moment and enough for a LONG interval.
With typical 19 digits of precision for a double (sizeof(double)==8),
it is possible to represent more than 500 thousand million years second by
second... this seems enough for our needs */
extern double date2jd( JDTimePtr jdt );

/* Inverse function, given a time coordinate, get the broken down date */
extern void jd2date( double jd , JDTimePtr jdt );

/* Simulated "monthly" steps, even though a month is not an evenly spaced time
unit, using these steps and the time coordinate defined in this 
package, our years behave as if they had twelve equally spaced months... 
Return the step as days */
extern double monthlystep( void );

#endif
