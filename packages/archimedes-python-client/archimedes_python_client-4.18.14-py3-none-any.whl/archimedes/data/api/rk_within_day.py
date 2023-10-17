"""
Get RK within day data from the Archimedes API
"""

from datetime import datetime
from typing import Union

import pandas as pd

from archimedes.data.common import get_api_base_url_v3
from archimedes.utils.api_request import api
from archimedes.utils.date import convert_to_iso_format


def directions(
    start: Union[str, pd.Timestamp, datetime],
    end: Union[str, pd.Timestamp, datetime],
    price_area: str,
    ref_dt: Union[str, pd.Timestamp, datetime, None] = None,
    *,
    access_token: str = None,
    **kwargs,
) -> pd.DataFrame:
    """
    The predicted probability of any given hour is up(UP), down(DOWN) or no direction(NONE).

    Parameters:
        start: The first hour to fetch prediction for (inclusive).
        end: The last time to fetch prediction for (inclusive).
        price_area: The name of the price area (eg - 'NO2', 'SE4').
        ref_dt: The time of the latest RK data to include in the forecast. If not provided, all the data for the given
                hours with all available ref_dt will be returned.
        access_token: Access token
    """
    start = convert_to_iso_format(start)
    end = convert_to_iso_format(end)
    ref_dt = convert_to_iso_format(ref_dt)
    query = {
        "start": start,
        "end": end,
        "price_area": price_area,
    }
    if ref_dt is not None:
        query["ref_dt"] = ref_dt
    data = api.request(
        f"{get_api_base_url_v3()}/rk_within_day/directions",
        access_token=access_token,
        params=query,
        **kwargs,
    )
    return pd.DataFrame.from_dict(data)


def distributions(
    start: Union[str, pd.Timestamp, datetime],
    end: Union[str, pd.Timestamp, datetime],
    price_area: str,
    ref_dt: Union[str, pd.Timestamp, datetime, None] = None,
    *,
    access_token: str = None,
    **kwargs,
) -> pd.DataFrame:
    """
    The predicted imbalance price distribution.

    In the response, spread is defined as the difference between the RK price and the spot price (priceRK - pricespot).

    Parameters:
        start: The first hour to fetch prediction for (inclusive).
        end: The last time to fetch prediction for (inclusive).
        price_area: The name of the price area (eg - 'NO2', 'SE4').
        ref_dt: The time of the latest RK data to include in the forecast. If not provided, all the data for the given
                hours with all available ref_dt will be returned.
        access_token: Access token
    """
    start = convert_to_iso_format(start)
    end = convert_to_iso_format(end)
    ref_dt = convert_to_iso_format(ref_dt)
    query = {
        "start": start,
        "end": end,
        "price_area": price_area,
    }
    if ref_dt is not None:
        query["ref_dt"] = ref_dt
    data = api.request(
        f"{get_api_base_url_v3()}/rk_within_day/distributions",
        access_token=access_token,
        params=query,
        **kwargs,
    )
    return pd.DataFrame.from_dict(data)


def large_up_fps(  # pylint: disable=too-many-arguments
    start: Union[str, pd.Timestamp, datetime],
    end: Union[str, pd.Timestamp, datetime],
    price_area: str,
    large_price_level: int,
    ref_dt: Union[str, pd.Timestamp, datetime, None] = None,
    conditional: bool = True,
    *,
    access_token: str = None,
    **kwargs,
) -> pd.DataFrame:
    """
    Indicator for whether a given hour will experience a large up RK price.

    Parameters:
        start: The first hour to fetch prediction for (inclusive).
        end: The last time to fetch prediction for (inclusive).
        price_area: The name of the price area (eg - 'NO2', 'SE4').
        large_price_level: The abs(priceRK - priceSpot) spread in €/MWh above which price the RK-spot spread is
                            considered large. Supported values are 20, 50 and 100.
        ref_dt: The time of the latest RK data to include in the forecast. If not provided, all the data for the given
                hours with all available ref_dt will be returned.
        conditional: Whether to fetch conditional data (one of 'True' and 'False'). Defaults to True.
        access_token: Access token
    """
    start = convert_to_iso_format(start)
    end = convert_to_iso_format(end)
    ref_dt = convert_to_iso_format(ref_dt)
    query = {
        "start": start,
        "end": end,
        "price_area": price_area,
        "large_price_level": large_price_level,
        "conditional": conditional,
    }
    if ref_dt is not None:
        query["ref_dt"] = ref_dt
    data = api.request(
        f"{get_api_base_url_v3()}/rk_within_day/large_up_fps",
        access_token=access_token,
        params=query,
        **kwargs,
    )
    return pd.DataFrame.from_dict(data)


def large_down_fps(  # pylint: disable=too-many-arguments
    start: Union[str, pd.Timestamp, datetime],
    end: Union[str, pd.Timestamp, datetime],
    price_area: str,
    large_price_level: int,
    ref_dt: Union[str, pd.Timestamp, datetime, None] = None,
    conditional: bool = True,
    *,
    access_token: str = None,
    **kwargs,
) -> pd.DataFrame:
    """
    Indicator for whether a given hour will experience a large down RK price.

    Parameters:
        start: The first hour to fetch prediction for (inclusive).
        end: The last time to fetch prediction for (inclusive).
        price_area: The name of the price area (eg - 'NO2', 'SE4').
        large_price_level: The abs(priceRK - priceSpot) spread in €/MWh above which price the RK-spot spread is
                            considered large. Supported values are 20, 50 and 100.
        ref_dt: The time of the latest RK data to include in the forecast. If not provided, all the data for the given
                hours with all available ref_dt will be returned.
        conditional: Whether to fetch conditional data (one of 'True' and 'False'). Defaults to True.
        access_token: Access token
    """
    start = convert_to_iso_format(start)
    end = convert_to_iso_format(end)
    ref_dt = convert_to_iso_format(ref_dt)
    query = {
        "start": start,
        "end": end,
        "price_area": price_area,
        "large_price_level": large_price_level,
        "conditional": conditional,
    }
    if ref_dt is not None:
        query["ref_dt"] = ref_dt
    data = api.request(
        f"{get_api_base_url_v3()}/rk_within_day/large_down_fps",
        access_token=access_token,
        params=query,
        **kwargs,
    )
    return pd.DataFrame.from_dict(data)


def comparison_by_price(
    start: Union[str, pd.Timestamp, datetime],
    end: Union[str, pd.Timestamp, datetime],
    price_area: str,
    ref_price: int,
    ref_dt: Union[str, pd.Timestamp, datetime, None] = None,
    *,
    access_token: str = None,
    **kwargs,
) -> pd.DataFrame:
    """
    Get the probability of the RK price being less than or equal to the user specified reference price for each hour
    between start and end (inclusive).

    Parameters:
        start: The first hour to fetch prediction for (inclusive).
        end: The last time to fetch prediction for (inclusive).
        price_area: The name of the price area (eg - 'NO2', 'SE4').
        ref_price: The reference price in € for price comparison.
        ref_dt: The time of the latest RK data to include in the comparison.
                If None, the latest available reference date is used.
        access_token: Access token
    """
    start = convert_to_iso_format(start)
    end = convert_to_iso_format(end)
    ref_dt = convert_to_iso_format(ref_dt)
    query = {
        "start": start,
        "end": end,
        "price_area": price_area,
        "ref_price": ref_price,
        "ref_dt": ref_dt,
    }
    data = api.request(
        f"{get_api_base_url_v3()}/rk_within_day/price_comparison/by_price",
        access_token=access_token,
        params=query,
        **kwargs,
    )
    return pd.DataFrame.from_dict(data)
