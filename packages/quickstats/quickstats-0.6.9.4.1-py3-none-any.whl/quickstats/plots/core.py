from typing import List, Dict, Optional, Union
from cycler import cycler

import numpy as np

from quickstats import DescriptiveEnum

class ErrorDisplayFormat(DescriptiveEnum):
    ERRORBAR = (0, "Error bar", "errorbar")
    FILL     = (1, "Fill interpolated error range across bins", "fill_between")
    SHADE    = (2, "Shade error range in each bin", "bar")
    
    def __new__(cls, value:int, description:str="", mpl_method:str=""):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.description = description
        obj.mpl_method = mpl_method
        return obj
    
class PlotFormat(DescriptiveEnum):
    ERRORBAR = (0, "Error bar", "errorbar")
    HIST     = (1, "Histogram", "hist")
                
    def __new__(cls, value:int, description:str="", mpl_method:str=""):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.description = description
        obj.mpl_method = mpl_method
        return obj

def set_attrib(obj, **kwargs):
    for key, value in kwargs.items():
        target = obj
        if '.' in key:
            tokens = key.split('.')
            if len(tokens) != 2:
                raise ValueError('maximum of 1 subfield is allowed but {} is given'.format(len(tokens)-1))
            field, key = tokens[0], tokens[1]
            method_name = 'Get' + field
            if hasattr(obj, 'Get' + field):
                target = getattr(obj, method_name)()
            else:
                raise ValueError('{} object does not contain the method {}'.format(type(target), method_name)) 
        method_name = 'Set' + key
        if hasattr(target, 'Set' + key):
            method_name = 'Set' + key
        elif hasattr(target, key):
            method_name = key
        else:
            raise ValueError('{} object does not contain the method {}'.format(type(target), method_name))         
        if value is None:
            getattr(target, method_name)()
        elif isinstance(value, (list, tuple)):
            getattr(target, method_name)(*value)
        else:
            getattr(target, method_name)(value)
    return obj


# taken from https://matplotlib.org/stable/tutorials/colors/colormaps.html
def plot_color_gradients(cmap_list:List[str], size:Optional[int]=None):
    """
    Parameters
    ----------
    cmap_list : list of str
        List of color map names.
    size: int or None, default: None
        The colormap will be resampled to have size entries in the lookup table.
    """
    import matplotlib.pyplot as plt
    from matplotlib.cm import get_cmap
    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))    
    # Create figure and adjust figure height to number of colormaps
    nrows = len(cmap_list)
    figh = 0.35 + 0.15 + (nrows + (nrows - 1) * 0.1) * 0.22
    fig, axs = plt.subplots(nrows=nrows + 1, figsize=(6.4, figh))
    fig.subplots_adjust(top=1 - 0.35 / figh, bottom=0.15 / figh,
                        left=0.2, right=0.99)

    for ax, name in zip(axs, cmap_list):
        ax.imshow(gradient, aspect='auto', cmap=get_cmap(name, size))
        ax.text(-0.01, 0.5, name, va='center', ha='right', fontsize=10,
                transform=ax.transAxes)

    # Turn off *all* ticks & spines, not just the ones with colormaps.
    for ax in axs:
        ax.set_axis_off()
        
def register_cmaps(listed_colors:Dict[str, List[str]]):
    """
    Parameters
    ----------
    listed_colors : dictionary of list of str
        A map from cmap name to the underlying list of colors
    """
    from matplotlib.colors import ListedColormap
    from matplotlib.cm import register_cmap
    for name, colors in listed_colors.items():
        cmap = ListedColormap(colors, name=name)
        register_cmap(name=name, cmap=cmap, override_builtin=True)
        
def get_cmap(source:Optional[Union[List, str]], name:Optional[str]="from_list", size:Optional[int]=None, resample:bool=True):
    from matplotlib.colors import ListedColormap, LinearSegmentedColormap
    if isinstance(source, str):
        from matplotlib.cm import get_cmap as gcm
        cmap = gcm(source)
        return get_cmap(cmap, size=size, resample=resample)
    elif isinstance(source, (ListedColormap, LinearSegmentedColormap)):
        if size is None:
            return source.copy()
        if resample or (size >= source.N):
            return source.resampled(size)
        else:
            cmap_rgba = source(range(source.N))[:size]
            return get_cmap(cmap_rgba, name=source.name)
    else:
        return ListedColormap(source, name=name, N=size)
    
def get_cmap_rgba(source:Optional[Union[List, str]], size:Optional[int]=None, resample:bool=True):
    cmap = get_cmap(source, size=size, resample=resample)
    N = cmap.N
    return cmap(range(N))
    
def get_color_cycle(source:Optional[Union[List, str, "ListedColorMap"]]="default"):
    from matplotlib.colors import ListedColormap
    if isinstance(source, str):
        cmap = get_cmap(source)
        return get_color_cycle(cmap)
    elif isinstance(source, ListedColormap):
        colors = source.colors
        return get_color_cycle(colors)
    return (cycler(color=source))
    