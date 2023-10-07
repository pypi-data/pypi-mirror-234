from typing import Dict, Optional, Union, List
import pandas as pd
import numpy as np

from quickstats.plots import General1DPlot
from quickstats.plots.template import create_transform
from quickstats.utils.common_utils import combine_dict

class Likelihood1DPlot(General1DPlot):
    
    STYLES = {
        'annotation':{
            'fontsize': 20
        },
        'text':{
            'fontsize': 20
        }
    }
    
    CONFIG = {
        # intervals to include in the plot
        "interval_formats": {
            "68_95"         : ('0.68', '0.95'),
            "one_two_sigma" : ('1sigma', '2sigma')
        },
        'sigma_line_styles':{
            'color': 'gray',
            'linestyle': '--'
        },
        'sigma_text_styles':{
            'x': 0.98,
            'ha': 'right',
            'color': 'gray'
        },        
        'sigma_interval_styles':{
            'loc': (0.2, 0.4),
            'main_text': '',
            'sigma_text': r'{sigma_label}: {xlabel}$\in {intervals}$',
            'dy': 0.05,
            'decimal_place': 2
        }
    }
    
    coverage_proba_data = {
        '0.68': {
            'qmu': 0.99,
            'label': '68% CL'
        },
        '1sigma': {  
            'qmu': 1, # 68.2%
            'label': '1 $\sigma$'
        },
        '0.95': {
            'qmu': 3.84,
            'label': '95% CL'
        },
        '2sigma': {
            'qmu': 4,
            'label': '2 $\sigma$'
        }
    }    
    
    def __init__(self, data_map:Union[pd.DataFrame, Dict[str, pd.DataFrame]],
                 label_map:Optional[Dict]=None,
                 styles_map:Optional[Dict]=None,
                 color_cycle=None,
                 styles:Optional[Union[Dict, str]]=None,
                 analysis_label_options:Optional[Dict]=None,
                 config:Optional[Dict]=None):
        super().__init__(data_map=data_map,
                         label_map=label_map,
                         styles_map=styles_map,
                         color_cycle=color_cycle,
                         styles=styles,
                         analysis_label_options=analysis_label_options,
                         config=config)
        self.intervals = {}
    
    def get_sigma_levels_values_labels(self, interval_format:Union[str, List[str]]="one_two_sigma"):
        if isinstance(interval_format, (list, tuple)):
            sigma_levels = list(interval_format)
        else:
            if interval_format not in self.config['interval_formats']:
                choices = ','.join([f'"{choice}"' for choice in self.config['interval_formats']])
                raise ValueError(f'undefined sigma interval format: {interval_format} (choose from {choices})')
            sigma_levels = self.config['interval_formats'][interval_format]
        sigma_values = []
        sigma_labels = []
        for sigma_level in sigma_levels:
            if sigma_level not in self.coverage_proba_data:
                raise RuntimeError(f'undefined sigma level: {sigma_level}')
            sigma_values.append(self.coverage_proba_data[sigma_level]['qmu'])
            sigma_labels.append(self.coverage_proba_data[sigma_level]['label'])
        return sigma_levels, sigma_values, sigma_labels
    
    def get_sigma_intervals(self, x:np.ndarray, y:np.ndarray,
                            interval_format:Union[str, List[str]]="one_two_sigma"):
        from quickstats.maths.interpolation import get_intervals
        sigma_levels, sigma_values, sigma_labels = self.get_sigma_levels_values_labels(interval_format)
        sigma_intervals = {}
        for i, (sigma_level, sigma_value, sigma_label) in enumerate(zip(sigma_levels, sigma_values, sigma_labels)):
            intervals = get_intervals(x, y, sigma_value)
            sigma_intervals[sigma_level] = intervals
        return sigma_intervals
    
    def get_bestfit(self, x:np.ndarray, y:np.ndarray):
        bestfit_idx = np.argmin(y)
        bestfit_x   = x[bestfit_idx]
        bestfit_y   = y[bestfit_idx]
        return bestfit_x, bestfit_y
        
    def draw_sigma_lines(self, ax, interval_format:Union[str, List[str]]="one_two_sigma"):
        sigma_line_styles = self.config['sigma_line_styles']
        sigma_levels, sigma_values, sigma_labels = self.get_sigma_levels_values_labels(interval_format)
        transform = create_transform(transform_x="axis", transform_y="data")
        ax.hlines(sigma_values, xmin=0, xmax=1, zorder=0, transform=transform,
                  **self.config['sigma_line_styles'])
        styles = combine_dict(self.styles['text'], self.config['sigma_text_styles'])
        if 'va' not in styles:
            styles['va'] = 'bottom' if ((styles['x'] > 0) and (styles['x'] < 1)) else 'center'
        for sigma_value, sigma_label in zip(sigma_values, sigma_labels):
            ax.text(y=sigma_value, s=sigma_label, **styles, transform=transform)
    
    def draw_sigma_intervals(self, ax, x:np.ndarray, y:np.ndarray, xlabel:str="",
                             interval_format:Union[str, List[str]]="one_two_sigma"):
        from quickstats.maths.interpolation import get_intervals
        sigma_levels, sigma_values, sigma_labels = self.get_sigma_levels_values_labels(interval_format)
        sigma_intervals = self.get_sigma_intervals(x, y, interval_format=interval_format)
        self.intervals  = sigma_intervals
        styles     = self.config['sigma_interval_styles']
        loc        = styles['loc']
        dp         = styles['decimal_place']
        dy         = styles['dy']
        sigma_text = styles['sigma_text']
        # do not draw when no intervals available
        if all(len(intervals) == 0 for intervals in sigma_intervals.values()):
            return None
        ax.annotate(styles['main_text'], loc, xycoords='axes fraction', **self.styles['annotation'])
        for i, (sigma_level, sigma_label) in enumerate(zip(sigma_levels, sigma_labels)):
            sigma_interval = sigma_intervals[sigma_level]
            if len(sigma_interval) == 0:
                continue
            interval_str = r" \cup ".join([f"[{lo:.{dp}f}, {hi:.{dp}f}]" for (lo, hi) in sigma_interval])
            interval_str = interval_str.replace('-inf', r'N.A.').replace('inf', 'N.A.')
            text = sigma_text.format(sigma_label=sigma_label,
                                     xlabel=xlabel,
                                     intervals=interval_str)
            ax.annotate(text, (loc[0], loc[1] - (i + 1) * dy),
                        xycoords='axes fraction', **self.styles['annotation'])

    def draw(self, xattrib:str='mu', yattrib:str='qmu', xlabel:Optional[str]=None, 
             ylabel:Optional[str]="$-2\Delta ln(L)$", targets:Optional[List[str]]=None,
             ymin:float=0, ymax:float=7, xmin:Optional[float]=None, xmax:Optional[float]=None,
             draw_sigma_line:bool=True,
             #draw_sm_line:bool=False,
             draw_sigma_intervals:Union[str, bool]=False,
             interval_format:Union[str, List[str]]="one_two_sigma"):
        # ylabel = "$-2\Delta ln(L)$"
        ax = super().draw(xattrib=xattrib, yattrib=yattrib,
                          xlabel=xlabel, ylabel=ylabel, targets=targets,
                          ymin=ymin, ymax=ymax, xmin=xmin, xmax=xmax)

        if draw_sigma_line:
            self.draw_sigma_lines(ax, interval_format=interval_format)
            
        """
        if draw_sm_line:
            transform = create_transform(transform_y="axis", transform_x="data")
            sm_line_styles = self.config['sm_line_styles']
            sm_values = self.config['sm_values']
            sm_names = self.config['sm_names']
            ax.vlines(sm_values, ymin=0, ymax=1, zorder=0, transform=transform,
                      **sm_line_styles)
            if sm_names:
                sm_pos = self.config['sm_pos']
                for sm_value, sm_name in zip(sm_values, sm_names):
                    ax.text(sm_value, sm_pos, sm_name, color='gray', ha='right', rotation=90,
                            va='bottom' if (sm_pos > 0 and sm_pos < 1) else 'center', fontsize=20, transform=transform)
        """
        
        if draw_sigma_intervals:
            if isinstance(self.data_map, pd.DataFrame):
                x = self.data_map[xattrib].values
                y = self.data_map[yattrib].values
            elif isinstance(self.data_map, dict):
                if not isinstance(draw_sigma_intervals, str):
                    raise RuntimeError("name of the target likelihood curve must be specified "
                                       "when drawing sigma intervals")
                target = draw_sigma_intervals
                x = self.data_map[target][xattrib].values
                y = self.data_map[target][yattrib].values
            else:
                raise ValueError("invalid data format")
            self.draw_sigma_intervals(ax, x, y, xlabel=xlabel, interval_format=interval_format)
        return ax
