from typing import Optional, Union, Dict, List, Sequence

import pandas as pd
import numpy as np

from matplotlib import colors
from matplotlib.ticker import MaxNLocator
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon

from quickstats.plots import AbstractPlot, get_color_cycle
from quickstats.plots.template import ratio_frames, centralize_axis, remake_handles
from quickstats.utils.common_utils import combine_dict
from quickstats.maths.numerics import safe_div
from quickstats.maths.statistics import (HistComparisonMode,
                                         min_max_to_range, get_hist_data,
                                         get_stacked_hist_data,
                                         get_hist_comparison_data,
                                         get_clipped_data)

from .core import PlotFormat, ErrorDisplayFormat

class VariableDistributionPlot(AbstractPlot):
    
    COLOR_CYCLE = "simple_contrast"
    
    STYLES = {
        "legend": {
            "handletextpad": 0.3
        },
        "hist": {
            'histtype' : 'step',
            'linestyle': '-',
            'linewidth': 2
        },
        "bar": {
            'linewidth' : 0,
            'alpha'     : 0.5
        },
        "fill_between": {
            'alpha' : 0.5
        },
        'errorbar': {
            "marker": 'o',
            "markersize": None,
            'linestyle': 'none',
            "linewidth": 0,
            "elinewidth": 2,
            "capsize": 0,
            "capthick": 0
        },        
    }
    
    CONFIG = {
        'ratio_line_styles':{
            'color': 'gray',
            'linestyle': '--',
            'zorder': 0
        },
        'plot_format': 'hist',
        'error_format': 'shade',
        'error_label_format': r'{label} $\pm \sigma$',
        'show_xerr': False,
        'stacked_label': ':stacked_{index}:',
        'box_legend_handle': False,
        'save_hist_data': False
    }
    
    def __init__(self, data_map:Union["pandas.DataFrame", Dict[str, "pandas.DataFrame"]],
                 plot_options:Optional[Dict]=None,
                 label_map:Optional[Dict]=None,
                 color_cycle:Optional[Union[List, str, "ListedColorMap"]]='simple_contrast',
                 styles:Optional[Union[Dict, str]]=None,
                 comparison_styles:Optional[Union[Dict, str]]=None,
                 analysis_label_options:Optional[Dict]=None,
                 config:Optional[Dict]=None,
                 verbosity:Optional[Union[int, str]]='INFO'):
        """
            Parameters
            ----------------------------------------------------------------------------
            data_map: pandas.DataFrame or dictionary of pandas.DataFrame
                Input dataframe(s). If a dictionary is given, it should be of the form
                {<sample_name>: <pandas.DataFrame>}
            plot_options: dicionary
                A dictionary containing the plot options for various group of samples.
                It should be of the form
                { <sample_group>:
                  {
                    "samples": <list of sample names>,
                    "weight_scale": <scale factor>,
                    "styles" : <options in mpl.hist or mpl.errorbar>,
                    "error_styles": <options in mpl.bar>,
                    "plot_format": "hist" or "errorbar",
                    "show_error": True or False,
                    "stack_index": <stack index>
                  }
                }
                where "styles" should match the options available in mpl.hist if
                `plot_format` = "hist" or mpl.errorbar if `plot_format` = "errorbar"
                
                (optional) "weight_scale" is used to scale the weights of the given
                group of samples by the given factor
                
                "error_styles" should match the options available in mpl.errorbar if
                `error_format` = "errorbar", mpl.bar if `error_format` = "shade" or
                mpl.fill_between if `error_format` = "fill"
                
                (optional) "show_error" is used to specify whether to show the errorbar/
                errorbands for this particular target.
                
                (optional) "stack_index" is be used when multiple stacked plots are made;
                sample groups with the same stack index will be stacked; this option
                is only used when `plot_format` = "hist" and the draw method is called
                with the `stack` option set to True; by default a stack index of 0 will
                be assigned
                
                Note: If both `plot_format` and `error_format` are errorbar, "styles"
                will be used instead of "error_styles" for the error styles.
                
                
        """
        self.load_data(data_map)
        self.plot_options = plot_options
        self.label_map = label_map
        self.reset_hist_data()
        super().__init__(color_cycle=color_cycle,
                         styles=styles,
                         analysis_label_options=analysis_label_options,
                         config=config,
                         verbosity=verbosity)
    
    def load_data(self, data_map:Dict[str, pd.DataFrame]):
        if not isinstance(data_map, dict):
            data_map = {None: data_map}
        self.data_map = data_map
        
    def set_plot_format(self, plot_format:str):
        self.config['plot_format'] = PlotFormat.parse(plot_format)
        
    def set_error_format(self, error_format:str):
        self.config['error_format'] = ErrorDisplayFormat.parse(error_format)
        
    def is_single_data(self):
        return (None in self.data_map) and (len(self.data_map) == 1)
    
    def resolve_plot_options(self, plot_options:Optional[Dict]=None,
                             targets:Optional[List[str]]=None):
        if self.is_single_data():
            if targets is not None:
                raise ValueError('no targets should be specified if only a single set of input data is given')
            targets = [None]
        elif targets is None:
            if plot_options is not None:
                targets = list(plot_options.keys())
            elif isinstance(self.data_map, dict):
                targets = list(self.data_map.keys())
        final_plot_options = {}
        colors = self.get_colors()
        n_colors, color_i = len(colors), 0
        if plot_options is None:
            plot_options = {}
        if self.label_map is not None:
            label_map = self.label_map
        else:
            label_map = {}
        for target in targets:
            options = combine_dict(plot_options.get(target, {}))
            if 'plot_format' not in options:
                options['plot_format'] = PlotFormat.parse(self.config['plot_format'])
            else:
                options['plot_format'] = PlotFormat.parse(options['plot_format'])
            if 'error_format' not in options:
                if options['plot_format'] == PlotFormat.ERRORBAR:
                    options['error_format'] = ErrorDisplayFormat.ERRORBAR
                else:
                    options['error_format'] = ErrorDisplayFormat.parse(self.config['error_format'])
            else:
                options['error_format'] = ErrorDisplayFormat.parse(options['error_format'])
            # use default styles if not specified
            if 'styles' not in options:
                options['styles'] = combine_dict(self.get_styles(options['plot_format'].mpl_method))
            else:
                options['styles'] = combine_dict(self.get_styles(options['plot_format'].mpl_method), options['styles'])
            if 'color' not in options['styles']:
                if color_i == n_colors:
                    self.stdout.warning("Number of targets is more than the number of colors "
                                        "available in the color map. The colors will be repeated.")
                options['styles']['color'] = colors[color_i % n_colors]
                color_i += 1
            if 'label' not in options['styles']:
                label = label_map.get(target, target)
                if label is None:
                    label = 'None'
                options['styles']['label'] = label
            if 'samples' not in options:
                options['samples'] = [target]
            if 'error_styles' not in options:
                options['error_styles'] = combine_dict(self.get_styles(options['error_format'].mpl_method))
            else:
                options['error_styles'] = combine_dict(self.get_styles(options['error_format'].mpl_method), options['error_styles'])
            if 'color' not in options['error_styles']:
                options['error_styles']['color'] = options['styles']['color']
            if 'label' not in options['error_styles']:
                fmt = self.config['error_label_format']
                options['error_styles']['label'] = fmt.format(label=options['styles']['label'])
            if 'stack_index' not in options:
                options['stack_index'] = 0
            if 'weight_scale' not in options:
                options['weight_scale'] = None
            final_plot_options[target] = options
        return final_plot_options
    
    def resolve_comparison_options(self, comparison_options:Optional[Dict]=None,
                                   plot_options:Optional[Dict]=None):
        if comparison_options is None:
            return None
        if plot_options is None:
            plot_options = {}
        comparison_options = combine_dict(comparison_options)
        comparison_options['mode'] = HistComparisonMode.parse(comparison_options['mode'])
        colors = self.get_colors()
        n_colors, color_i = len(colors), 0
        if 'plot_format' in comparison_options:
            plot_format = PlotFormat.parse(comparison_options.pop('plot_format'))
        else:
            plot_format = PlotFormat.parse(self.config['plot_format'])
        # temporary fix because only error plot format is supported
        plot_format = PlotFormat.ERRORBAR
        if 'error_format' in comparison_options:
            error_format = ErrorDisplayFormat.parse(comparison_options.pop('error_format'))
        else:
            error_format = ErrorDisplayFormat.parse(self.config['error_format'])
        components = comparison_options['components']
        if not isinstance(components, list):
            components = [components]
        for component in components:
            reference = component['reference']
            target    = component['target']
            if 'plot_format' not in component:
                component['plot_format'] = plot_format
            if 'error_format' not in component:
                component['error_format'] = error_format
            com_plot_format = PlotFormat.parse(component['plot_format'])
            com_error_format = ErrorDisplayFormat.parse(component['error_format'])
            if 'styles' not in component:
                component['styles'] = combine_dict(self.get_styles(com_plot_format.mpl_method))
            if 'error_styles' not in component:
                component['error_styles'] = combine_dict(self.get_styles(com_error_format.mpl_method))
            if 'color' not in component['styles']:
                if target in plot_options:
                    component['styles']['color'] = plot_options[target]['styles']['color']
                else:
                    component['styles']['color'] = colors[color_i % n_colors]
                    color_i += 1
            if 'color' not in component['error_styles']:
                if target in plot_options:
                    component['error_styles']['color'] = plot_options[target]['error_styles']['color']
                else:
                    component['error_styles']['color'] = component['styles']['color']
            component['mode'] = comparison_options['mode']
        comparison_options['components'] = components
        return comparison_options

    def draw_comparison_data(self, ax, reference_data, target_data,
                             bin_edges:Optional[np.ndarray]=None,
                             mode:Union[HistComparisonMode, str]="ratio",
                             draw_error:bool=True,
                             plot_format:Union[PlotFormat, str]='errorbar',
                             error_format:Union[ErrorDisplayFormat, str]='errorbar',
                             styles:Optional[Dict]=None,
                             error_styles:Optional[Dict]=None):
        mode = HistComparisonMode.parse(mode)
        comparison_data = get_hist_comparison_data(reference_data,
                                                   target_data,
                                                   mode=mode)
        handle, error_handle = self.draw_binned_data(ax, comparison_data,
                                                     bin_edges=bin_edges,
                                                     draw_data=True,
                                                     draw_error=draw_error,
                                                     plot_format=plot_format,
                                                     error_format=error_format,
                                                     styles=styles,
                                                     error_styles=error_styles)
        # expand ylim according to data range
        y = comparison_data['y']
        ylim = list(ax.get_ylim())
        if ylim[0] > np.min(y):
            ylim[0] = np.min(y)
        if ylim[1] < np.max(y):
            ylim[1] = np.max(y)
        ax.set_ylim(ylim)

        if self.config['save_hist_data']:
            self.hist_comparison_data.append(comparison_data)
            
        return handle, error_handle
    
    def deduce_bin_range(self, samples:List[str], column_name:str,
                         variable_scale:Optional[float]=None):
        xmin = None
        xmax = None
        for sample in samples:
            df = self.data_map[sample]
            x = df[column_name].values
            if variable_scale is not None:
                x = x * variable_scale
            if xmin is None:
                xmin = np.min(x)
            else:
                xmin = min(xmin, np.min(x))
            if xmax is None:
                xmax = np.max(x)
            else:
                xmax = max(xmax, np.max(x))
        return (xmin, xmax)
    
    def get_sample_data(self, samples:List[str],
                        column_name:str,
                        variable_scale:Optional[float]=None,
                        weight_scale:Optional[float]=None,
                        weight_name:Optional[str]=None):
        df = pd.concat([self.data_map[sample] for sample in samples], ignore_index=True)
        x = df[column_name].values
        if variable_scale is not None:
            x = x * variable_scale
        if weight_name is not None:
            weights = df[weight_name]
        else:
            weights = np.ones(x.shape)
        if weight_scale is not None:
            weights = weights * weight_scale            
        return x, weights
    
    def draw_stacked(self, ax, plot_options:Dict,
                     column_name:str, weight_name:Optional[str]=None,
                     bins:Union[int, Sequence]=25,
                     bin_range:Optional[Sequence]=None,
                     clip_weight:bool=False,
                     underflow:bool=False,
                     overflow:bool=False,
                     divide_bin_width:bool=False,
                     normalize:bool=True,
                     show_error:bool=False,
                     variable_scale:Optional[float]=None):
        stacked_data = {
            'x'       : [],
            'weights' : [],
            'color'   : [],
            'label'   : [],
        }

        stacked_styles = []
        for target, options in plot_options.items():
            samples, styles = options['samples'], options['styles']
            label, color = styles['label'], styles['color']
            weight_scale = options['weight_scale']
            x, weights = self.get_sample_data(samples, column_name,
                                              variable_scale=variable_scale,
                                              weight_scale=weight_scale,
                                              weight_name=weight_name)
            x = get_clipped_data(x, bin_range=bin_range, clip_lower=underflow, clip_upper=overflow)
            stacked_data['x'].append(x)
            stacked_data['weights'].append(weights)
            stacked_data['color'].append(color)
            stacked_data['label'].append(label)
            stacked_styles.append(styles)
        bin_edges = np.histogram_bin_edges(np.concatenate(stacked_data['x']).flatten(),
                                           bins=bins, range=bin_range)
        hist_data = get_stacked_hist_data(stacked_data['x'], stacked_data['weights'],
                                          underflow=underflow,
                                          overflow=overflow,
                                          divide_bin_width=divide_bin_width,
                                          normalize=normalize,
                                          bin_range=bin_range, bins=bins,
                                          clip_weight=clip_weight,
                                          xerr=show_error and self.config['show_xerr'],
                                          yerr=show_error,
                                          error_option='auto')
        stacked_styles = {k:v for k,v in stacked_styles[0].items() if k not in ['color', 'label']}
        stacked_data_processed = get_stacked_hist_data(stacked_data['x'], stacked_data['weights'],
                                                       underflow=underflow,
                                                       overflow=overflow,
                                                       divide_bin_width=divide_bin_width,
                                                       normalize=normalize,
                                                       bin_range=bin_range, bins=bins,
                                                       clip_weight=clip_weight,
                                                       xerr=False,
                                                       yerr=False,
                                                       merge=False,
                                                       error_option='auto')
        stacked_data['x'] = stacked_data_processed['x']
        stacked_data['weights'] = stacked_data_processed['y']
        hist_y, bin_edges_, handle = ax.hist(**stacked_data,
                                             bins=bins,
                                             range=bin_range,
                                             stacked=True,
                                             **stacked_styles)
        for i, target in enumerate(plot_options):
            self.update_legend_handles({target:handle[i]})
        return bin_edges, hist_data

    def reset_hist_data(self):
        self.hist_data = {}
        self.hist_comparison_data = []
            
    def draw(self, column_name:str, weight_name:Optional[str]=None,
             targets:Optional[List[str]]=None, 
             xlabel:str="", ylabel:str="Fraction of Events / {bin_width:.2f}{unit}",
             unit:Optional[str]=None, bins:Union[int, Sequence]=25,
             bin_range:Optional[Sequence]=None, clip_weight:bool=True,
             underflow:bool=False, overflow:bool=False, divide_bin_width:bool=False,
             normalize:bool=True, show_error:bool=False, show_error_legend:bool=False,
             stacked:bool=False, xmin:Optional[float]=None, xmax:Optional[float]=None,
             ymin:Optional[float]=None, ymax:Optional[float]=None, ypad:float=0.3,
             variable_scale:Optional[float]=None, logy:bool=False,
             comparison_options:Optional[Union[Dict, List[Dict]]]=None,
             legend_order:Optional[List[str]]=None):
        """
        
        Arguments:
            column_name: string
                Name of the variable in the dataframe(s).
            weight_name: (optional) string
                If specified, weight the histogram by the "weight_name" variable
                in the dataframe.
            targets: (optional) list of str
                List of target inputs to be included in the plot. All inputs are
                included by default.
            xlabel: string, default = "Score"
                Label of x-axis.
            ylabel: string, default = "Fraction of Events / {bin_width}"
                Label of y-axis.
            boundaries: (optional) list of float
                If specified, draw score boundaries at given values.
            bins: int or sequence of scalars, default = 25
                If integer, it defines the number of equal-width bins in the given range.
                If sequence, it defines a monotonically increasing array of bin edges,
                including the rightmost edge.
            bin_range: (optional) (float, float)
                Range of histogram bins.
            clip_weight: bool, default = True
                If True, ignore data outside given range when evaluating total weight
                used in normalization.
            underflow: bool, default = False
                Include undeflow data in the first bin.
            overflow: bool, default = False
                Include overflow data in the last bin.
            divide_bin_width: bool, default = False
                Divide each bin by the bin width.
            normalize: bool, default = True
                Normalize the sum of weights to one. Weights outside the bin range will
                not be counted if ``clip_weight`` is set to false, so the sum of bin
                content could be less than one.
            show_error: bool, default = False
                Whether to display data error.
            show_error_legend: bool, default = False
                Whether to include legend for the error artists.
            xmin: (optional) float
                Minimum range of x-axis.
            xmax: (optional) float
                Maximum range of x-axis.
            ymin: (optional) float
                Minimum range of y-axis.
            ymax: (optional) float
                Maximum range of y-axis.
            ypad: float, default = 0.3
                Fraction of the y-axis that should be padded. This options will be
                ignored if ymax is set.
            variable_scale: (optional) float
                Rescale variable values by a factor.
            logy: bool, default = False
                Use log scale for y-axis.
            comparison_options: (optional) dict or list of dict
                One or multiple dictionaries containing instructions on
                making comparison plots.
            legend_order: (optional) list of str
                Order of legend labels. The same order as targets will be used by default.
        """
        plot_options = self.resolve_plot_options(self.plot_options, targets=targets)
        comparison_options = self.resolve_comparison_options(comparison_options,
                                                             plot_options)
        if legend_order is not None:
            self.legend_order = list(legend_order)
        else:
            self.legend_order = list(plot_options)
        if show_error_legend and (not stacked):
            self.legend_order.extend([f"{target}_error" for target in self.legend_order])
                
        if comparison_options is not None:
            ax, ax_ratio = self.draw_frame(ratio_frames, logy=logy,
                                           **self.styles["ratio_frames"])
        else:
            ax = self.draw_frame(logy=logy)
            
        if (bin_range is None) and isinstance(bins, (int, float)):
            relevant_samples = [sample for options in plot_options.values() \
                                for sample in options['samples']]
            bin_range = self.deduce_bin_range(relevant_samples, column_name, variable_scale=variable_scale)
            self.stdout.info(f"Using deduced bin range ({bin_range[0]:.3f}, {bin_range[1]:.3f})")

        self.reset_data()
        binned_data   = {}
        target_bin_edges = {}
        
        stacked_plot_options = {}
        if stacked:
            stack_targets = [target for target, options in plot_options.items() if \
                             options['plot_format'] == PlotFormat.HIST]
            if not stack_targets:
                raise RuntimeError('no histograms to be stacked')
            for target in stack_targets:
                options = plot_options.pop(target)
                stack_index = options['stack_index']
                if stack_index not in stacked_plot_options:
                    stacked_plot_options[stack_index] = {}
                stacked_plot_options[stack_index][target] = options
            for stack_index, stacked_plot_options_i in stacked_plot_options.items():
                bin_edges, hist_data = self.draw_stacked(ax, stacked_plot_options_i,
                                                         column_name=column_name,
                                                         weight_name=weight_name,
                                                         bins=bins, bin_range=bin_range,
                                                         underflow=underflow,
                                                         overflow=overflow,
                                                         normalize=normalize,
                                                         clip_weight=clip_weight,
                                                         divide_bin_width=divide_bin_width,
                                                         variable_scale=variable_scale)
                label = self.config['stacked_label'].format(index=stack_index)
                binned_data[label] = hist_data
                target_bin_edges[label] = bin_edges
        for target, options in plot_options.items():
            samples, styles, error_styles = options['samples'], options['styles'], options['error_styles']
            label = styles['label']
            weight_scale = options['weight_scale']
            show_this_error = options.get('show_error', show_error)
            plot_format, error_format = options['plot_format'], options['error_format']
            x, weights = self.get_sample_data(samples, column_name,
                                              variable_scale=variable_scale,
                                              weight_scale=weight_scale,
                                              weight_name=weight_name)
            bin_edges = np.histogram_bin_edges(x, bins=bins, range=bin_range)
            hist_data = get_hist_data(x, weights, underflow=underflow,
                                      overflow=overflow, normalize=normalize,
                                      divide_bin_width=divide_bin_width,
                                      bin_range=bin_range, bins=bins,
                                      clip_weight=clip_weight,
                                      xerr=show_this_error and self.config['show_xerr'],
                                      yerr=show_this_error,
                                      error_option='auto')
            binned_data[target] = hist_data
            target_bin_edges[target] = bin_edges
            if plot_format == PlotFormat.HIST:
                # draw data
                hist_y, _, handle = ax.hist(hist_data['x'], bins, range=bin_range,
                                            weights=hist_data['y'], **styles)
                assert np.allclose(hist_data['y'], hist_y)
                # draw error only
                handles = self.draw_binned_data(ax, hist_data,
                                                bin_edges=bin_edges,
                                                draw_data=False,
                                                draw_error=show_this_error,
                                                error_format=error_format,
                                                error_styles=error_styles)
                if not isinstance(handle, list):
                    handle = [handle]
                handles = tuple(list(handles) + handle)
            elif plot_format == PlotFormat.ERRORBAR:
                handles = self.draw_binned_data(ax, hist_data,
                                                bin_edges=bin_edges,
                                                styles=styles,
                                                draw_error=show_this_error,
                                                error_format=error_format,
                                                error_styles=error_styles)
            
            self.update_legend_handles({target:handles})
        # propagate bin width to ylabel if needed
        if isinstance(bins, int):
            bin_width = (bin_range[1] - bin_range[0]) / bins
            if unit is None:
                unit_str = ""
            else:
                unit_str = f" {unit}"
            ylabel = ylabel.format(bin_width=bin_width, unit=unit_str)
        
        if unit is not None:
            xlabel = f"{xlabel} [{unit}]"
        self.draw_axis_components(ax, xlabel=xlabel, ylabel=ylabel)
        self.set_axis_range(ax, xmin=xmin, xmax=xmax,
                            ymin=ymin, ymax=ymax, ypad=ypad)
                
        if not self.is_single_data():
            handles, labels = self.get_legend_handles_labels()
            box_legend_handle = self.config['box_legend_handle']
            if not box_legend_handle:
                handles = remake_handles(handles, polygon_to_line=True,
                                         line2d_styles=self.styles['legend_Line2D'])
            ax.legend(handles=handles, labels=labels, **self.styles['legend'])
        
        if comparison_options is not None:
            components = comparison_options.pop('components')
            for component in components:
                reference = component.pop('reference')
                target    = component.pop('target')
                bin_edges = target_bin_edges[target]
                self.draw_comparison_data(ax_ratio,
                                          binned_data[reference],
                                          binned_data[target],
                                          bin_edges=bin_edges,
                                          **component)
            comparison_options['xlabel'] = ax.get_xlabel()
            self.decorate_comparison_axis(ax_ratio, **comparison_options)
            ax.set(xlabel=None)
            ax.tick_params(axis="x", labelbottom=False)

        if save_hist_data:
            self.hist_data = binned_data
            
        if comparison_options is not None:
            return ax, ax_ratio
        
        return ax