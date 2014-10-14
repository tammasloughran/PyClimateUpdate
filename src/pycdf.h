/********

pycdf.h

Definitions for the wrapper functions used to be able to
use dcdflib from Python

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

Jon Saenz, 19990310

*******/
#ifndef __pycdf__
#define __pycdf__ 1


/***
There are a lot of times qhere we don't want to compute p and q, and they must
be defined such that q=1.-p. Thus, we force such a condition inside the 
routines by means of a static function pycdfgetq(). This rests 
the user a degree of freedom when calling the routines,
but, on the other side, it allows him/her not caring about this
restriction.
In case a user was really interested in using Q instead of P, he/she can 
always previously use the function pycdfsetq() 

All the pycdf structures start by the which,p,q fields. They are the
"common part" of the pycdf structures. We will use this
property to get the pointers to the p and q fields.
This will be a dirty trick but...
***/
typedef struct {
  int which;
  double p;
  double q; } CDFPQ;

extern double pycdfsetq( CDFPQ *pycdfob , double q );

/*******
Unless a cliente really needs to use the Q field, the external
interface really starts here,,,,,
 ******/
/*** Wrappers for cdfbet() ***/
typedef struct {
  int which;
  double p;
  double q;
  double x;
  double y;
  double a;
  double b;
  int status;
  double bound;
} CDFBet ;
extern int pycdfbet( CDFBet *sptr );

/*** Wrappers for cdfbin() ***/
typedef struct {
  int which;
  double p;
  double q;
  double s;
  double xn;
  double pr;
  double ompr;
  int status;
  double bound;
} CDFBin ;
extern int pycdfbin( CDFBin *sptr );

/*** Wrapper for cdfchi() ***/
typedef struct {
  int which;
  double p;
  double q;
  double x;
  double df;
  int status;
  double bound;
} CDFChi ;
extern int pycdfchi( CDFChi *sptr );

/*** Wrapper for cdfchn() ***/
typedef struct {
  int which;
  double p;
  double q;
  double x;
  double df;
  double pnonc;
  int status;
  double bound;
} CDFChn;
extern int pycdfchn( CDFChn *sptr );

/*** Wrapper for cdff() *****/
typedef struct {
  int which;
  double p;
  double q;
  double f;
  double dfn;
  double dfd;
  int status;
  double bound;
} CDFF;
extern int pycdff( CDFF *sptr );

/*** Wrapper for cdffnc() ***/
typedef struct {
  int which;
  double p;
  double q;
  double f;
  double dfn;
  double dfd;
  double pnonc;
  int status;
  double bound;
} CDFFnc ;
extern int pycdffnc( CDFFnc *sptr );

/*** Wrapper for cdfgam() ***/
typedef struct {
  int which;
  double p;
  double q;
  double x;
  double shape;
  double scale;
  int status;
  double bound;
} CDFGam;
extern int pycdfgam( CDFGam *sptr );

/*** Wrapper for cdfnbn ***/
typedef struct {
  int which;
  double p;
  double q;
  double s;
  double xn;
  double pr;
  double ompr;
  int status;
  double bound;
} CDFNbn ;
extern int pycdfnbn( CDFNbn *sptr );

/*** Wrapper for cdfnor() ***/
typedef struct {
  int which;
  double p;
  double q;
  double x;
  double mean;
  double sd;
  int status;
  double bound;
} CDFNor ;
extern int pycdfnor( CDFNor *sptr );

/*** Wrapper for cdfpoi() ***/
typedef struct {
  int which;
  double p;
  double q;
  double s;
  double xlam;
  int status;
  double bound;
} CDFPoi ;
extern int pycdfpoi( CDFPoi *sptr );

/*** Wrapper for cdft() ***/
typedef struct {
  int which;
  double p;
  double q;
  double t;
  double df;
  int status;
  double bound;
} CDFT;
extern int pycdft( CDFT *sptr );

/** Wrapper for cdftnc() ***/
typedef struct {
  int which;
  double p;
  double q;
  double t;
  double df;
  double pnonc;
  int status;
  double bound;
} CDFTnc ;
extern int pycdftnc( CDFTnc *sptr );




#endif
