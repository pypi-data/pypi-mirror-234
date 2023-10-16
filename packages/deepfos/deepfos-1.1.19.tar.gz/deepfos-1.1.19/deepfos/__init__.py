# from .core import *
from .options import OPTION, set_option, show_option

from . import _version
__version__ = _version.get_versions()['version']
