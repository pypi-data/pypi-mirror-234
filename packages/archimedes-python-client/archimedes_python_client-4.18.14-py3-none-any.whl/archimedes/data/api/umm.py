"""
Urgent Market Messages data from the Archimedes API
"""
# pylint: disable=too-many-arguments

from datetime import datetime
from typing import List, Union

import pandas as pd

from archimedes.data.common import get_api_base_url_v2
from archimedes.utils.api_request import api
from archimedes.utils.date import convert_to_iso_format, get_end_date, get_start_date


def umm_get_series_list(
    *,
    access_token: str = None,
    **kwargs,
) -> list:
    """
    Get a list of all Urgent Market Messages (UMM) series

    Args:
        access_token: Access token

    Returns:
        A list of all UMM types
    """
    data = api.request(
        f"{get_api_base_url_v2()}/umm/get_series_list",
        access_token=access_token,
        **kwargs,
    )
    return data


def umm_get_area_codes(
    series_id: str,
    *,
    access_token: str = None,
    **kwargs,
) -> list:
    """
    Get a list of all price areas available for the specified type of Urgent Market Messages

    Args:
        series_id:
            The type of the UMM's to return (eg - 'UMM/Production' or 'UMM/Transmission').  Get a list of available
            series by using `umm_get_series_list`
        access_token: Access token

    Returns:
        A list of all price areas
    """
    query = {
        "series_id": series_id,
    }
    data = api.request(
        f"{get_api_base_url_v2()}/umm/get_area_codes",
        access_token=access_token,
        params=query,
        **kwargs,
    )
    return data


def umm_get_summary(
    series_ids: List[str],
    price_areas: Union[str, List[str]] = None,
    start: Union[str, pd.Timestamp, datetime, None] = None,
    end: Union[str, pd.Timestamp, datetime, None] = None,
    ref_dt_lag_hours: Union[int, None] = None,
    ref_dt: Union[int, None] = None,
    treat_generation_as_production: bool = True,
    *,
    access_token: str = None,
    **kwargs,
) -> pd.DataFrame:
    """
    Get Urgent Market Messages summarized for every hour between `start` and `end`.

    NOTE - The output may not contain all hours in the requested time frame - hourly summarys will only exist for
    hours in which UMMs have been reported.

    Args:
        series_ids:
            The types of the UMM's to return (eg - 'UMM/Production' or 'UMM/Transmission').  Get a list of available
            series by using `umm_get_series_list`
        price_areas:
            The price areas to filter by (eg - 'NO2', 'NO5', or 'DE1-NO1').  Retrieve a list of all available price
            areas for each series by using `umm_get_area_codes`
        start:
            The first datetime to fetch (inclusive). Returns all if not set. Should be specified in ISO 8601 format
            (eg - '2021-11-29T06:00:00+00:00')
        end:
            The last datetime to fetch (exclusive). Returns all if not set. Should be specified in ISO 8601 format
            (eg - '2021-11-30T06:00:00+00:00')
        ref_dt_lag_hours:
            Only return data in which the interval between the publication timestamp and the time period start is
            greater than or equal to the provided number of hours.  Cannot be used with ref_dt parameter.
        ref_dt:
            Only return data in which the publication timestamp is earlier or equal to the provided timestamp. Cannot
            be used with ref_dt_lag_hours parameter. Should be specified in ISO 8601 format
            (eg - '2021-11-29T06:00:00+00:00')
        treat_generation_as_production:
            If true, treats all generation as production.
            The Nordpool API separates power production into two series - "Production" and "Generation".  But, their
            User Interface lists them both as "Production".  Setting this boolean to True will emulate that behavior.
        access_token: Access token

    Returns:
        Dataframe with the Urgent Market Messages
    """
    if isinstance(series_ids, str):
        series_ids = [series_ids]
    if isinstance(price_areas, str):
        price_areas = [price_areas]

    start = convert_to_iso_format(get_start_date(start))
    end = convert_to_iso_format(get_end_date(end))

    query = {
        "series_ids": series_ids,
        "price_areas": price_areas,
        "start": start,
        "end": end,
        "ref_dt_lag_hours": ref_dt_lag_hours,
        "ref_dt": ref_dt,
        "treat_generation_as_production": treat_generation_as_production,
    }
    data = api.request(
        f"{get_api_base_url_v2()}/umm/get_summary",
        access_token=access_token,
        params=query,
        **kwargs,
    )
    return pd.DataFrame.from_dict(data)


def umm_get(
    series_ids: List[str],
    price_areas: Union[str, List[str]] = None,
    start: Union[str, pd.Timestamp, datetime, None] = None,
    end: Union[str, pd.Timestamp, datetime, None] = None,
    ref_dt_lag_hours: Union[int, None] = None,
    ref_dt: Union[int, None] = None,
    include_history: bool = False,
    treat_generation_as_production: bool = True,
    *,
    access_token: str = None,
    **kwargs,
) -> pd.DataFrame:
    """
    Get Urgent Market Messages for every hour between `start` and `end`.

    Args:
        series_ids:
            The types of the UMM's to return (eg - 'UMM/Production' or 'UMM/Transmission').  Get a list of available
            series by using `umm_get_series_list`
        price_areas:
            The price areas to filter by (eg - 'NO2', 'NO5', or 'DE1-NO1').  Retrieve a list of all available price
            areas for each series by using `umm_get_area_codes`
        start:
            The first datetime to fetch (inclusive). Returns all if not set. Should be specified in ISO 8601 format
            (eg - '2021-11-29T06:00:00+00:00')
        end:
            The last datetime to fetch (exclusive). Returns all if not set. Should be specified in ISO 8601 format
            (eg - '2021-11-30T06:00:00+00:00')
        ref_dt_lag_hours:
            Only return data in which the interval between the publication timestamp and the time period start is
            greater than or equal to the provided number of hours.  Cannot be used with ref_dt parameter.
        ref_dt:
            Only return data in which the publication timestamp is earlier or equal to the provided timestamp. Cannot
            be used with ref_dt_lag_hours parameter. Should be specified in ISO 8601 format
            (eg - '2021-11-29T06:00:00+00:00')
        include_history:
            If True, Returns all data set. If False, Only returns the latest version for each message id.
        treat_generation_as_production:
            If true, treats all generation as production.
            The Nordpool API separates power production into two series - "Production" and "Generation".  But, their
            User Interface lists them both as "Production".  Setting this boolean to True will emulate that behavior.
        access_token: Access token

    Returns:
        Dataframe with the Urgent Market Messages
    """

    if isinstance(series_ids, str):
        series_ids = [series_ids]
    if isinstance(price_areas, str):
        price_areas = [price_areas]

    start = convert_to_iso_format(get_start_date(start))
    end = convert_to_iso_format(get_end_date(end))

    query = {
        "series_ids": series_ids,
        "price_areas": price_areas,
        "start": start,
        "end": end,
        "ref_dt_lag_hours": ref_dt_lag_hours,
        "ref_dt": ref_dt,
        "include_history": include_history,
        "treat_generation_as_production": treat_generation_as_production,
    }
    data = api.request(
        f"{get_api_base_url_v2()}/umm/get",
        access_token=access_token,
        params=query,
        **kwargs,
    )
    return pd.DataFrame.from_dict(data)


def umm_get_by_id(
    message_id: str,
    include_history: bool = False,
    treat_generation_as_production: bool = True,
    *,
    access_token: str = None,
    **kwargs,
) -> pd.DataFrame:
    """
    Get all the Urgent Market Messages associated with the specified message ID.

    Args:
        message_id:
            The ID of the messages to return.
        include_history:
            Include messages which have been superseded by newer updates to the same UMM.
        treat_generation_as_production:
            Update the series ID parameter of the output to replace "Generation" with "Production".
            The Nordpool API separates power production into two series - "Production" and "Generation".  But, their
            User Interface lists them both as "Production".  Setting this boolean to True will emulate that behavior.
        access_token: Access token

    Returns:
        Dataframe with the Urgent Market Messages
    """

    query = {
        "message_id": message_id,
        "include_history": include_history,
        "treat_generation_as_production": treat_generation_as_production,
    }
    data = api.request(
        f"{get_api_base_url_v2()}/umm/get_by_id",
        access_token=access_token,
        params=query,
        **kwargs,
    )
    return pd.DataFrame.from_dict(data)
