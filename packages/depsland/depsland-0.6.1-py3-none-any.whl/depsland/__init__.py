if True:
    import lk_logger
    lk_logger.setup(quiet=True, show_varnames=True, async_=False)

from . import api
from . import config
from . import launcher
from . import manifest
from . import paths
from . import system_info
from . import utils
from . import venv
from .api import init
from .api import install
from .api import publish
from .pip import Pip
from .pip import pip
from .pypi import pypi
from .pypi import rebuild_index as rebuild_pypi_index
from .utils import bat_2_exe

__version__ = '0.6.1'
__date__ = '2023-10-07'
