import os
import yaml
from typing import Optional, Dict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from quickstats.utils.common_utils import combine_dict

STYLES = {
    "default": {
        'cmap': 'seismic',
        'value_color': 'black'
    },
    "viridis": {
        'cmap': 'viridis',
        'value_color': 'black'
    }
}

class CorrelationPlot():
    
    CONFIG = {
        'cax_kwargs': {
            'position': 'right',
            'size': '5%',
            'pad' : 0.05
        },
        'colorbar_kwargs': {
        }
    }
    
    def __init__(self, data:pd.DataFrame, label_map:Optional[Dict]=None,
                 config:Optional[Dict]=None):
        
        self.data = data
        self.label_map = label_map
        self.config = combine_dict(self.CONFIG, config)
        
    @staticmethod
    def parse_style(style:Optional[str]=None):
        if not style:
            return STYLES["default"]
        elif isinstance(style, dict):
            return style
        if os.path.exists(style):
            return yaml.safe_load(open(style))
        _style = STYLES.get(style.lower(), None)
        if not _style:
            raise ValueError(f'unknown style: {style}')
        return _style
        
    def draw(self, cmap:str='seismic', xlabel_rotation:float=90, ylabel_rotation:float=0, label_size:float=25,
             figscale:int=1, show_values:bool=True, value_color:str="black", value_size=16, value_precision:int=2,
             gridline:Optional[str]="--", gridcolor:str="black", xlabelpad:Optional[float]=None,
             ylabelpad:Optional[float]=None, vmin:float=-1, vmax:float=1, norm:Optional=None,
             draw_colorbar:bool=False):
        if norm is not None:
            vmin, vmax = None, None
        if self.label_map is None:
            label_map = {}
        else:
            label_map = combine_dict(self.label_map)
        plt.clf()
        size = np.max([len(self.data.columns), len(self.data.index)])
        figsize = size * figscale
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(figsize, figsize), facecolor= "#FFFFFF", dpi=72)
        handle = ax.matshow(self.data, cmap=cmap, norm=norm, vmin=vmin, vmax=vmax)
        if draw_colorbar:
            figure = plt.gcf()
            from mpl_toolkits.axes_grid1 import make_axes_locatable
            divider = make_axes_locatable(ax)
            cax = divider.append_axes(**self.config['cax_kwargs'])
            figure.colorbar(handle, cax=cax, **self.config['colorbar_kwargs'])
        xticks = np.arange(0, len(self.data.columns), 1)
        yticks = np.arange(0, len(self.data.index), 1)
        ax.set_xticks(xticks)
        ax.set_yticks(yticks)
        ax.set_xticklabels([label_map.get(label, label) for label in self.data.columns],
                           rotation=xlabel_rotation,
                           fontsize=label_size)
        if xlabelpad is not None:
            ax.tick_params(axis='x', which='major', pad=xlabelpad)
        ax.set_yticklabels([label_map.get(label, label) for label in self.data.index],
                           rotation=ylabel_rotation,
                           fontsize=label_size)
        if ylabelpad is not None:
            ax.tick_params(axis='y', which='major', pad=ylabelpad)
        ax.tick_params(axis="both", which="both", length=0)
        if show_values:
            fmt_str = f'{{:0.{value_precision}f}}'
            for (i, j), z in np.ndenumerate(self.data.values):
                ax.text(j, i, fmt_str.format(z), ha='center', va='center', color=value_color, fontsize=value_size)
        if gridline:
            for i in range(len(yticks) - 1):
                ax.axhline(i + 0.5, linestyle=gridline, color=gridcolor)
            for i in range(len(xticks) - 1):
                ax.axvline(i + 0.5, linestyle=gridline, color=gridcolor)
        return ax
    
    def draw_style(self, style:Optional[Dict]=None):
        style = self.parse_style(style)
        return self.draw(**style)