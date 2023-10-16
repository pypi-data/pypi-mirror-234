__version__ = '0.2.42'

import logging
from bblogger.logger import getLogger

log = getLogger(__name__, 3, appname = "DateParser" )

from .dateparser import DateParser

__all__ = [ 'DateParser' ]
