"""
Date utils
"""

from datetime import datetime
from typing import Union

import numpy as np
import pandas as pd

from archimedes import ArchimedesConstants


def get_start_date(start) -> pd.Timestamp:
    """
    Args:
        start (str): The start date provided by the user

    Returns:
        pd.Timestamp: start date given in string form to pd.Timestamp. If not given,
                      or empty, it returns ArchimedesConstants.DATE_LOW
    """
    return pd.to_datetime(start, utc=True) if start else ArchimedesConstants.DATE_LOW


def get_end_date(end) -> pd.Timestamp:
    """
    Args:
        end (str): The end date provided by the user

    Returns:
        pd.Timestamp: end date given in string form to pd.Timestamp. If not given,
                      or empty, it returns ArchimedesConstants.DATE_HIGH
    """
    return pd.to_datetime(end, utc=True) if end else ArchimedesConstants.DATE_HIGH


def convert_to_iso_format(
    input_datetime: Union[str, pd.Timestamp, datetime, np.datetime64, None]
) -> Union[str, None]:
    """
    Convert the input datetime (str, pd.Timestamp, np.datetime64, datetime) to its ISO format string representation.

    Args:
        input_datetime (Union[str, pd.Timestamp, np.datetime64, datetime, None]): Input datetime.

    Returns:
        Union[str, None]: ISO format string representation of the input datetime, or None if input is None or invalid.

    Raises:
        ValueError: If the input is invalid.
    """

    # If the input is a string, strip it and if it is empty, set it to None
    if isinstance(input_datetime, str):
        input_datetime = input_datetime.strip()
        if input_datetime == "":
            input_datetime = None

    pandas_dt = pd.to_datetime(input_datetime, utc=True)

    if pandas_dt == pd.NaT:
        raise ValueError(f"Invalid datetime: {input_datetime}")

    return pandas_dt.isoformat() if pd.isnull(pandas_dt) is False else None
