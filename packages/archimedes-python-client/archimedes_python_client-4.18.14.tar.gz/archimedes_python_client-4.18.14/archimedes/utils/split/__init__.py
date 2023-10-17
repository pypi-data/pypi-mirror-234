"""
Module to split requests into smaller queries based on approximate payload size based on the series metadata
"""

from .split import get_queries_observation, get_queries_observation_json
