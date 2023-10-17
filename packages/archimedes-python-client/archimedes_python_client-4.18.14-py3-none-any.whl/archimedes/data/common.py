"""
Common functions for API calls
"""

from functools import partial

from archimedes.configuration import get_api_base_url

get_api_base_url_v2 = partial(get_api_base_url, 2)
get_api_base_url_v3 = partial(get_api_base_url, 3)
