"""
Get package version of itself.
Technically, it gets the version of the installed package named archimedes-python-client.
"""

import pkg_resources

__version__ = pkg_resources.get_distribution("archimedes-python-client").version
