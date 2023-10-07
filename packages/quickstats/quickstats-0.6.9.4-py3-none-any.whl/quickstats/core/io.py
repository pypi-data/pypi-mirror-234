import os
import sys
import time
import difflib
import logging
import traceback
import threading
from enum import Enum
from typing import Union, Optional
from functools import total_ordering
from contextlib import contextmanager

text_color_map = {
    None: '',
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'bright black': '\033[30;1m',
    'bright red': '\033[31;1m',
    'bright green': '\033[32;1m',
    'bright yellow': '\033[33;1m',
    'bright blue': '\033[34;1m',
    'bright magenta': '\033[35;1m',
    'bright cyan': '\033[36;1m',
    'bright white': '\033[37;1m',    
    'darkred': '\033[91m',
    'reset': '\033[0m',
    'okgreen': '\033[92m'
}

def get_colored_text(text: str, color: str) -> str:
    """
    Returns the text formatted with the specified color.

    Args:
        text (str): The text to be colored.
        color (str): The color to apply to the text. 

    Returns:
        str: The input text with the specified color formatting.
    """
    return f"{text_color_map[color]}{text}{text_color_map['reset']}"

def format_comparison_text(text_left:str, text_right:str,
                           equal_color=None, delete_color:str="red", insert_color:str="green"):
    codes = difflib.SequenceMatcher(a=text_left, b=text_right).get_opcodes()
    s_left  = ""
    s_right = ""
    for code in codes:
        if code[0] == "equal":
            s = get_colored_text(text_left[code[1]:code[2]], equal_color)
            s_left  += s
            s_right += s
        elif code[0] == "delete":
            s_left  += get_colored_text(text_left[code[1]:code[2]], delete_color)
        elif code[0] == "insert":
            s_right += get_colored_text(text_right[code[3]:code[4]], insert_color)
        elif code[0] == "replace":
            s_left  += get_colored_text(text_left[code[1]:code[2]], delete_color)
            s_right += get_colored_text(text_right[code[3]:code[4]], insert_color)
    return s_left, s_right

getThreads = True
getMultiprocessing = True
getProcesses = True

@total_ordering
class Verbosity(Enum):
    
    CRITICAL = (50, 'CRITICAL')
    ERROR = (40, 'ERROR')
    TIPS = (35, 'TIPS')
    WARNING = (30, 'WARNING')
    INFO = (20, 'INFO')
    DEBUG = (10, 'DEBUG')
    NOTSET = (0, 'NOTSET')
    
    def __new__(cls, value:int, levelname:str=""):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.levelname = levelname
        return obj    
    
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        elif isinstance(other, int):
            return self.value < other
        elif isinstance(other, str):
            return self.value < getattr(self, other.upper()).value
        return NotImplemented
    
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        elif isinstance(other, int):
            return self.value == other
        elif isinstance(other, str):
            return self.value == getattr(self, other.upper()).value
        return NotImplemented
        
class VerbosePrint:
    
    DEFAULT_FORMAT = '[%(levelname)s] %(message)s'
    
    DEFAULT_DATEFORMAT = '%Y-%m-%d %H:%M:%S'
    DEFAULT_MSECFORMAT = '%s.%03d'
    
    ASCTIME_SEARCH = '%(asctime)'
    
    @property
    def verbosity(self):
        return self._verbosity
    
    @verbosity.setter
    def verbosity(self, val):
        if isinstance(val, str):
            try:
                v = getattr(Verbosity, val.upper())
            except:
                raise ValueError(f"invalid verbosity level: {val}")
            self._verbosity = v
        else:
            self._verbosity = val

    def __init__(self, verbosity:Union[int, Verbosity, str]=Verbosity.INFO,
                 fmt:Optional[str]=None, name:Optional[str]='',
                 msecfmt:Optional[str]=None,
                 datefmt:Optional[str]=None):
        self.verbosity = verbosity
        self.set_format(fmt)
        self.set_timefmt(datefmt, msecfmt)
        self._name = name
        
    def tips(self, text:str='', color=None, bare:bool=False):
        self.__call__(text, Verbosity.TIPS, color=color, bare=bare)
        
    def info(self, text:str='', color=None, bare:bool=False):
        self.__call__(text, Verbosity.INFO, color=color, bare=bare)
        
    def warning(self, text:str='', color=None, bare:bool=False):
        self.__call__(text, Verbosity.WARNING, color=color, bare=bare)
        
    def error(self, text:str='', color=None, bare:bool=False):
        self.__call__(text, Verbosity.ERROR, color=color, bare=bare)
        
    def critical(self, text:str='', color=None, bare:bool=False):
        self.__call__(text, Verbosity.CRITICAL, color=color, bare=bare)

    def debug(self, text:str='', color=None, bare:bool=False):
        self.__call__(text, Verbosity.DEBUG, color=color, bare=bare)
        
    def set_format(self, fmt:Optional[str]=None):
        if fmt is None:
            fmt = self.DEFAULT_FORMAT
        self._formatter = logging.Formatter(fmt)
        
    def set_timefmt(self, datefmt:Optional[str]=None, msecfmt:Optional[str]=None):
        if datefmt is None:
            datefmt = self.DEFAULT_DATEFORMAT
        if msecfmt is None:
            msecfmt = self.DEFAULT_MSECFORMAT
        self._datefmt = datefmt
        self._msecfmt = msecfmt
        
    def format_time(self):
        _ct = time.time()
        ct = self._formatter.converter(_ct)
        s = time.strftime(self._datefmt, ct)
        if self._msecfmt:
            msecs = int((_ct - int(_ct)) * 1000) + 0.0
            s = self._msecfmt % (s, msecs)
        return s
        
    def __call__(self, text:str, verbosity:int=Verbosity.INFO,
                 color=None, bare:bool=False):
        if verbosity < self.verbosity:
            return None
        if color:
            text = f"{text_color_map[color]}{text}{text_color_map['reset']}"
        if not bare:
            if hasattr(verbosity, 'levelname'):
                levelname = verbosity.levelname
            else:
                levelname = f"Level {verbosity}"
            if self._formatter.usesTime():
                asctime = self.format_time()
            else:
                asctime = None
            if getThreads:
                thread = threading.get_ident()
                threadName = threading.current_thread().name
            else:
                thread = None
                threadName = None
            if getProcesses and hasattr(os, 'getpid'):
                process = os.getpid()
            else:
                process = None
            args = {
                'name': self._name,
                'message': text,
                'levelname': levelname,
                'asctime': asctime,
                'thread': thread,
                'threadName': threadName,
                'process': process
            }
            text = self._formatter._fmt % args
        sys.stdout.write(f"{text}\n")
        
@contextmanager
def switch_verbosity(target:Verbosity, verbosity:str):
    try:
        orig_verbosity = target.verbosity
        target.verbosity = verbosity
        yield
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
    finally:
        target.verbosity = orig_verbosity  