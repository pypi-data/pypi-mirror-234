from typing import Dict, Optional, Union, List, Tuple
import pandas as pd
import numpy as np

from quickstats.plots import AbstractPlot
from quickstats.plots.template import format_axis_ticks
from quickstats.maths.interpolation import interpolate_2d
from quickstats.utils.common_utils import combine_dict

class General2DPlot(AbstractPlot):
    
    STYLES = {
        'pcolormesh': {
            'cmap': 'GnBu',
            'shading': 'auto'
        },
        'colorbar': {
            'pad': 0.02,
        },
        'contour': {
            'linestyles': 'solid',
            'linewidths': 3
        },
        'scatter': {
            'c': 'hh:darkpink',
            'marker': 'o',
            's': 40,
            'edgecolors': 'hh:darkblue',
            'alpha': 0.7,
            'linewidth': 1,
        },
        'legend': {
            'handletextpad': 0.,
        },
        'clabel': {
            'inline': True,
            'fontsize': 10
        }
    }
    
    CONFIG = {
        'interpolate_method': 'cubic',
        'num_grid_points': 500
    }    
    
    def __init__(self, data:pd.DataFrame,
                 styles:Optional[Union[Dict, str]]=None,
                 analysis_label_options:Optional[Dict]=None,
                 config:Optional[Dict]=None):
        
        self.data = data
        
        super().__init__(styles=styles,
                         analysis_label_options=analysis_label_options,
                         config=config)
    
    def draw(self, xattrib:str, yattrib:str, zattrib:str,
             xlabel:Optional[str]=None, ylabel:Optional[str]=None,
             ymin:Optional[float]=None, ymax:Optional[float]=None,
             xmin:Optional[float]=None, xmax:Optional[float]=None,
             zmin:Optional[float]=None, zmax:Optional[float]=None,
             logx:bool=False, logy:bool=False, norm:Optional=None,
             draw_colormesh:bool=True, draw_contour:bool=False,
             draw_scatter:bool=False, draw_clabel:bool=True,
             contour_levels:Optional[Union[float, List[float]]]=None, ax=None):
        
        if ax is None:
            ax = self.draw_frame(logx=logx, logy=logy)
        
        data = self.data
        x, y, z = data[xattrib], data[yattrib], data[zattrib]
        interp_method = self.config['interpolate_method']
        n = self.config['num_grid_points']
        if draw_colormesh or draw_contour:
            X, Y, Z = interpolate_2d(x, y, z, method=interp_method, n=n)
            self.Z = Z
        if draw_colormesh:
            pcm_styles = combine_dict(self.styles['pcolormesh'])
            if norm is not None:
                pcm_styles.pop('vmin', None)
                pcm_styles.pop('vmax', None)
            pcm = ax.pcolormesh(X, Y, Z, norm=norm, **pcm_styles)
            import matplotlib.pyplot as plt
            cbar = plt.colorbar(pcm, ax=ax, **self.styles['colorbar'])
            format_axis_ticks(cbar.ax, **self.styles['cbar_axis'])
            #self.cbar.set_label(**config['colorbar_label'])
        
        if draw_contour:
            handle = ax.contour(X, Y, Z, levels=contour_levels, **self.styles['contour'])
             
            if draw_clabel:
                ax.clabel(handle, **self.styles['clabel'])             
        
        if draw_scatter:
            handle = ax.scatter(x, y, **self.styles['scatter'])
            ax.legend(**self.styles['legend'])
             
        self.draw_axis_components(ax, xlabel=xlabel, ylabel=ylabel)
        self.set_axis_range(ax, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)
        
        return ax
