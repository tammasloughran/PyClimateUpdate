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
import pydcdflibc
class CDFPQPtr :
    def __init__(self,this):
        self.this = this
        self.thisown = 0
    def __del__(self):
        if self.thisown == 1 :
            pydcdflibc.delete_CDFPQ(self.this)
    def __setattr__(self,name,value):
        if name == "which" :
            pydcdflibc.CDFPQ_which_set(self.this,value)
            return
        if name == "p" :
            pydcdflibc.CDFPQ_p_set(self.this,value)
            return
        if name == "q" :
            pydcdflibc.CDFPQ_q_set(self.this,value)
            return
        self.__dict__[name] = value
    def __getattr__(self,name):
        if name == "which" : 
            return pydcdflibc.CDFPQ_which_get(self.this)
        if name == "p" : 
            return pydcdflibc.CDFPQ_p_get(self.this)
        if name == "q" : 
            return pydcdflibc.CDFPQ_q_get(self.this)
        raise AttributeError,name
    def __repr__(self):
        return "<C CDFPQ instance>"
class CDFPQ(CDFPQPtr):
    def __init__(self) :
        self.this = pydcdflibc.new_CDFPQ()
        self.thisown = 1




class CDFBetPtr :
    def __init__(self,this):
        self.this = this
        self.thisown = 0
    def __del__(self):
        if self.thisown == 1 :
            pydcdflibc.delete_CDFBet(self.this)
    def __setattr__(self,name,value):
        if name == "which" :
            pydcdflibc.CDFBet_which_set(self.this,value)
            return
        if name == "p" :
            pydcdflibc.CDFBet_p_set(self.this,value)
            return
        if name == "q" :
            pydcdflibc.CDFBet_q_set(self.this,value)
            return
        if name == "x" :
            pydcdflibc.CDFBet_x_set(self.this,value)
            return
        if name == "y" :
            pydcdflibc.CDFBet_y_set(self.this,value)
            return
        if name == "a" :
            pydcdflibc.CDFBet_a_set(self.this,value)
            return
        if name == "b" :
            pydcdflibc.CDFBet_b_set(self.this,value)
            return
        if name == "status" :
            pydcdflibc.CDFBet_status_set(self.this,value)
            return
        if name == "bound" :
            pydcdflibc.CDFBet_bound_set(self.this,value)
            return
        self.__dict__[name] = value
    def __getattr__(self,name):
        if name == "which" : 
            return pydcdflibc.CDFBet_which_get(self.this)
        if name == "p" : 
            return pydcdflibc.CDFBet_p_get(self.this)
        if name == "q" : 
            return pydcdflibc.CDFBet_q_get(self.this)
        if name == "x" : 
            return pydcdflibc.CDFBet_x_get(self.this)
        if name == "y" : 
            return pydcdflibc.CDFBet_y_get(self.this)
        if name == "a" : 
            return pydcdflibc.CDFBet_a_get(self.this)
        if name == "b" : 
            return pydcdflibc.CDFBet_b_get(self.this)
        if name == "status" : 
            return pydcdflibc.CDFBet_status_get(self.this)
        if name == "bound" : 
            return pydcdflibc.CDFBet_bound_get(self.this)
        raise AttributeError,name
    def __repr__(self):
        return "<C CDFBet instance>"
class CDFBet(CDFBetPtr):
    def __init__(self) :
        self.this = pydcdflibc.new_CDFBet()
        self.thisown = 1




class CDFBinPtr :
    def __init__(self,this):
        self.this = this
        self.thisown = 0
    def __del__(self):
        if self.thisown == 1 :
            pydcdflibc.delete_CDFBin(self.this)
    def __setattr__(self,name,value):
        if name == "which" :
            pydcdflibc.CDFBin_which_set(self.this,value)
            return
        if name == "p" :
            pydcdflibc.CDFBin_p_set(self.this,value)
            return
        if name == "q" :
            pydcdflibc.CDFBin_q_set(self.this,value)
            return
        if name == "s" :
            pydcdflibc.CDFBin_s_set(self.this,value)
            return
        if name == "xn" :
            pydcdflibc.CDFBin_xn_set(self.this,value)
            return
        if name == "pr" :
            pydcdflibc.CDFBin_pr_set(self.this,value)
            return
        if name == "ompr" :
            pydcdflibc.CDFBin_ompr_set(self.this,value)
            return
        if name == "status" :
            pydcdflibc.CDFBin_status_set(self.this,value)
            return
        if name == "bound" :
            pydcdflibc.CDFBin_bound_set(self.this,value)
            return
        self.__dict__[name] = value
    def __getattr__(self,name):
        if name == "which" : 
            return pydcdflibc.CDFBin_which_get(self.this)
        if name == "p" : 
            return pydcdflibc.CDFBin_p_get(self.this)
        if name == "q" : 
            return pydcdflibc.CDFBin_q_get(self.this)
        if name == "s" : 
            return pydcdflibc.CDFBin_s_get(self.this)
        if name == "xn" : 
            return pydcdflibc.CDFBin_xn_get(self.this)
        if name == "pr" : 
            return pydcdflibc.CDFBin_pr_get(self.this)
        if name == "ompr" : 
            return pydcdflibc.CDFBin_ompr_get(self.this)
        if name == "status" : 
            return pydcdflibc.CDFBin_status_get(self.this)
        if name == "bound" : 
            return pydcdflibc.CDFBin_bound_get(self.this)
        raise AttributeError,name
    def __repr__(self):
        return "<C CDFBin instance>"
class CDFBin(CDFBinPtr):
    def __init__(self) :
        self.this = pydcdflibc.new_CDFBin()
        self.thisown = 1




class CDFChiPtr :
    def __init__(self,this):
        self.this = this
        self.thisown = 0
    def __del__(self):
        if self.thisown == 1 :
            pydcdflibc.delete_CDFChi(self.this)
    def __setattr__(self,name,value):
        if name == "which" :
            pydcdflibc.CDFChi_which_set(self.this,value)
            return
        if name == "p" :
            pydcdflibc.CDFChi_p_set(self.this,value)
            return
        if name == "q" :
            pydcdflibc.CDFChi_q_set(self.this,value)
            return
        if name == "x" :
            pydcdflibc.CDFChi_x_set(self.this,value)
            return
        if name == "df" :
            pydcdflibc.CDFChi_df_set(self.this,value)
            return
        if name == "status" :
            pydcdflibc.CDFChi_status_set(self.this,value)
            return
        if name == "bound" :
            pydcdflibc.CDFChi_bound_set(self.this,value)
            return
        self.__dict__[name] = value
    def __getattr__(self,name):
        if name == "which" : 
            return pydcdflibc.CDFChi_which_get(self.this)
        if name == "p" : 
            return pydcdflibc.CDFChi_p_get(self.this)
        if name == "q" : 
            return pydcdflibc.CDFChi_q_get(self.this)
        if name == "x" : 
            return pydcdflibc.CDFChi_x_get(self.this)
        if name == "df" : 
            return pydcdflibc.CDFChi_df_get(self.this)
        if name == "status" : 
            return pydcdflibc.CDFChi_status_get(self.this)
        if name == "bound" : 
            return pydcdflibc.CDFChi_bound_get(self.this)
        raise AttributeError,name
    def __repr__(self):
        return "<C CDFChi instance>"
class CDFChi(CDFChiPtr):
    def __init__(self) :
        self.this = pydcdflibc.new_CDFChi()
        self.thisown = 1




class CDFChnPtr :
    def __init__(self,this):
        self.this = this
        self.thisown = 0
    def __del__(self):
        if self.thisown == 1 :
            pydcdflibc.delete_CDFChn(self.this)
    def __setattr__(self,name,value):
        if name == "which" :
            pydcdflibc.CDFChn_which_set(self.this,value)
            return
        if name == "p" :
            pydcdflibc.CDFChn_p_set(self.this,value)
            return
        if name == "q" :
            pydcdflibc.CDFChn_q_set(self.this,value)
            return
        if name == "x" :
            pydcdflibc.CDFChn_x_set(self.this,value)
            return
        if name == "df" :
            pydcdflibc.CDFChn_df_set(self.this,value)
            return
        if name == "pnonc" :
            pydcdflibc.CDFChn_pnonc_set(self.this,value)
            return
        if name == "status" :
            pydcdflibc.CDFChn_status_set(self.this,value)
            return
        if name == "bound" :
            pydcdflibc.CDFChn_bound_set(self.this,value)
            return
        self.__dict__[name] = value
    def __getattr__(self,name):
        if name == "which" : 
            return pydcdflibc.CDFChn_which_get(self.this)
        if name == "p" : 
            return pydcdflibc.CDFChn_p_get(self.this)
        if name == "q" : 
            return pydcdflibc.CDFChn_q_get(self.this)
        if name == "x" : 
            return pydcdflibc.CDFChn_x_get(self.this)
        if name == "df" : 
            return pydcdflibc.CDFChn_df_get(self.this)
        if name == "pnonc" : 
            return pydcdflibc.CDFChn_pnonc_get(self.this)
        if name == "status" : 
            return pydcdflibc.CDFChn_status_get(self.this)
        if name == "bound" : 
            return pydcdflibc.CDFChn_bound_get(self.this)
        raise AttributeError,name
    def __repr__(self):
        return "<C CDFChn instance>"
class CDFChn(CDFChnPtr):
    def __init__(self) :
        self.this = pydcdflibc.new_CDFChn()
        self.thisown = 1




class CDFFPtr :
    def __init__(self,this):
        self.this = this
        self.thisown = 0
    def __del__(self):
        if self.thisown == 1 :
            pydcdflibc.delete_CDFF(self.this)
    def __setattr__(self,name,value):
        if name == "which" :
            pydcdflibc.CDFF_which_set(self.this,value)
            return
        if name == "p" :
            pydcdflibc.CDFF_p_set(self.this,value)
            return
        if name == "q" :
            pydcdflibc.CDFF_q_set(self.this,value)
            return
        if name == "f" :
            pydcdflibc.CDFF_f_set(self.this,value)
            return
        if name == "dfn" :
            pydcdflibc.CDFF_dfn_set(self.this,value)
            return
        if name == "dfd" :
            pydcdflibc.CDFF_dfd_set(self.this,value)
            return
        if name == "status" :
            pydcdflibc.CDFF_status_set(self.this,value)
            return
        if name == "bound" :
            pydcdflibc.CDFF_bound_set(self.this,value)
            return
        self.__dict__[name] = value
    def __getattr__(self,name):
        if name == "which" : 
            return pydcdflibc.CDFF_which_get(self.this)
        if name == "p" : 
            return pydcdflibc.CDFF_p_get(self.this)
        if name == "q" : 
            return pydcdflibc.CDFF_q_get(self.this)
        if name == "f" : 
            return pydcdflibc.CDFF_f_get(self.this)
        if name == "dfn" : 
            return pydcdflibc.CDFF_dfn_get(self.this)
        if name == "dfd" : 
            return pydcdflibc.CDFF_dfd_get(self.this)
        if name == "status" : 
            return pydcdflibc.CDFF_status_get(self.this)
        if name == "bound" : 
            return pydcdflibc.CDFF_bound_get(self.this)
        raise AttributeError,name
    def __repr__(self):
        return "<C CDFF instance>"
class CDFF(CDFFPtr):
    def __init__(self) :
        self.this = pydcdflibc.new_CDFF()
        self.thisown = 1




class CDFFncPtr :
    def __init__(self,this):
        self.this = this
        self.thisown = 0
    def __del__(self):
        if self.thisown == 1 :
            pydcdflibc.delete_CDFFnc(self.this)
    def __setattr__(self,name,value):
        if name == "which" :
            pydcdflibc.CDFFnc_which_set(self.this,value)
            return
        if name == "p" :
            pydcdflibc.CDFFnc_p_set(self.this,value)
            return
        if name == "q" :
            pydcdflibc.CDFFnc_q_set(self.this,value)
            return
        if name == "f" :
            pydcdflibc.CDFFnc_f_set(self.this,value)
            return
        if name == "dfn" :
            pydcdflibc.CDFFnc_dfn_set(self.this,value)
            return
        if name == "dfd" :
            pydcdflibc.CDFFnc_dfd_set(self.this,value)
            return
        if name == "pnonc" :
            pydcdflibc.CDFFnc_pnonc_set(self.this,value)
            return
        if name == "status" :
            pydcdflibc.CDFFnc_status_set(self.this,value)
            return
        if name == "bound" :
            pydcdflibc.CDFFnc_bound_set(self.this,value)
            return
        self.__dict__[name] = value
    def __getattr__(self,name):
        if name == "which" : 
            return pydcdflibc.CDFFnc_which_get(self.this)
        if name == "p" : 
            return pydcdflibc.CDFFnc_p_get(self.this)
        if name == "q" : 
            return pydcdflibc.CDFFnc_q_get(self.this)
        if name == "f" : 
            return pydcdflibc.CDFFnc_f_get(self.this)
        if name == "dfn" : 
            return pydcdflibc.CDFFnc_dfn_get(self.this)
        if name == "dfd" : 
            return pydcdflibc.CDFFnc_dfd_get(self.this)
        if name == "pnonc" : 
            return pydcdflibc.CDFFnc_pnonc_get(self.this)
        if name == "status" : 
            return pydcdflibc.CDFFnc_status_get(self.this)
        if name == "bound" : 
            return pydcdflibc.CDFFnc_bound_get(self.this)
        raise AttributeError,name
    def __repr__(self):
        return "<C CDFFnc instance>"
class CDFFnc(CDFFncPtr):
    def __init__(self) :
        self.this = pydcdflibc.new_CDFFnc()
        self.thisown = 1




class CDFGamPtr :
    def __init__(self,this):
        self.this = this
        self.thisown = 0
    def __del__(self):
        if self.thisown == 1 :
            pydcdflibc.delete_CDFGam(self.this)
    def __setattr__(self,name,value):
        if name == "which" :
            pydcdflibc.CDFGam_which_set(self.this,value)
            return
        if name == "p" :
            pydcdflibc.CDFGam_p_set(self.this,value)
            return
        if name == "q" :
            pydcdflibc.CDFGam_q_set(self.this,value)
            return
        if name == "x" :
            pydcdflibc.CDFGam_x_set(self.this,value)
            return
        if name == "shape" :
            pydcdflibc.CDFGam_shape_set(self.this,value)
            return
        if name == "scale" :
            pydcdflibc.CDFGam_scale_set(self.this,value)
            return
        if name == "status" :
            pydcdflibc.CDFGam_status_set(self.this,value)
            return
        if name == "bound" :
            pydcdflibc.CDFGam_bound_set(self.this,value)
            return
        self.__dict__[name] = value
    def __getattr__(self,name):
        if name == "which" : 
            return pydcdflibc.CDFGam_which_get(self.this)
        if name == "p" : 
            return pydcdflibc.CDFGam_p_get(self.this)
        if name == "q" : 
            return pydcdflibc.CDFGam_q_get(self.this)
        if name == "x" : 
            return pydcdflibc.CDFGam_x_get(self.this)
        if name == "shape" : 
            return pydcdflibc.CDFGam_shape_get(self.this)
        if name == "scale" : 
            return pydcdflibc.CDFGam_scale_get(self.this)
        if name == "status" : 
            return pydcdflibc.CDFGam_status_get(self.this)
        if name == "bound" : 
            return pydcdflibc.CDFGam_bound_get(self.this)
        raise AttributeError,name
    def __repr__(self):
        return "<C CDFGam instance>"
class CDFGam(CDFGamPtr):
    def __init__(self) :
        self.this = pydcdflibc.new_CDFGam()
        self.thisown = 1




class CDFNbnPtr :
    def __init__(self,this):
        self.this = this
        self.thisown = 0
    def __del__(self):
        if self.thisown == 1 :
            pydcdflibc.delete_CDFNbn(self.this)
    def __setattr__(self,name,value):
        if name == "which" :
            pydcdflibc.CDFNbn_which_set(self.this,value)
            return
        if name == "p" :
            pydcdflibc.CDFNbn_p_set(self.this,value)
            return
        if name == "q" :
            pydcdflibc.CDFNbn_q_set(self.this,value)
            return
        if name == "s" :
            pydcdflibc.CDFNbn_s_set(self.this,value)
            return
        if name == "xn" :
            pydcdflibc.CDFNbn_xn_set(self.this,value)
            return
        if name == "pr" :
            pydcdflibc.CDFNbn_pr_set(self.this,value)
            return
        if name == "ompr" :
            pydcdflibc.CDFNbn_ompr_set(self.this,value)
            return
        if name == "status" :
            pydcdflibc.CDFNbn_status_set(self.this,value)
            return
        if name == "bound" :
            pydcdflibc.CDFNbn_bound_set(self.this,value)
            return
        self.__dict__[name] = value
    def __getattr__(self,name):
        if name == "which" : 
            return pydcdflibc.CDFNbn_which_get(self.this)
        if name == "p" : 
            return pydcdflibc.CDFNbn_p_get(self.this)
        if name == "q" : 
            return pydcdflibc.CDFNbn_q_get(self.this)
        if name == "s" : 
            return pydcdflibc.CDFNbn_s_get(self.this)
        if name == "xn" : 
            return pydcdflibc.CDFNbn_xn_get(self.this)
        if name == "pr" : 
            return pydcdflibc.CDFNbn_pr_get(self.this)
        if name == "ompr" : 
            return pydcdflibc.CDFNbn_ompr_get(self.this)
        if name == "status" : 
            return pydcdflibc.CDFNbn_status_get(self.this)
        if name == "bound" : 
            return pydcdflibc.CDFNbn_bound_get(self.this)
        raise AttributeError,name
    def __repr__(self):
        return "<C CDFNbn instance>"
class CDFNbn(CDFNbnPtr):
    def __init__(self) :
        self.this = pydcdflibc.new_CDFNbn()
        self.thisown = 1




class CDFNorPtr :
    def __init__(self,this):
        self.this = this
        self.thisown = 0
    def __del__(self):
        if self.thisown == 1 :
            pydcdflibc.delete_CDFNor(self.this)
    def __setattr__(self,name,value):
        if name == "which" :
            pydcdflibc.CDFNor_which_set(self.this,value)
            return
        if name == "p" :
            pydcdflibc.CDFNor_p_set(self.this,value)
            return
        if name == "q" :
            pydcdflibc.CDFNor_q_set(self.this,value)
            return
        if name == "x" :
            pydcdflibc.CDFNor_x_set(self.this,value)
            return
        if name == "mean" :
            pydcdflibc.CDFNor_mean_set(self.this,value)
            return
        if name == "sd" :
            pydcdflibc.CDFNor_sd_set(self.this,value)
            return
        if name == "status" :
            pydcdflibc.CDFNor_status_set(self.this,value)
            return
        if name == "bound" :
            pydcdflibc.CDFNor_bound_set(self.this,value)
            return
        self.__dict__[name] = value
    def __getattr__(self,name):
        if name == "which" : 
            return pydcdflibc.CDFNor_which_get(self.this)
        if name == "p" : 
            return pydcdflibc.CDFNor_p_get(self.this)
        if name == "q" : 
            return pydcdflibc.CDFNor_q_get(self.this)
        if name == "x" : 
            return pydcdflibc.CDFNor_x_get(self.this)
        if name == "mean" : 
            return pydcdflibc.CDFNor_mean_get(self.this)
        if name == "sd" : 
            return pydcdflibc.CDFNor_sd_get(self.this)
        if name == "status" : 
            return pydcdflibc.CDFNor_status_get(self.this)
        if name == "bound" : 
            return pydcdflibc.CDFNor_bound_get(self.this)
        raise AttributeError,name
    def __repr__(self):
        return "<C CDFNor instance>"
class CDFNor(CDFNorPtr):
    def __init__(self) :
        self.this = pydcdflibc.new_CDFNor()
        self.thisown = 1




class CDFPoiPtr :
    def __init__(self,this):
        self.this = this
        self.thisown = 0
    def __del__(self):
        if self.thisown == 1 :
            pydcdflibc.delete_CDFPoi(self.this)
    def __setattr__(self,name,value):
        if name == "which" :
            pydcdflibc.CDFPoi_which_set(self.this,value)
            return
        if name == "p" :
            pydcdflibc.CDFPoi_p_set(self.this,value)
            return
        if name == "q" :
            pydcdflibc.CDFPoi_q_set(self.this,value)
            return
        if name == "s" :
            pydcdflibc.CDFPoi_s_set(self.this,value)
            return
        if name == "xlam" :
            pydcdflibc.CDFPoi_xlam_set(self.this,value)
            return
        if name == "status" :
            pydcdflibc.CDFPoi_status_set(self.this,value)
            return
        if name == "bound" :
            pydcdflibc.CDFPoi_bound_set(self.this,value)
            return
        self.__dict__[name] = value
    def __getattr__(self,name):
        if name == "which" : 
            return pydcdflibc.CDFPoi_which_get(self.this)
        if name == "p" : 
            return pydcdflibc.CDFPoi_p_get(self.this)
        if name == "q" : 
            return pydcdflibc.CDFPoi_q_get(self.this)
        if name == "s" : 
            return pydcdflibc.CDFPoi_s_get(self.this)
        if name == "xlam" : 
            return pydcdflibc.CDFPoi_xlam_get(self.this)
        if name == "status" : 
            return pydcdflibc.CDFPoi_status_get(self.this)
        if name == "bound" : 
            return pydcdflibc.CDFPoi_bound_get(self.this)
        raise AttributeError,name
    def __repr__(self):
        return "<C CDFPoi instance>"
class CDFPoi(CDFPoiPtr):
    def __init__(self) :
        self.this = pydcdflibc.new_CDFPoi()
        self.thisown = 1




class CDFTPtr :
    def __init__(self,this):
        self.this = this
        self.thisown = 0
    def __del__(self):
        if self.thisown == 1 :
            pydcdflibc.delete_CDFT(self.this)
    def __setattr__(self,name,value):
        if name == "which" :
            pydcdflibc.CDFT_which_set(self.this,value)
            return
        if name == "p" :
            pydcdflibc.CDFT_p_set(self.this,value)
            return
        if name == "q" :
            pydcdflibc.CDFT_q_set(self.this,value)
            return
        if name == "t" :
            pydcdflibc.CDFT_t_set(self.this,value)
            return
        if name == "df" :
            pydcdflibc.CDFT_df_set(self.this,value)
            return
        if name == "status" :
            pydcdflibc.CDFT_status_set(self.this,value)
            return
        if name == "bound" :
            pydcdflibc.CDFT_bound_set(self.this,value)
            return
        self.__dict__[name] = value
    def __getattr__(self,name):
        if name == "which" : 
            return pydcdflibc.CDFT_which_get(self.this)
        if name == "p" : 
            return pydcdflibc.CDFT_p_get(self.this)
        if name == "q" : 
            return pydcdflibc.CDFT_q_get(self.this)
        if name == "t" : 
            return pydcdflibc.CDFT_t_get(self.this)
        if name == "df" : 
            return pydcdflibc.CDFT_df_get(self.this)
        if name == "status" : 
            return pydcdflibc.CDFT_status_get(self.this)
        if name == "bound" : 
            return pydcdflibc.CDFT_bound_get(self.this)
        raise AttributeError,name
    def __repr__(self):
        return "<C CDFT instance>"
class CDFT(CDFTPtr):
    def __init__(self) :
        self.this = pydcdflibc.new_CDFT()
        self.thisown = 1




class CDFTncPtr :
    def __init__(self,this):
        self.this = this
        self.thisown = 0
    def __del__(self):
        if self.thisown == 1 :
            pydcdflibc.delete_CDFTnc(self.this)
    def __setattr__(self,name,value):
        if name == "which" :
            pydcdflibc.CDFTnc_which_set(self.this,value)
            return
        if name == "p" :
            pydcdflibc.CDFTnc_p_set(self.this,value)
            return
        if name == "q" :
            pydcdflibc.CDFTnc_q_set(self.this,value)
            return
        if name == "t" :
            pydcdflibc.CDFTnc_t_set(self.this,value)
            return
        if name == "df" :
            pydcdflibc.CDFTnc_df_set(self.this,value)
            return
        if name == "pnonc" :
            pydcdflibc.CDFTnc_pnonc_set(self.this,value)
            return
        if name == "status" :
            pydcdflibc.CDFTnc_status_set(self.this,value)
            return
        if name == "bound" :
            pydcdflibc.CDFTnc_bound_set(self.this,value)
            return
        self.__dict__[name] = value
    def __getattr__(self,name):
        if name == "which" : 
            return pydcdflibc.CDFTnc_which_get(self.this)
        if name == "p" : 
            return pydcdflibc.CDFTnc_p_get(self.this)
        if name == "q" : 
            return pydcdflibc.CDFTnc_q_get(self.this)
        if name == "t" : 
            return pydcdflibc.CDFTnc_t_get(self.this)
        if name == "df" : 
            return pydcdflibc.CDFTnc_df_get(self.this)
        if name == "pnonc" : 
            return pydcdflibc.CDFTnc_pnonc_get(self.this)
        if name == "status" : 
            return pydcdflibc.CDFTnc_status_get(self.this)
        if name == "bound" : 
            return pydcdflibc.CDFTnc_bound_get(self.this)
        raise AttributeError,name
    def __repr__(self):
        return "<C CDFTnc instance>"
class CDFTnc(CDFTncPtr):
    def __init__(self) :
        self.this = pydcdflibc.new_CDFTnc()
        self.thisown = 1






#-------------- FUNCTION WRAPPERS ------------------

def pycdfsetq(arg0,arg1):
    val = pydcdflibc.pycdfsetq(arg0.this,arg1)
    return val

def pycdfbet(arg0):
    val = pydcdflibc.pycdfbet(arg0.this)
    return val

def pycdfbin(arg0):
    val = pydcdflibc.pycdfbin(arg0.this)
    return val

def pycdfchi(arg0):
    val = pydcdflibc.pycdfchi(arg0.this)
    return val

def pycdfchn(arg0):
    val = pydcdflibc.pycdfchn(arg0.this)
    return val

def pycdff(arg0):
    val = pydcdflibc.pycdff(arg0.this)
    return val

def pycdffnc(arg0):
    val = pydcdflibc.pycdffnc(arg0.this)
    return val

def pycdfgam(arg0):
    val = pydcdflibc.pycdfgam(arg0.this)
    return val

def pycdfnbn(arg0):
    val = pydcdflibc.pycdfnbn(arg0.this)
    return val

def pycdfnor(arg0):
    val = pydcdflibc.pycdfnor(arg0.this)
    return val

def pycdfpoi(arg0):
    val = pydcdflibc.pycdfpoi(arg0.this)
    return val

def pycdft(arg0):
    val = pydcdflibc.pycdft(arg0.this)
    return val

def pycdftnc(arg0):
    val = pydcdflibc.pycdftnc(arg0.this)
    return val



#-------------- VARIABLE WRAPPERS ------------------

__pycdf__ = pydcdflibc.__pycdf__
