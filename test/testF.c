/***

A simple file that tests a problem in the original C DCDFLIB.C library and
which shows that the problem is not Python-specific

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


***/
#include <stdio.h>
#include "cdflib.h"

int main( void );
void printparameters(double p, double q , double f,  double dfn , double dfd , double bo , int s )
{
  printf("p,q,f:%g,%g %g\n",p,q,f);
  printf("dfn,dfd:%g,%g\n",dfn,dfd);
  printf("bo,s:%g,%d\n",bo,s);
}

int main( void )
{
  int which,status;
  double p,q,f,dfn,dfd,bound;

  p=0.95;
  q=1.-p;
  dfn=6.0;
  dfd=5.0;
  bound=1.0e50;
  which=2;
  /** Compute  F to initialize the parameters **/
  cdff(&which,&p,&q,&f,&dfn,&dfd,&status,&bound);
  printparameters(p,q,f,dfn,dfd,bound,status);
  /*** Recompute dfn, dfd **/
  which=3;
  cdff(&which,&p,&q,&f,&dfn,&dfd,&status,&bound);
  printparameters(p,q,f,dfn,dfd,bound,status);
  return 0;
}
