import array
import numpy as np

from quickstats import semistaticmethod
from quickstats.interface.root import TObject, TArrayData
from quickstats.interface.cppyy.vectorize import c_array_to_np_array

class TH3(TObject):
    
    DTYPE_MAP = {
        "TH3I": "int",
        "TH3F": "float",
        "TH3D": "double"
    }
    
    def __init__(self, h:"ROOT.TH3", underflow_bin:bool=False, overflow_bin:bool=False):
        import ROOT
        dtype_map = {
            ROOT.TH3I: "int",
            ROOT.TH3F: "float",
            ROOT.TH3D: "double"
        }
        self.dtype = dtype_map.get(type(h), "double")
        self.underflow_bin = underflow_bin
        self.overflow_bin  = overflow_bin
        self.init(h)
        
    def get_fundamental_type(self):
        import ROOT
        return ROOT.TH3
        
    def init(self, h):
        self.bin_content    = self.GetBinContentArray(h, self.dtype, self.underflow_bin, self.overflow_bin)
        self.x_bin_center   = self.GetXBinCenterArray(h, self.dtype, self.underflow_bin, self.overflow_bin)
        self.y_bin_center   = self.GetYBinCenterArray(h, self.dtype, self.underflow_bin, self.overflow_bin)
        self.z_bin_center   = self.GetZBinCenterArray(h, self.dtype, self.underflow_bin, self.overflow_bin)
        self.x_bin_width    = self.GetXBinWidthArray(h, self.dtype, self.underflow_bin, self.overflow_bin)
        self.y_bin_width    = self.GetYBinWidthArray(h, self.dtype, self.underflow_bin, self.overflow_bin)
        self.z_bin_width    = self.GetZBinWidthArray(h, self.dtype, self.underflow_bin, self.overflow_bin)
        self.x_bin_low_edge = self.GetXBinLowEdgeArray(h, self.dtype, self.underflow_bin, self.overflow_bin)
        self.y_bin_low_edge = self.GetYBinLowEdgeArray(h, self.dtype, self.underflow_bin, self.overflow_bin)
        self.z_bin_low_edge = self.GetZBinLowEdgeArray(h, self.dtype, self.underflow_bin, self.overflow_bin)
        
    @staticmethod
    def GetBinContentArray(h, dtype:str='double', underflow_bin:bool=False, overflow_bin:bool=False):
        arr = h.GetArray()
        n_bins_x = h.GetNbinsX()
        n_bins_y = h.GetNbinsY()
        n_bins_z = h.GetNbinsZ()
        # account for underflow and overflow bins
        size = (n_bins_x + 2) * (n_bins_y + 2) * (n_bins_z + 2)
        np_arr = c_array_to_np_array(arr, size=size)
        np_arr = np_arr.reshape((n_bins_x + 2, n_bins_y + 2, n_bins_z + 2), order='F')
        x_start = 1 if not underflow_bin else 0
        y_start = x_start
        z_start = x_start
        x_end = -1 if not overflow_bin else n_bins_x + 2
        y_end = -1 if not overflow_bin else n_bins_y + 2
        z_end = -1 if not overflow_bin else n_bins_z + 2
        np_arr = np_arr[x_start:x_end, y_start:y_end, z_start:z_end]
        return np_arr
    
    @staticmethod
    def GetXLabelArray(h:"ROOT.TH2"):
        return np.array(h.GetXaxis().GetLabels(), dtype=str)
    
    @staticmethod
    def GetYLabelArray(h:"ROOT.TH2"):
        return np.array(h.GetYaxis().GetLabels(), dtype=str)
    
    @staticmethod
    def GetZLabelArray(h:"ROOT.TH2"):
        return np.array(h.GetYaxis().GetLabels(), dtype=str)
    
    @staticmethod
    def GetAxisBinCenterArray(ax:"ROOT.TAxis", dtype:str='double', underflow_bin:int=0, overflow_bin:int=0):
        import ROOT
        c_vector = ROOT.TAxisUtils.GetBinCenterArray[dtype](ax, underflow_bin, overflow_bin)
        return TArrayData.vec_to_array(c_vector)
    
    @staticmethod
    def GetAxisBinWidthArray(ax:"ROOT.TAxis", dtype:str='double', underflow_bin:int=0, overflow_bin:int=0):
        import ROOT
        c_vector = ROOT.TAxisUtils.GetBinWidthArray[dtype](ax, underflow_bin, overflow_bin)
        return TArrayData.vec_to_array(c_vector)

    @staticmethod
    def GetAxisBinLowEdgeArray(ax:"ROOT.TAxis", dtype:str='double', underflow_bin:int=0, overflow_bin:int=0):
        import ROOT
        c_vector = ROOT.TAxisUtils.GetBinLowEdgeArray[dtype](ax, underflow_bin, overflow_bin)
        return TArrayData.vec_to_array(c_vector)

    @staticmethod
    def GetXBinCenterArray(h:"ROOT.TH2", dtype:str='double', underflow_bin:bool=False, overflow_bin:bool=False):
        return TH2.GetAxisBinCenterArray(h.GetXaxis(), dtype, underflow_bin, overflow_bin)
    
    @staticmethod
    def GetYBinCenterArray(h:"ROOT.TH2", dtype:str='double', underflow_bin:bool=False, overflow_bin:bool=False):
        return TH2.GetAxisBinCenterArray(h.GetYaxis(), dtype, underflow_bin, overflow_bin)
    
    @staticmethod
    def GetZBinCenterArray(h:"ROOT.TH2", dtype:str='double', underflow_bin:bool=False, overflow_bin:bool=False):
        return TH2.GetAxisBinCenterArray(h.GetZaxis(), dtype, underflow_bin, overflow_bin)
    
    @staticmethod
    def GetXBinWidthArray(h:"ROOT.TH2", dtype:str='double', underflow_bin:bool=False, overflow_bin:bool=False):
        return TH2.GetAxisBinWidthArray(h.GetXaxis(), dtype, underflow_bin, overflow_bin)
    
    @staticmethod
    def GetYBinWidthArray(h:"ROOT.TH2", dtype:str='double', underflow_bin:bool=False, overflow_bin:bool=False):
        return TH2.GetAxisBinWidthArray(h.GetYaxis(), dtype, underflow_bin, overflow_bin)
    
    @staticmethod
    def GetZBinWidthArray(h:"ROOT.TH2", dtype:str='double', underflow_bin:bool=False, overflow_bin:bool=False):
        return TH2.GetAxisBinWidthArray(h.GetZaxis(), dtype, underflow_bin, overflow_bin)

    @staticmethod
    def GetXBinLowEdgeArray(h:"ROOT.TH2", dtype:str='double', underflow_bin:int=0, overflow_bin:int=0):
        return TH2.GetAxisBinLowEdgeArray(h.GetXaxis(), dtype, underflow_bin, overflow_bin)
    
    @staticmethod
    def GetYBinLowEdgeArray(h:"ROOT.TH2", dtype:str='double', underflow_bin:int=0, overflow_bin:int=0):
        return TH2.GetAxisBinLowEdgeArray(h.GetYaxis(), dtype, underflow_bin, overflow_bin)
    
    @staticmethod
    def GetZBinLowEdgeArray(h:"ROOT.TH2", dtype:str='double', underflow_bin:int=0, overflow_bin:int=0):
        return TH2.GetAxisBinLowEdgeArray(h.GetZaxis(), dtype, underflow_bin, overflow_bin)