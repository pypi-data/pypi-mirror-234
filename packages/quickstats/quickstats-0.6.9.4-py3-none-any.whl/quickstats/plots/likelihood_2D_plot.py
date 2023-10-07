from typing import Dict, Optional, Union, List, Sequence

from functools import partial
from itertools import repeat

import numpy as np
import pandas as pd

from quickstats.plots import AbstractPlot
from quickstats.plots.template import create_transform
from quickstats.utils.common_utils import combine_dict
from quickstats.utils.string_utils import remove_neg_zero
from quickstats.maths.interpolation import get_regular_meshgrid
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon, Rectangle


class Likelihood2DPlot(AbstractPlot):

    CONFIG = {
        # intervals to include in the plot
        "interval_formats": {
            "68_95"               : ('0.68', '0.95'),
            "one_two_sigma"       : ('1sigma', '2sigma'),
            "68_95_99"            : ('0.68', '0.95', '0.99'),
            "one_two_three_sigma" : ('1sigma', '2sigma', '3sigma')
        },
        'highlight_styles': {
            'linewidth': 0,
            'marker': '*',
            'markersize': 20,
            'color': '#E9F1DF',
            'markeredgecolor': 'black'
        },
        'bestfit_styles':{
            'marker': 'P',
            'linewidth': 0,
            'markersize': 15
        },
        'contour_styles': {
            'linestyles': 'solid',
            'linewidths': 3            
        },
        'contourf_styles': {
            'alpha': 0.5,
            'zorder': 0            
        },
        'fill_contour': False,
        'legend_label': '{sigma_label}',
        'bestfit_label': 'Best fit ({x:.2f}, {y:.2f})',
        'polygon_label': "Nan NLL region",
        'cmap': 'GnBu',
        'interpolation': 'cubic',
        'num_grid_points': 500,
        'alphashape_alpha': 2,
        'polygon_styles': {
            'fill': True,
            'hatch': '/',
            'alpha': 0.5,
            'color': 'gray'
        }
    }
    
    # qmu from https://pdg.lbl.gov/2018/reviews/rpp2018-rev-statistics.pdf#page=31
    coverage_proba_data = {
        '0.68': {
            'qmu': 2.30,
            'label': '68% CL',
            'color': "hh:darkblue"
        },
        '1sigma': {  
            'qmu': 2.30, # 68.2%
            'label': '1 $\sigma$',
            'color': "hh:darkblue"
        },
        '0.90': {
            'qmu': 4.61,
            'label': '90% CL',
            'color': "#36b1bf"
        },
        '0.95': {
            'qmu': 5.99,
            'label': '95% CL',
            'color': "#F2385A"
        },
        '2sigma': {
            'qmu': 6.18, # 95.45%
            'label': '2 $\sigma$',
            'color': "#F2385A"
        },
        '0.99': {
            'qmu': 9.21,
            'label': '99% CL',
            'color': "#FDC536"
        },
        '3sigma': {
            'qmu': 11.83, # 99.73%
            'label': '3 $\sigma$',
            'color': "#FDC536"
        }
    }

    def __init__(self, data_map: Union[pd.DataFrame, Dict[str, pd.DataFrame]],
                 label_map: Optional[Dict] = None,
                 styles: Optional[Union[Dict, str]] = None,
                 analysis_label_options: Optional[Dict] = None,
                 config: Optional[Dict] = None,
                 config_map: Optional[Dict] = None):

        self.data_map = data_map
        self.label_map = label_map
        self.config_map = combine_dict(config_map)
        self.highlight_data = []

        super().__init__(styles=styles,
                         analysis_label_options=analysis_label_options,
                         config=config)
        
    def get_sigma_levels(self, interval_format:str="one_two_three_sigma"):
        if interval_format not in self.config['interval_formats']:
            choices = ','.join([f'"{choice}"' for choice in self.config['interval_formats']])
            raise ValueError(f'undefined sigma interval format: {interval_format} (choose from {choices})')
        sigma_levels = self.config['interval_formats'][interval_format]
        return sigma_levels

    def get_nan_shapes(self, data: pd.DataFrame,
                       xattrib: str, yattrib: str,
                       zattrib: str = 'qmu'):
        df_nan = data[np.isnan(data[zattrib])]
        xy = df_nan[[xattrib, yattrib]].values
        import alphashape
        shape = alphashape.alphashape(xy, alpha=self.config['alphashape_alpha'])
        if hasattr(shape, 'geoms'):
            shapes = [s for s in shape.geoms]
        else:
            shapes = [shape]
        return shapes
    
    def draw_shades(self, ax, shapes):
        if len(shapes) == 0:
            return None
        for shape in shapes:
            x, y = shape.exterior.coords.xy
            xy = np.column_stack((np.array(x).ravel(), np.array(y).ravel()))
            polygon = Polygon(xy, **self.config['polygon_styles'],
                              label=self.config['polygon_label'])
            ax.add_patch(polygon)
            if 'shade' not in self.legend_data:
                self.update_legend_handles({f'shade': polygon})
                self.legend_order.append(f'shade')

    def draw_single_data(self, ax, data: pd.DataFrame,
                         xattrib: str, yattrib: str,
                         zattrib: str = 'qmu',
                         config: Optional[Dict] = None,
                         clabel_size=None, draw_colormesh=False,
                         interval_format:str="one_two_three_sigma",
                         remove_nan_points_within_distance:Optional[float]=None,
                         shade_nan_points:bool=False):
        if config is None:
            config = self.config
        sigma_levels = self.get_sigma_levels(interval_format=interval_format)
        sigma_values = [self.coverage_proba_data[level]['qmu'] for level in sigma_levels]
        sigma_labels = [self.coverage_proba_data[level]['label'] for level in sigma_levels]
        sigma_colors = [self.coverage_proba_data[level]['color'] for level in sigma_levels]

        interpolate_method = config.get('interpolation', None)
        if interpolate_method is not None:
            from scipy import interpolate
            x, y, z = data[xattrib], data[yattrib], data[zattrib]
            mask = ~np.isnan(z)
            x, y, z = x[mask], y[mask], z[mask]
            n = config.get('num_grid_points', 500)
            X, Y = get_regular_meshgrid(x, y, n=n)
            Z = interpolate.griddata(np.stack((x, y), axis=1), z, (X, Y), interpolate_method)
        else:
            X_unique = np.sort(data[xattrib].unique())
            Y_unique = np.sort(data[yattrib].unique())
            X, Y = np.meshgrid(X_unique, Y_unique)
            Z = (data.pivot_table(index=xattrib, columns=yattrib, values=zattrib).T.values
                 - data[zattrib].min())
            
        if (remove_nan_points_within_distance is not None) or (shade_nan_points):
            nan_shapes = self.get_nan_shapes(data, xattrib, yattrib, zattrib)
        else:
            nan_shapes = None
        if (remove_nan_points_within_distance is not None) and (len(nan_shapes) > 0):
            if len(nan_shapes) > 0:
                from shapely import Point
                XY = np.column_stack((X.ravel(), Y.ravel()))
                d = remove_nan_points_within_distance
                for shape in nan_shapes:
                    x_ext, y_ext = shape.exterior.coords.xy
                    min_x_cutoff, max_x_cutoff = np.min(x_ext) - d, np.max(x_ext) + d
                    min_y_cutoff, max_y_cutoff = np.min(y_ext) - d, np.max(y_ext) + d
                    # only focus on points within the largest box formed by the convex hull + distance
                    box_mask = (((XY[:, 0] > min_x_cutoff) & (XY[:, 0] < max_x_cutoff)) & 
                                ((XY[:, 1] > min_y_cutoff) & (XY[:, 1] < max_y_cutoff)))
                    mask = np.full(box_mask.shape, False)
                    XY_box = XY[box_mask]
                    # remove points inside the polygon
                    mask_int = np.array([shape.contains(Point(xy)) for xy in XY_box])
                    XY_box_ext = XY_box[~mask_int]
                    # remove points within distance d of the polygon
                    mask_int_d = np.array([shape.exterior.distance(Point(xy)) < d for xy in XY_box_ext])
                    slice_int = np.arange(mask.shape[0])[box_mask][mask_int]
                    slice_int_d = np.arange(mask.shape[0])[box_mask][~mask_int][mask_int_d]
                    mask[slice_int] = True
                    mask[slice_int_d] = True
                    Z[mask.reshape(Z.shape)] = np.nan
        if draw_colormesh:
            cmap = config['cmap']
            im = ax.pcolormesh(X, Y, Z, cmap=cmap, shading='auto')
            import matplotlib.pyplot as plt
            self.cbar = plt.colorbar(im, ax=ax, **config['colorbar'])
            self.cbar.set_label(**config['colorbar_label'])
        fill_contour = config['fill_contour']
        if fill_contour:
            contour_func = ax.contourf
            contour_styles = combine_dict(self.styles['contourf'], config['contourf_styles'])
            if sigma_values:
                sigma_values = [-np.inf] + sigma_values
        else:
            contour_func = ax.contour
            contour_styles = combine_dict(self.styles['contour'], config['contour_styles'])
        if sigma_values:
            if 'colors' not in contour_styles:
                cp = contour_func(X, Y, Z, levels=sigma_values, colors=sigma_colors,
                                **contour_styles)
            else:
                cp = contour_func(X, Y, Z, levels=sigma_values, **contour_styles)
            if clabel_size is not None:
                ax.clabel(cp, inline=True, fontsize=clabel_size)
        leg_contour_styles = self._get_contour_styles(contour_styles)
        labels = [config['legend_label'].format(sigma_label=sigma_label) for sigma_label in sigma_labels]
        def handle_kwargs(color, styles, cls):
            kwargs = combine_dict(styles)
            if 'color' not in kwargs:
                kwargs['color'] = color
            if cls == Rectangle:
                kwargs['facecolor'] = kwargs.pop('color')
            return kwargs
        if fill_contour:
            handle_func = partial(Rectangle, (0, 0), 1, 1)
        else:
            handle_func = partial(Line2D, [0], [0])
        custom_handles = [handle_func(label=label, **handle_kwargs(color, styles, handle_func.func))
                          for color, label, styles in
                          zip(sigma_colors, labels, leg_contour_styles)]
        self.update_legend_handles(dict(zip(labels, custom_handles)))
        self.legend_order.extend(labels)
        
        if shade_nan_points and (len(nan_shapes) > 0):
            self.draw_shades(ax, nan_shapes)
            
        return custom_handles
    
    def _get_contour_styles(self, styles:Dict):
        style_key_map = {
            'linestyles': 'linestyle',
            'linewidths': 'linewidth',
            'colors'    : 'color',
            'alpha'     : 'alpha'
        }
        new_styles = {new_name: styles[old_name] for old_name, new_name \
                      in style_key_map.items() if old_name in styles}
        sizes = []
        for style in new_styles.values():
            if (isinstance(style, Sequence)) and (not isinstance(style, str)):
                sizes.append(len(style))
            else:
                sizes.append(1)
        if not sizes:
            return repeat({})
        sizes_not_one = [size for size in sizes if size != 1]
        if len(np.unique(sizes_not_one)) > 1:
            raise ValueError('contour styles have inconsistent sizes')
        size = np.max(sizes)
        if size == 1:
            return repeat(new_styles)
        list_styles = []
        for i in range(size):
            styles_i = {key: value if sizes[j] == 1 else value[i]
                        for j, (key, value) in enumerate(new_styles.items())}
            list_styles.append(styles_i)
        return list_styles
    
    def is_single_data(self):
        return (None in self.data_map) and (len(self.data_map) == 1)    
    
    def resolve_target_configs(self, config_map:Optional[Dict]=None,
                               targets:Optional[List[str]]=None):
        if targets is None:
            targets = [None] if self.is_single_data else list(self.data_map)
        if config_map is None:
            config_map = {}
        target_configs = {}
        for target in targets:
            if target is None:
                target_configs[target] = combine_dict(self.config)
            else:
                target_configs[target] = combine_dict(self.config, config_map.get(target))
        return target_configs                

    def draw(self, xattrib:str, yattrib:str, zattrib:str='qmu',
             targets:Optional[List[str]]=None,
             xlabel: Optional[str] = "", ylabel: Optional[str] = "",
             zlabel: Optional[str] = "$-2\Delta ln(L)$",
             ymax:Optional[float]=None, ymin:Optional[float]=None,
             xmin:Optional[float]=None, xmax:Optional[float]=None,
             clabel_size=None, draw_sm_line: bool = False,
             draw_bestfit:Union[List[str], bool]=True,
             draw_colormesh=False, draw_legend=True,
             interval_format:str="one_two_three_sigma",
             remove_nan_points_within_distance:Optional[float]=None,
             shade_nan_points:bool=False):
        
        self.reset_legend_data()
        ax = self.draw_frame()
        
        target_configs = self.resolve_target_configs(self.config_map, targets=targets)
        highlight_index = 0
        for target, config in target_configs.items():
            if (target is None):
                data = self.data_map
            else:
                if target not in self.data_map:
                    raise RuntimeError(f'no input data for the target "{target}" is found')
                data = self.data_map[target]
                
            self.draw_single_data(ax, data, xattrib=xattrib, yattrib=yattrib,
                                  zattrib=zattrib, config=config,
                                  clabel_size=clabel_size, draw_colormesh=draw_colormesh,
                                  interval_format=interval_format,
                                  remove_nan_points_within_distance=remove_nan_points_within_distance,
                                  shade_nan_points=shade_nan_points)
            if ((draw_bestfit is True) or
                (isinstance(draw_bestfit, (list, tuple)) and target in draw_bestfit)):
                valid_data = data.query(f'{zattrib} >= 0')
                bestfit_idx = np.argmin(valid_data[zattrib].values)
                bestfit_x   = valid_data.iloc[bestfit_idx][xattrib]
                bestfit_y   = valid_data.iloc[bestfit_idx][yattrib]
                label = remove_neg_zero(config["bestfit_label"].format(x=bestfit_x, y=bestfit_y))
                self.draw_highlight(ax, bestfit_x, bestfit_y, label=label,
                                    styles=config['bestfit_styles'],
                                    index=highlight_index)
                highlight_index += 1
        
        if self.highlight_data is not None:
            for i, options in enumerate(self.highlight_data):
                self.draw_highlight(ax, **options,
                                    index=highlight_index + i)

        if draw_sm_line:
            sm_x, sm_y = self.config['sm_values']
            transform = create_transform(transform_x="data", transform_y="axis")
            ax.vlines(sm_x, ymin=0, ymax=1, zorder=0, transform=transform,
                      **sm_line_styles)
            transform = create_transform(transform_x="axis", transform_y="data")
            ax.hlines(sm_y, xmin=0, xmax=1, zorder=0, transform=transform,
                      **self.config['sm_line_styles'])

        if draw_legend:
            handles, labels = self.get_legend_handles_labels()
            ax.legend(handles, labels, **self.styles['legend'])

        self.draw_axis_components(ax, xlabel=xlabel, ylabel=ylabel)
        self.set_axis_range(ax, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)

        return ax

    def draw_highlight(self, ax, x, y, label:str,
                       styles:Optional[Dict]=None,
                       index:int=0):
        if styles is None:
            styles = self.config['highlight_styles']
        handle = ax.plot(x, y, label=label, **styles)
        self.update_legend_handles({f'highlight_{index}': handle[0]})
        self.legend_order.append(f'highlight_{index}')

    def add_highlight(self, x: float, y: float, label: str = "SM prediction",
                      styles: Optional[Dict] = None):
        highlight_data = {
            'x': x,
            'y': y,
            'label': label,
            'styles': styles
        }
        self.highlight_data.append(highlight_data)
