from typing import Optional, Union, Dict, List, Tuple
import os
import sys
import copy
import fnmatch
import time
import json
import inspect
import datetime
import functools
import collections.abc

import numpy as np

from .string_utils import split_str, parse_as_dict

def timely_info(green_text, normal_text, adjust=40):
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '\033[92m[INFO]\033[0m', '\033[92m{}\033[0m'.format(green_text).rjust(40, ' '), normal_text)

def get_cpu_count():
    return os.cpu_count()

def parallel_run(func, *iterables, max_workers):
    from concurrent.futures  import ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers) as executor:
        results = []
        for result in executor.map(func, *iterables):
            results.append(result)
    return results

def execute_multi_tasks(func, *iterables, parallel):
    if parallel == 0:
        result = []
        for args in zip(*iterables):
            result.append(func(*args))
        return result
    else:
        if parallel == -1:
            max_workers = get_cpu_count()
        else:
            max_workers = parallel
        return parallel_run(func, *iterables, max_workers=max_workers)

def stdout_print(msg):
    sys.__stdout__.write(msg + '\n')
    
def redirect_stdout(logfile_path):
    import ROOT
    sys.stdout = open(logfile_path, 'w')
    ROOT.gSystem.RedirectOutput(logfile_path)

def restore_stdout():
    import ROOT
    if sys.stdout != sys.__stdout__:
        sys.stdout.close()
    sys.stdout = sys.__stdout__
    ROOT.gROOT.ProcessLine('gSystem->RedirectOutput(0);')

def redirect_stdout_test(func):
    """Redirect stdout to a log file"""
    import ROOT
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        logfile_path = kwargs.get('logfile_path', None)
        if logfile_path is not None:
            sys.stdout = open(logfile_path, 'w')
            ROOT.gSystem.RedirectOutput(logfile_path)
            value = func(*args, **kwargs)
            sys.stdout.close()
            sys.stdout = sys.__stdout__
            ROOT.gROOT.ProcessLine('gSystem->RedirectOutput(0);')
            return value
        else:
            return func(*args, **kwargs)
    return wrapper_timer

def json_load(fp, *args, **kwargs):
    try:
        data = json.load(fp, *args, **kwargs)
    except:
        raise RuntimeError(f"broken json input: {fp}")
    return data

def parse_config(source:Optional[Union[Dict, str]]=None):
    if source is None:
        return {}
    elif isinstance(source, str):
        with open(source, 'r') as f:
                config = json.load(f)
        return config
    elif isinstance(source, dict):
        return source
    else:
        raise ValueError("invalid config input")
        
class NpEncoder(json.JSONEncoder):
    """
    Custom JSON Encoder for handling NumPy data types in JSON serialization.

    This custom JSONEncoder subclass is designed to handle NumPy data types 
    (such as np.integer, np.floating, and np.ndarray) during JSON serialization. 
    
    Note:
        To use this custom encoder, you can pass it as the 'cls' argument when 
        calling the json.dumps() function or json.dump() method.

    Example:
        import json
        import numpy as np

        # Create a dictionary with NumPy data types
        data = {
            'integer': np.int64(42),
            'floating': np.float64(3.14),
            'array': np.array([1, 2, 3])
        }

        # Serialize the dictionary using the NpEncoder
        json_string = json.dumps(data, cls=NpEncoder)

        # Deserialize the JSON string
        decoded_data = json.loads(json_string)

        # The NumPy data types are now properly serialized and deserialized
        print(decoded_data['integer'])  # outputs: 42
        print(decoded_data['floating'])  # outputs: 3.14
        print(decoded_data['array'])  # outputs: [1, 2, 3]
    """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

    
def update_nested_dict(d: Dict, u: Dict) -> Dict:
    """
    Recursively updates nested dictionaries.

    Parameters
    ----------
    d : Dict
        The dictionary to be updated.
    u : Dict
        The dictionary containing updates.

    Returns
    -------
    Dict
        The updated dictionary.

    Notes
    -----
    If a key exists in `u` but not in `d`, the key-value pair from `u` is added to `d`.
    """
    for k, v in u.items():
        if isinstance(d.get(k, None), collections.Mapping) and isinstance(v, collections.Mapping):
            d[k] = update_nested_dict(d.get(k, {}), v)
        else:
            d[k] = v
    return d

def combine_dict(d: Optional[Dict] = None, u: Optional[Dict] = None) -> Dict:
    """
    Creates a deep copy of two dictionaries and combines their contents.

    Parameters
    ----------
    d : Dict, optional
        The primary dictionary. Default is None.
    u : Dict, optional
        The dictionary containing updates. If `None`, the function returns a 
        deep copy of `d`. Default is None.

    Returns
    -------
    Dict
        The combined dictionary.
    """
    d_copy = copy.deepcopy(d) if d is not None else {}
    if u is None:
        return d_copy

    u_copy = copy.deepcopy(u)
    return update_nested_dict(d_copy, u_copy)
    
def str_list_filter(source:List[str], patterns:List[str], inclusive:bool=True):
    if inclusive:
        result = [s for p in patterns for s in source if fnmatch.fnmatch(s, p)]
        return sorted(list(set(result)))
    else:
        result = set(source)
        for p in patterns:
            result &= set([s for s in source if not fnmatch.fnmatch(s, p)])
        return sorted(list(result))

def get_class_that_defined_method(meth):
    if isinstance(meth, functools.partial):
        return get_class_that_defined_method(meth.func)
    if inspect.ismethod(meth) or (inspect.isbuiltin(meth) and getattr(meth, '__self__', None) is not None and getattr(meth.__self__, '__class__', None)):
        for cls in inspect.getmro(meth.__self__.__class__):
            if meth.__name__ in cls.__dict__:
                return cls
        meth = getattr(meth, '__func__', meth)  # fallback to __qualname__ parsing
    if inspect.isfunction(meth):
        cls = getattr(inspect.getmodule(meth),
                      meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0],
                      None)
        if isinstance(cls, type):
            return cls
    return getattr(meth, '__objclass__', None)

def batch_makedirs(dirnames:Union[str, List[str], Dict[str, str]]) -> None:
    """
    Create multiple directories in a batch. 

    This function accepts a single directory name as a string, a list of directory 
    names, or a dictionary where the values are directory names. It then creates 
    these directories if they do not already exist.

    Parameters
    ----------
    dirnames : Union[str, List[str], Dict[str, str]]
        The directory name(s) to be created. 
        - If it's a string, a single directory will be created.
        - If it's a list, each element is treated as a directory name.
        - If it's a dictionary, each value is treated as a directory name.

    Raises
    ------
    ValueError
        If `dirnames` is not a string, a list, or a dictionary.

    Examples
    --------
    >>> batch_makedirs('new_dir')
    >>> batch_makedirs(['new_dir1', 'new_dir2'])
    >>> batch_makedirs({'dir1': 'new_dir1', 'dir2': 'new_dir2'})
    """
    if isinstance(dirnames, str):
        dirnames = [dirnames]
    elif isinstance(dirnames, dict):
        dirnames = list(dirnames.values())

    if isinstance(dirnames, list):
        for dirname in dirnames:
            abs_dirname = os.path.abspath(dirname)
            os.makedirs(abs_dirname, exist_ok=True)
    else:
        raise ValueError('invalid format for "dirnames"')

def set_scripts_path(scripts_path, undo=False):
    if (scripts_path in sys.path) and (undo==True):
        sys.path.remove(scripts_path)
        os.environ["PYTHONPATH"].replace(scripts_path+":","")
        
    if (scripts_path not in sys.path) and (undo==False):
        sys.path.insert(0, scripts_path)
        os.environ["PYTHONPATH"] = scripts_path + ":" + os.environ.get("PYTHONPATH", "")
        
def is_valid_file(filename:str):
    if not filename:
        return False
    if not os.path.exists(filename):
        return False
    ext = os.path.splitext(filename)[-1]
    if ext == ".root":
        from quickstats.utils.root_utils import is_corrupt
        return not is_corrupt(filename)
    return (os.path.isfile(filename)) and (os.path.getsize(filename) > 0)

def remove_list_duplicates(seq:List, keep_order:bool=True):
    if keep_order:
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]
    else:
        return list(set(seq))
    
def format_delimiter_enclosed_text(text:str, delimiter:str, width:int=10, indent_str:str="\t",
                                   upper_margin:int=1, lower_margin:int=1):
    full_line_width = 2 * width + ( len(text) if (len(text) > 2 * width) else (2 * width) ) + 2
    full_line = delimiter * full_line_width
    line = delimiter * width
    result = "\n"*upper_margin + f"{indent_str} {full_line}\n"
    if len(text) > 2 * width:
        result += f"{indent_str} {line} {text} {line}\n"
    else:
        result += f"{indent_str} {line}{text.center(2*width+2)}{line}\n"
    result += f"{indent_str} {full_line}" + "\n"*lower_margin
    return result

def insert_periodic_substr(s:str, every:int=64, substr:str='\n'):
    return substr.join(s[i:i+every] for i in range(0, len(s), every))
        
def format_display_string(s:str, indent:str="", linebreak:int=80, skipfirst:bool=False):
    if len(indent) >= linebreak:
        raise RuntimeError("size of indentation is greater linebreak")
    substr = "\n" + indent
    every = linebreak - len(indent)
    ss = insert_periodic_substr(s, every, substr)
    if not skipfirst:
        return indent + ss
    return ss

def itemize_dict(d:Dict, separator:str=": ", leftmargin:int=0, linebreak:int=100):
    max_key_size = max([len(k) for k in d.keys()])
    bullet_size = max_key_size + len(separator)
    indent_size = leftmargin + bullet_size
    text_size = linebreak - indent_size
    if text_size <= 0:
        raise RuntimeError("size of indentation is greater linebreak")
    texts = []
    substr = "\n" + " " * indent_size
    for k, v in d.items():
        v = v.replace("\n", "")
        text = "{0:>{1}}".format(k + separator, indent_size) + insert_periodic_substr(v, text_size, substr)
        texts.append(text)
    return "\n".join(texts) + "\n"

def filter_by_wildcards(targets: List[str], conditions: Optional[Union[str, List[str]]] = None, exclusion: bool = False) -> List[str]:
    """
    Filters a list of string targets based on wildcard conditions.

    This method filters a list of targets based on provided wildcard patterns.
    It can either return targets that match the conditions or exclude them.

    Parameters
    ----------
    targets : List[str]
        A list of string targets to be filtered.
    conditions : Union[str, List[str]], optional
        Wildcard patterns used for filtering. If a string is provided,
        it is split by commas into individual conditions.
    exclusion : bool
        If True, the method returns targets that do not match the 
        conditions. If False, it returns targets that match the conditions.
        Defaults to False.

    Returns
    -------
    List[str]
        A filtered list of string targets based on the provided conditions.

    Examples
    --------
    >>> filter_by_wildcards(['apple', 'banana', 'cherry'], 'a*')
    ['apple']

    >>> filter_by_wildcards(['apple', 'banana', 'cherry'], 'a*', exclusion=True)
    ['banana', 'cherry']

    >>> filter_by_wildcards(['apple', 'banana', 'cherry'], ['a*', '*rr*'])
    ['apple', 'cherry']

    """
    if not conditions:
        return targets

    if isinstance(conditions, str):
        conditions = conditions.split(',')
    
    if exclusion:
        return [target for target in targets if not any(fnmatch.fnmatch(target, condition) for condition in conditions)]
    
    return [target for target in targets if any(fnmatch.fnmatch(target, condition) for condition in conditions)]

def set_unlimited_stacksize():
    import resource
    resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
    
def in_notebook() -> bool:
    try:
        from IPython import get_ipython
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except ImportError:
        return False
    except AttributeError:
        return False
    except NameError:
        return False      # Probably standard Python interpreter    
    return True

def reindex_dataframe(df, index_values:Union[Tuple[List], List],
                      index_levels:Optional[Union[Tuple[str], Tuple[int], str, int]]=None):
    if not isinstance(index_values, tuple):
        index_values = tuple([index_values])
    if index_levels is None:
        index_levels = tuple(range(len(index_values)))
    if isinstance(index_levels, (str, int)):
        index_levels = (index_levels,)
    for values, level in zip(index_values, index_levels):
        mask = np.in1d(values, df.index.get_level_values(level))
        df = df.reindex(np.array(values)[mask], level=level)
    return df

def filter_dataframe_by_index_values(df, index_values:Union[Tuple[List], List],
                                     index_levels:Optional[Union[Tuple[str], Tuple[int], str, int]]=None):
    if not isinstance(index_values, tuple):
        index_values = tuple([index_values])
    if index_levels is None:
        index_levels = tuple(range(len(index_values)))
    if isinstance(index_levels, (int, str)):
        index_levels = (index_levels,)
    for values, level in zip(index_values, index_levels):
        df = df.loc[df.index.get_level_values(level).isin(values)]
    return df

def parse_config_dict(expr:Optional[Union[str, Dict]]=None):
    if expr is None:
        return {}
    if isinstance(expr, str):
        return parse_as_dict(expr)
    if isinstance(expr, dict):
        return expr
    raise ValueError(f'expr of type "{type(expr)}" is not convertible to a config dict')

def update_config_dict(orig_dict, new_dict, allow_overlap_keys:bool=True):
    orig_dict = parse_config_dict(orig_dict)
    new_dict = parse_config_dict(new_dict)
    if not allow_overlap_keys:
        overlap_keys = list(set(orig_dict.keys()) & set(new_dict.keys()))
        if overlap_keys:
            raise RuntimeError(f'found overlap keys between two config dict: {", ".join(overlap_keys)}')
    return combine_dict(orig_dict, new_dict)

def list_of_dict_to_dict_of_list(source:List[Dict], use_first_keys:bool=True):
    if use_first_keys:
        return {k: [item[k] for item in source] for k in source[0]}
    common_keys = set.intersection(*map(set, source))
    return {k: [item[k] for item in source] for k in common_keys}

def dict_of_list_to_list_of_dict(source:Dict[str, List]):
    return [dict(zip(source, t)) for t in zip(*source.values())]

def save_as_json(data:Dict, outname:str,
                 indent:int=2, truncate:bool=True):
    with open(outname, "w") as file:
        json.dump(data, file, indent=2)
        if truncate:
            file.truncate()