"""
This module will load the components of Boa that are necessary for a Python interpreter with Boa installed.
"""

from . import signal            # Because this module should be loaded from the main thread. It should be the case at interpreter startup...