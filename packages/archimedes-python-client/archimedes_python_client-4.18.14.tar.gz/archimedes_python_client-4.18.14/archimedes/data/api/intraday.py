"""
Get intraday trades data from the Archimedes API
"""

import json
from datetime import datetime
from typing import List, Union

import pandas as pd

from archimedes.data.common import get_api_base_url_v2
from archimedes.utils.api_request import api
from archimedes.utils.date import convert_to_iso_format, get_end_date, get_start_date
from archimedes.utils.split import get_queries_observation_json
from archimedes.utils.threaded_executor import execute_many


def get_intraday_trades(
    price_areas: List[str] = None,
    start: Union[str, pd.Timestamp, datetime, None] = None,
    end: Union[str, pd.Timestamp, datetime, None] = None,
    *,
    access_token: str = None,
    **kwargs,
) -> pd.DataFrame:
    """Get raw intraday trades from Archimedes Database

    This function can be used to fetch raw time series from the Archimedes Database
    without any post-processing.
    To see which series are available, use `list_ids()`.

    Example:
        >>> import archimedes
        >>> archimedes.get_intraday_trades(
        >>>     price_areas=["NO1",],
        >>>     start="2020-06-20T04:00:00+00:00",
        >>>     end="2020-06-20T09:00:00+00:00",
        >>> )
                              from_dt                      to_dt          series_id  price  volume                    trade_time buy_area sell_area                                         attributes
        0   2020-06-20T04:00:00+00:00  2020-06-20T05:00:00+00:00  NP/IntradayTrades   7.05     0.9  2020-06-19T15:55:24.817+0000      OPX       NO1  {'price': 7.05, 'buy_area': 'OPX', 'currency':...
        1   2020-06-20T05:00:00+00:00  2020-06-20T06:00:00+00:00  NP/IntradayTrades   6.80     0.9  2020-06-19T15:55:24.817+0000      OPX       NO1  {'price': 6.8, 'buy_area': 'OPX', 'currency': ...
        2   2020-06-20T06:00:00+00:00  2020-06-20T07:00:00+00:00  NP/IntradayTrades   7.75     0.9  2020-06-19T15:55:24.817+0000      OPX       NO1  {'price': 7.75, 'buy_area': 'OPX', 'currency':...
        3   2020-06-20T07:00:00+00:00  2020-06-20T08:00:00+00:00  NP/IntradayTrades   1.70     0.1  2020-06-19T20:20:14.765+0000       FI       NO1  {'price': 1.7, 'buy_area': 'FI', 'currency': '...
        4   2020-06-20T07:00:00+00:00  2020-06-20T08:00:00+00:00  NP/IntradayTrades   8.30     0.9  2020-06-19T15:55:24.817+0000      OPX       NO1  {'price': 8.3, 'buy_area': 'OPX', 'currency': ...
        5   2020-06-20T08:00:00+00:00  2020-06-20T09:00:00+00:00  NP/IntradayTrades   2.60     2.0  2020-06-19T20:19:56.057+0000      OPX       NO1  {'price': 2.6, 'buy_area': 'OPX', 'currency': ...
        6   2020-06-20T08:00:00+00:00  2020-06-20T09:00:00+00:00  NP/IntradayTrades   2.60     6.0  2020-06-19T20:19:56.057+0000      OPX       NO1  {'price': 2.6, 'buy_area': 'OPX', 'currency': ...
        7   2020-06-20T08:00:00+00:00  2020-06-20T09:00:00+00:00  NP/IntradayTrades   2.60     6.0  2020-06-19T20:19:56.057+0000      OPX       NO1  {'price': 2.6, 'buy_area': 'OPX', 'currency': ...
        8   2020-06-20T08:00:00+00:00  2020-06-20T09:00:00+00:00  NP/IntradayTrades   2.60     6.0  2020-06-19T20:19:56.057+0000      OPX       NO1  {'price': 2.6, 'buy_area': 'OPX', 'currency': ...
        9   2020-06-20T08:00:00+00:00  2020-06-20T09:00:00+00:00  NP/IntradayTrades   2.60     0.9  2020-06-19T20:19:56.057+0000      OPX       NO1  {'price': 2.6, 'buy_area': 'OPX', 'currency': ...
        10  2020-06-20T08:00:00+00:00  2020-06-20T09:00:00+00:00  NP/IntradayTrades   2.60     6.0  2020-06-19T20:19:56.057+0000      OPX       NO1  {'price': 2.6, 'buy_area': 'OPX', 'currency': ...
        11  2020-06-20T08:00:00+00:00  2020-06-20T09:00:00+00:00  NP/IntradayTrades   2.60     0.1  2020-06-19T20:19:56.057+0000      OPX       NO1  {'price': 2.6, 'buy_area': 'OPX', 'currency': ...
        12  2020-06-20T08:00:00+00:00  2020-06-20T09:00:00+00:00  NP/IntradayTrades   2.60     6.0  2020-06-19T20:19:56.057+0000      OPX       NO1  {'price': 2.6, 'buy_area': 'OPX', 'currency': ...
        13  2020-06-20T08:00:00+00:00  2020-06-20T09:00:00+00:00  NP/IntradayTrades   2.60     6.0  2020-06-19T20:19:56.057+0000      OPX       NO1  {'price': 2.6, 'buy_area': 'OPX', 'currency': ...
        14  2020-06-20T08:00:00+00:00  2020-06-20T09:00:00+00:00  NP/IntradayTrades   2.60     6.0  2020-06-19T20:19:56.057+0000      OPX       NO1  {'price': 2.6, 'buy_area': 'OPX', 'currency': ...
        15  2020-06-20T08:00:00+00:00  2020-06-20T09:00:00+00:00  NP/IntradayTrades   2.60     5.1  2020-06-19T20:19:56.057+0000      OPX       NO1  {'price': 2.6, 'buy_area': 'OPX', 'currency': ...
        16  2020-06-20T08:00:00+00:00  2020-06-20T09:00:00+00:00  NP/IntradayTrades   9.90     0.9  2020-06-19T15:55:24.817+0000      OPX       NO1  {'price': 9.9, 'buy_area': 'OPX', 'currency': ...

    Args:
        price_areas (List[str], optional): The price areas to pick, all price areas if None. Defaults to None.
        start (str, optional): The first datetime to fetch (inclusive). Returns all if None. Defaults to None.
        end (str, optional): The last datetime to fetch (exclusive). Returns all if None. Defaults to None.
        access_token (str, optional): None - access token for the API

    Returns:
        DataFrame with all the time series data

    Raises:
        HTTPError: If an HTTP error occurs when requesting the API.
        NoneAuth: If the user is unauthorized or if the authorization has expired.
    """  # pylint:disable=line-too-long

    if isinstance(price_areas, str):
        price_areas = [price_areas]

    start = convert_to_iso_format(get_start_date(start))
    end = convert_to_iso_format(get_end_date(end))

    queries = get_queries_observation_json(
        ["NP/IntradayTrades"],
        price_areas,
        start,
        end,
    )

    base_url = get_api_base_url_v2()

    params_array = [
        {
            "url": f"{base_url}/observation_json/get",
            "access_token": access_token,
            "params": query,
            **kwargs,
        }
        for query in queries
    ]

    observation_data = execute_many(api.request, params_array)

    if len(observation_data) == 0:
        return pd.DataFrame(
            columns=[
                "from_dt",
                "to_dt",
                "series_id",
                "price",
                "volume",
                "trade_time",
                "buy_area",
                "sell_area",
                "attributes",
                "tx_index",
            ]
        )
    observation_data = [
        {
            **i,
            "price": i["value"].get("price"),
            "volume": i["value"].get("quantity"),
            "trade_time": i["value"].get("trade_time"),
            "no_of_occurrences": i["value"].get("no_of_occurrences", 1),
        }
        for i in observation_data
    ]
    observation_data = pd.DataFrame(observation_data)

    # get only max version
    observation_data = pd.merge(
        observation_data,
        observation_data.groupby(
            ["from_dt", "to_dt", "series_id", "price_area"], as_index=False
        )["version"].max(),
        on=["from_dt", "to_dt", "series_id", "price_area", "version"],
        how="inner",
    )

    # Extracting buy area and sell area from price_area
    observation_data[["buy_area", "sell_area"]] = observation_data[
        "price_area"
    ].str.split("-", n=2, expand=True)
    observation_data["value"] = observation_data["value"].apply(json.dumps)

    observation_data["volume"] = (
        observation_data["volume"] / observation_data["no_of_occurrences"]
    )
    # duplicate data based on no_of_occurrences
    observation_data = observation_data.loc[
        observation_data.index.repeat(observation_data["no_of_occurrences"])
    ]
    observation_data["tx_index"] = 1
    observation_data["tx_index"] = observation_data.groupby(
        list(set(observation_data.columns) - {"tx_index"})
    )["tx_index"].cumsum()

    observation_data["attributes"] = observation_data["value"].apply(json.loads)
    observation_data = observation_data.drop(
        ["value", "version", "price_area", "no_of_occurrences"],
        axis=1,
    )
    observation_data = observation_data.sort_values(by=["from_dt"]).reset_index(
        drop=True
    )

    return observation_data
