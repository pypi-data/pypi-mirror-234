"""
Get metadata about the data available in the Archimedes API
"""

import re

import pandas as pd

from archimedes.data.common import get_api_base_url_v2
from archimedes.utils.api_request import api


def list_series_price_areas(
    series_id: str, *, access_token: str = None, **kwargs
) -> pd.DataFrame:
    """
    Retrieve all the price_areas which are available for the specified data series

    Example:
        >>> import archimedes
        >>> archimedes.list_series_price_areas('NP/AreaPrices')
           price_areas
        0          DK1
        1          DK2
        ...        ...
        10         SE3
        11         SE4

    Returns:
        Dataframe with all available price areas for the specified series_id
    """
    query = {
        "series_id": series_id,
    }
    base_url = get_api_base_url_v2()
    data = api.request(
        f"{base_url}/data/list_series_price_areas",
        access_token=access_token,
        params=query,
        **kwargs,
    )
    data = pd.DataFrame.from_dict(data)

    observation_data = api.request(
        f"{base_url}/observation_json/list_series_price_areas",
        access_token=access_token,
        params=query,
        **kwargs,
    )
    observation_data = pd.DataFrame.from_dict(observation_data)

    price_area_df = pd.concat([data, observation_data]).drop_duplicates()
    price_area_df = price_area_df.sort_values("price_areas").reset_index(drop=True)
    return price_area_df


def list_ids(sort: bool = False, *, access_token: str = None, **kwargs) -> pd.DataFrame:
    """List all the series ids available.

    Example:
        >>> import archimedes
        >>> archimedes.list_ids()
                                    series_id
        0   NP/NegativeProductionImbalancePrices
        1                    NP/ProductionTotals
        ..                                   ...
        38                 NP/OrdinaryDownVolume
        39                    NP/SpecialUpVolume

    Args:
        sort (bool): False - return all series in one dataframe column, True - order
                             dataframe by data-origin
        access_token (str, optional): None - access token for the API

    Returns:
        DataFrame with all available list_ids
    """
    base_url = get_api_base_url_v2()
    data = api.request(f"{base_url}/data/list_ids", access_token=access_token, **kwargs)
    data = pd.DataFrame.from_dict(data)

    observation_data = api.request(
        f"{base_url}/observation_json/list_ids",
        access_token=access_token,
        **kwargs,
    )
    observation_data = pd.DataFrame.from_dict(observation_data)

    series_df = pd.concat([data, observation_data]).drop_duplicates()
    series_df = series_df.sort_values(["series_id"]).reset_index(drop=True)
    if not sort:
        return series_df

    series_df["pre"] = series_df["series_id"].str.split("/", 1).str[0]
    series_df = pd.DataFrame.from_dict(
        series_df.groupby("pre")["series_id"].apply(list).to_dict(), orient="index"
    ).transpose()
    series_df = series_df[sorted(series_df.columns)]

    series_df = series_df.fillna("")
    return series_df.copy()


def list_ids_expanded(
    id_filter=None, source_filter=None, name_filter=None, case_sensitive=False, **kwargs
):
    """
    Obtain series ids from archimedes in a dataframe, with the series_ids expanded into columns for series
    "source" and "name".

    Args:
        id_filter: str -> regular expression to filter the series_ids.
        source_filter: str -> regular expression to filter the sources.
        name_filter: str -> regular expression to filter the series names.
        case_sensitive: boolean -> if filtering is case sensitive or not
        **kwargs: arguments for the archimedes.list_ids function, passed through. Note: the sort arg is dropped
                (superceeded by this function)

    Returns:
        dataframe with columns ["series_id", "source", "series_name"]

    Example:
        >>> srs1 = list_ids_expanded(source_filter=".")
        >>> srs1.head()

        series_id	                    source  series_name
    0	ENT/AfrrActivatedPricesDown     ENT     AfrrActivatedPricesDown
    1	ENT/AfrrActivatedPricesUp       ENT     AfrrActivatedPricesUp
    2	ENT/AfrrActivatedVolumesDown    ENT     AfrrActivatedVolumesDown
    3	ENT/AfrrActivatedVolumesUp      ENT     AfrrActivatedVolumesUp
    4	ENT/AfrrProcuredPricesDownD1    ENT     AfrrProcuredPricesDownD1
    """
    if "sort" in kwargs:
        kwargs.pop("sort")

    series_names = list_ids(**kwargs)

    series_names[["source", "series_name"]] = series_names["series_id"].str.split(
        "/", expand=True
    )

    flags = 0 if case_sensitive else re.IGNORECASE
    for filter_pattern, column in (
        (id_filter, "series_id"),
        (source_filter, "source"),
        (name_filter, "series_name"),
    ):
        if filter_pattern is None:
            continue
        series_names = series_names[
            series_names[column].str.contains(filter_pattern, flags=flags)
        ]

    return series_names


def list_prediction_ids(*, access_token: str = None, **kwargs) -> pd.DataFrame:
    """List all the prediction series ids available.

    Example:
        >>> import archimedes
        >>> archimedes.list_prediction_ids()
                                     series_id
        0               PX/rk-nn-probabilities
        1   PX/rk-nn-direction-probabilities/U
        ..                                ...
        22                           PX/rk-901
        23                         PX/rk-naive
    """

    data = api.request(
        f"{get_api_base_url_v2()}/data/list_prediction_ids",
        access_token=access_token,
        **kwargs,
    )

    return pd.DataFrame.from_dict(data)
