"""
Pipedocs - a CLI tool to automatically generate documentation for Azure Data Factory Pipelines and Azure Synapse Pipelines
"""

import pkgutil
import sys
import warnings

from pipedocs.documenters import Documenter
from pipedocs.generators import Generator
from pipedocs.models import *

__version__ = '0.1.2'

# TODO
#__version__ = '(pkgutil.get_data(__package__, "VERSION") or b"").decode("ascii").strip()'
#
## Check minimum required Python version
#if sys.version_info < (3, 7):
#    print(f"Pipedocs {__version__} requires Python 3.7+")
#    sys.exit(1)
