/*

  JDTime.c

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
#include <stdio.h>
#include <math.h>
#include <stdlib.h>

#include "JDTime.h"

/* From now on, the "private" interface */
/* Days in one tropical year (from udunits.dat) **/
const double days_per_tropical_year=365.242198781;
const double seconds_per_day=86400. ;

/* Year, month and day */
typedef struct {
  int year;
  int month;
  double day; } __YMD, *__YMDPtr ;

/* We might want to compute H:M:S.S data from JD's fractional part*/
typedef struct {
  int hour;
  int min;
  double sec; } __HMS, *__HMSPtr;


static double frac( double fnumber )
{
  return (fnumber-floor(fnumber));
}

/* From the day field of the JD struct, get H:M:S.S information ***/
static void day2hms( double day , __HMSPtr hms );

/* From hms, get the fractional part of the day */
static double hms2day( __HMSPtr hms );

/* paragraph 4: dd.dddd/mm/yyyy -> Julian day */
static double ymd2jd( __YMDPtr ymdptr )
{
   double a,b,c,d1,jd;
   int y;
   int m;
   double d;

   if (!ymdptr)
     return 0.0;
   y=ymdptr->year;
   m=ymdptr->month;
   d=ymdptr->day;

   if (m <= 2) {
      y -= 1; m += 12; 
   };
   a = floor((double)y/100.0);
   b = 2.0 - a + floor(a/4);
   if (y < 0 ) {
      c = floor((365.25*y)-0.75);
   } else {
      c = floor(365.25*y);
   };
   d1 = floor(30.6001*(m+1));
   jd = b+c+d1+d+1720994.5;
   return(jd);
}

/* paragraph 5: Julian day -> dd.dddd/mm/yyyy */
static void jd2ymd( double jd , __YMDPtr ymdptr )
{
   double a,b,c,d,e,g,i,f,m;

   jd += 0.5;
   i = floor(jd);
   f = frac(jd);
   if (i>2299160) {
     a=floor((i-1867216.25)/36524.25);
     b=i+1+a-floor(a/4.0);
   } else {
     b=i;
   };
   c = b+1524;
   d = floor((c-122.1)/365.25);
   e = floor(365.25*d);
   g = floor((c-e)/30.6001);
   ymdptr->day = c-e+f-floor(30.6001*g);
   if (g<13.5) {
      m=g-1.0;
      ymdptr->month = (int)g-1;
   } else {
      m=g-13.0;
      ymdptr->month = (int)g-13;
   };
   if (m>2.5) {
      ymdptr->year = (int)d-4716;
   } else {
      ymdptr->year = (int)d-4715;
   };
}

/* From the day field of the JD struct, get H:M:S.S information ***/
static void day2hms( double day , __HMSPtr hms )
{
  double fp;

  if (!hms)
    return;

  fp=frac(day)*24;
  hms->hour=(int)floor(fp);
  fp=frac(fp)*60;
  hms->min=(int)floor(fp);
  hms->sec=frac(fp)*60;
}

/* Inverse function... */
static double hms2day( __HMSPtr hms )
{
  double fp=0.0;
  fp+=hms->hour/24.;
  fp+=hms->min/1440.;
  fp+=hms->sec/86400.;
  return fp;
}

/* "Public" interface */
void jd2date( double jd , JDTimePtr jdt )
{
  __YMD ymd;
  __HMS hms;
  if (jdt){
    jd2ymd(jd,&ymd);
    day2hms(ymd.day,&hms);
    jdt->year=ymd.year;
    jdt->month=ymd.month;
    jdt->day=(int)ymd.day;
    jdt->hour=hms.hour;
    jdt->minute=hms.min;
    jdt->second=hms.sec;
  }
}

double date2jd( JDTimePtr jdt )
{
  __YMD ymd;
  __HMS hms;
  double jdpart,jd;
  if (!jdt)
    return -1.0;
  hms.hour=jdt->hour;
  hms.min=jdt->minute;
  hms.sec=jdt->second;
  jdpart=hms2day(&hms);
  ymd.year=jdt->year;
  ymd.month=jdt->month;
  ymd.day=jdt->day+jdpart;
  jd=ymd2jd(&ymd);
  return jd;
}


/* Simulated "monthly" steps, even though a month is not an evenly spaced time
unit */
double monthlystep( void )
{
  return (days_per_tropical_year/12.);
}
