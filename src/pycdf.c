/********

pycdf.c

Wrapper functions used to be able to
use dcdflib.c from Python

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
#include "cdflib.h"
#include "pycdf.h"

#include <stdio.h>

/***
There are a lot of times qhere we don't want to compute p and q, and they must
be defined such that q=1.-p. Thus, we force such a condition inside the 
routines by means of a static function pycdfgetq(). This rests 
the user a degree of freedom when calling the routines,
but, on the other side, it allows him/her not caring about this
restriction.
In case a user was really interested in using Q instead of P, he/she can 
always previously use the function pycdfsetq() 
****/

/*** #define __DEBUG_CDFPQ__ 1 ***/

/** Internal use only **/
static double *pycdfgetpptr( CDFPQ *pycdfob )
{
  double *pptr;
#ifdef __DEBUG_CDFPQ__
  FILE *ofile=fopen("pycdf.log","a");
  fprintf(ofile,"pycdfgetpptr: %X %d %g %g ->",(void*)pycdfob,pycdfob->which,
	  pycdfob->p,pycdfob->q);
#endif

  pptr=&(pycdfob->p);
#ifdef __DEBUG_CDFPQ__
  fprintf(ofile,"pptr:%X , %g\n",pptr,*pptr);
  fclose(ofile);
#endif
  return pptr;
}

static double *pycdfgetqptr( CDFPQ *pycdfob )
{
  double *qptr;
#ifdef __DEBUG_CDFPQ__
  FILE *ofile=fopen("pycdf.log","a");
  fprintf(ofile,"pycdfgetqptr: %X %d %g %g ->",(void*)pycdfob,pycdfob->which,
	  pycdfob->p,pycdfob->q);
#endif
  qptr=&(pycdfob->q);
#ifdef __DEBUG_CDFPQ__
  fprintf(ofile,"qptr:%X , %g\n",qptr,*qptr);
  fclose(ofile);
#endif
  return qptr;
}

static void pycdfgetq( CDFPQ *pycdfob )
{
  double *pptr=pycdfgetpptr(pycdfob);
  double *qptr=pycdfgetqptr(pycdfob);
#ifdef __DEBUG_CDFPQ__
  FILE *ofile=fopen("pycdf.log","a");
  fprintf(ofile,"pycdfgetq: %X %d %g %g ->",(void*)pycdfob,pycdfob->which,
	  pycdfob->p,pycdfob->q);
#endif
 *qptr=1.-(*pptr);
#ifdef __DEBUG_CDFPQ__
  fprintf(ofile,"p,q:%g, %g\n",*pptr,*qptr);
  fclose(ofile);
#endif
}

double pycdfsetq( CDFPQ *pycdfob , double q )
{
  double *pptr=pycdfgetpptr(pycdfob);
  double *qptr=pycdfgetqptr(pycdfob);
  *qptr=q;
  *pptr=1.-(*qptr);
  return *qptr;
}

int pycdfbet( CDFBet *sptr )
{
  double *yptr=&(sptr->y);
  pycdfgetq((CDFPQ*)sptr);
  *yptr=1.-sptr->x;
  cdfbet(&(sptr->which),
	 &(sptr->p),
	 &(sptr->q),
	 &(sptr->x),
	 &(sptr->y),
	 &(sptr->a),
	 &(sptr->b),
	 &(sptr->status),
	 &(sptr->bound));
  return sptr->status;
}

int pycdfbin( CDFBin *sptr )
{
  double *ompr=&(sptr->ompr);
  pycdfgetq((CDFPQ*)sptr);
  *ompr=1.-sptr->pr;
  cdfbin(&(sptr->which),
	 &(sptr->p),
	 &(sptr->q),
	 &(sptr->s),
	 &(sptr->xn),
	 &(sptr->pr),
	 &(sptr->ompr),
	 &(sptr->status),
	 &(sptr->bound));
  return sptr->status;
}

int pycdfchi( CDFChi *sptr )
{
  pycdfgetq((CDFPQ*)sptr);
  cdfchi(&(sptr->which),
	 &(sptr->p),
	 &(sptr->q),
	 &(sptr->x),
	 &(sptr->df),
	 &(sptr->status),
	 &(sptr->bound));
  return sptr->status;
}

int pycdfchn( CDFChn *sptr )
{
  pycdfgetq((CDFPQ*)sptr);
  cdfchn(&(sptr->which),
	 &(sptr->p),
	 &(sptr->q),
	 &(sptr->x),
	 &(sptr->df),
	 &(sptr->pnonc),
	 &(sptr->status),
	 &(sptr->bound));
  return sptr->status;
}

int pycdff( CDFF *sptr )
{
  pycdfgetq((CDFPQ*)sptr);
  cdff(  &(sptr->which),
	 &(sptr->p),
	 &(sptr->q),
	 &(sptr->f),
	 &(sptr->dfn),
	 &(sptr->dfd),
	 &(sptr->status),
	 &(sptr->bound));
  return sptr->status;
}

int pycdffnc( CDFFnc *sptr )
{
  pycdfgetq((CDFPQ*)sptr);
  cdffnc(&(sptr->which),
	 &(sptr->p),
	 &(sptr->q),
	 &(sptr->f),
	 &(sptr->dfn),
	 &(sptr->dfd),
	 &(sptr->pnonc),
	 &(sptr->status),
	 &(sptr->bound));
  return sptr->status;
}

int pycdfgam( CDFGam *sptr )
{
  pycdfgetq((CDFPQ*)sptr);
  cdfgam(&(sptr->which),
	 &(sptr->p),
	 &(sptr->q),
	 &(sptr->x),
	 &(sptr->shape),
	 &(sptr->scale),
	 &(sptr->status),
	 &(sptr->bound));
  return sptr->status;
}

int pycdfnbn( CDFNbn *sptr )
{
  pycdfgetq((CDFPQ*)sptr);
  sptr->ompr=1.-sptr->pr;
  cdfnbn(&(sptr->which),
	 &(sptr->p),
	 &(sptr->q),
	 &(sptr->s),
	 &(sptr->xn),
	 &(sptr->pr),
	 &(sptr->ompr),
	 &(sptr->status),
	 &(sptr->bound));
  return sptr->status;
}

int pycdfnor( CDFNor *sptr )
{
  pycdfgetq((CDFPQ*)sptr);
  cdfnor(&(sptr->which),
	 &(sptr->p),
	 &(sptr->q),
	 &(sptr->x),
	 &(sptr->mean),
	 &(sptr->sd),
	 &(sptr->status),
	 &(sptr->bound));
  return sptr->status;
}

int pycdfpoi( CDFPoi *sptr )
{
  pycdfgetq((CDFPQ*)sptr);
  cdfpoi(&(sptr->which),
	 &(sptr->p),
	 &(sptr->q),
	 &(sptr->s),
	 &(sptr->xlam),
	 &(sptr->status),
	 &(sptr->bound));
  return sptr->status;
}

int pycdft( CDFT *sptr )
{
  pycdfgetq((CDFPQ*)sptr);
  cdft(  &(sptr->which),
	 &(sptr->p),
	 &(sptr->q),
	 &(sptr->t),
	 &(sptr->df),
	 &(sptr->status),
	 &(sptr->bound));
  return sptr->status;
}

int pycdftnc( CDFTnc *sptr )
{
  pycdfgetq((CDFPQ*)sptr);
  cdftnc(&(sptr->which),
	 &(sptr->p),
	 &(sptr->q),
	 &(sptr->t),
	 &(sptr->df),
	 &(sptr->pnonc),
	 &(sptr->status),
	 &(sptr->bound));
  return sptr->status;
}

