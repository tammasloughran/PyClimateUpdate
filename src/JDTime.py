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
# This file was created automatically by SWIG.
import JDTimec
class JDTimePtr :
    def __init__(self,this):
        self.this = this
        self.thisown = 0
    def __del__(self):
        if self.thisown == 1 :
            JDTimec.delete_JDTime(self.this)
    def __setattr__(self,name,value):
        if name == "year" :
            JDTimec.JDTime_year_set(self.this,value)
            return
        if name == "month" :
            JDTimec.JDTime_month_set(self.this,value)
            return
        if name == "day" :
            JDTimec.JDTime_day_set(self.this,value)
            return
        if name == "hour" :
            JDTimec.JDTime_hour_set(self.this,value)
            return
        if name == "minute" :
            JDTimec.JDTime_minute_set(self.this,value)
            return
        if name == "second" :
            JDTimec.JDTime_second_set(self.this,value)
            return
        self.__dict__[name] = value
    def __getattr__(self,name):
        if name == "year" : 
            return JDTimec.JDTime_year_get(self.this)
        if name == "month" : 
            return JDTimec.JDTime_month_get(self.this)
        if name == "day" : 
            return JDTimec.JDTime_day_get(self.this)
        if name == "hour" : 
            return JDTimec.JDTime_hour_get(self.this)
        if name == "minute" : 
            return JDTimec.JDTime_minute_get(self.this)
        if name == "second" : 
            return JDTimec.JDTime_second_get(self.this)
        raise AttributeError,name
    def __repr__(self):
        return "<C JDTime instance>"
class JDTime(JDTimePtr):
    def __init__(self) :
        self.this = JDTimec.new_JDTime()
        self.thisown = 1






#-------------- FUNCTION WRAPPERS ------------------

def date2jd(arg0):
    val = JDTimec.date2jd(arg0.this)
    return val

def jd2date(arg0,arg1):
    val = JDTimec.jd2date(arg0,arg1.this)
    return val

monthlystep = JDTimec.monthlystep



#-------------- VARIABLE WRAPPERS ------------------

