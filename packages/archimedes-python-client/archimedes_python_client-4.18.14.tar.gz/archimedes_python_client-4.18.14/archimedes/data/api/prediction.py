"""
Get predictions from the Archimedes API
"""

import json
from datetime import datetime
from typing import Dict, List, Union

import pandas as pd
from requests.exceptions import HTTPError

from archimedes.data.common import get_api_base_url_v2
from archimedes.data.types import PredictionData
from archimedes.utils.api_request import api
from archimedes.utils.date import convert_to_iso_format
from archimedes.utils.idempotency import generate_idempotency_key
from archimedes.utils.threaded_executor import execute_many


def get_predictions(  # pylint:disable=too-many-arguments,too-many-locals
    series_ids: List[str] = None,
    price_areas: List[str] = None,
    filter_by: List[str] = None,
    start: Union[str, pd.Timestamp, datetime, None] = None,
    end: Union[str, pd.Timestamp, datetime, None] = None,
    ref_dt_start: Union[str, pd.Timestamp, datetime, None] = None,
    ref_dt_end: Union[str, pd.Timestamp, datetime, None] = None,
    *,
    access_token: str = None,
    **kwargs,
) -> pd.DataFrame:
    """Get any number of predictions

    This function can be used to fetch predictions from the Archimedes Database.

    Unlike `archimedes.get`, this will return a list, not a dataframe.

    Example:
        >>> import archimedes
        >>> archimedes.get_predictions(
        >>>    series_ids=["PX/rk-naive"],
        >>>    price_areas=["NO1"],
        >>>    start="2020"
        >>> )
        >>> [...]

    Args:
        series_ids (List[str], optional): The series ids to get.
        price_areas (List[str], optional): The price areas to get the data for.
        filter_by (List[str], optional):
            Additional filtering of the json_data field.  The fields available
            will vary depending on the series_id being fetched.  Examples:
                'variant=COND', 'direction=UP', 'hours_ahead>=5'
        start (str, pd.Timestamp, optional):
            The first datetime to fetch (inclusive). Returns all if None.
            Defaults to None.
        end (str, pd.Timestamp, optional):
            The last datetime to fetch (exclusive). Returns all if None.
            Defaults to None.
        ref_dt_start (str, pd.Timestamp, optional):
            The earliest ref_dt to fetch (inclusive). Defaults to None.
        ref_dt_end (str, pd.Timestamp, optional):
            The latest ref_dt to fetch (exclusive). Defaults to None.
        access_token (str, optional): None - access token for the API

    Returns:
        DataFrame with all the prediction data
    """
    if isinstance(series_ids, str):
        series_ids = [series_ids]

    if isinstance(price_areas, str):
        price_areas = [price_areas]

    if isinstance(filter_by, str):
        filter_by = [filter_by]

    start = convert_to_iso_format(start)
    end = convert_to_iso_format(end)
    ref_dt_start = convert_to_iso_format(ref_dt_start)
    ref_dt_end = convert_to_iso_format(ref_dt_end)

    query = {}

    if start is not None:
        query["start"] = pd.to_datetime(start, utc=True)

    if end is not None:
        query["end"] = pd.to_datetime(end, utc=True)

    if ref_dt_start is not None:
        query["ref_dt_start"] = pd.to_datetime(ref_dt_start, utc=True)

    if ref_dt_end is not None:
        query["ref_dt_end"] = pd.to_datetime(ref_dt_end, utc=True)

    if filter_by is not None:
        query["filter_by"] = filter_by

    queries = [query]
    if series_ids is not None:
        queries = [
            {"series_ids": series_id, "price_areas": price_areas, **query}
            for query in queries
            for series_id in series_ids
        ]

    def _merge_function(result, aggr):
        if aggr is None:
            aggr = []
        for item in result:
            if "json_data" in item:
                json_data = item.get("json_data")
                item.update(json_data)
                del item["json_data"]
            aggr.append(item)
        return aggr

    params_array = [
        {
            "url": f"{get_api_base_url_v2()}/data/get_predictions",
            "access_token": access_token,
            "params": query,
            **kwargs,
        }
        for query in queries
    ]

    data = execute_many(api.request, params_array, _merge_function)

    df = pd.DataFrame.from_dict(data)

    date_fields = ["from_dt", "run_dt", "ref_dt"]

    for date_field in date_fields:
        if date_field in df:
            df[date_field] = pd.to_datetime(df[date_field], utc=True)

    df = df.fillna("")

    return df


def get_predictions_ref_dts(
    prediction_id: str = None, *, access_token: str = None, **kwargs
) -> pd.DataFrame:
    """Get which ref_dts are available.

    ref_dt == prediction_build_dt
    Users views in the database.

    Args:
        prediction_id (str): The series id to get the reference dts for. If None, get
                             ref_dts for all prediction_ids.
        access_token (str, optional): Access token for the API

    Returns:
        DataFrame with all ref_dts
    """
    query = {}

    if prediction_id:
        query["prediction_id"] = prediction_id

    data = api.request(
        f"{get_api_base_url_v2()}/data/get_predictions_ref_dts",
        access_token=access_token,
        params=query,
        **kwargs,
    )

    return pd.DataFrame.from_dict(data)


def get_latest_predictions_ref_dt(
    series_id: str,
    price_area: Union[str, None] = None,
    time_interval: Union[int, None] = None,
    *,
    access_token: str = None,
    **kwargs,
) -> Union[pd.Timestamp, None]:
    """
    Returns the latest timestamp at which prediction for the series ID was made.

    Arguments:
        series_id (str): Series ID to filter
        price_area (str, optional): Price Area to filter
        time_interval (int):
            Optimal time difference in number of days between
            the time at which prediction was made
            and the time for which the prediction was made for the series id.

            It is better to be conservative and provide a time difference that is slightly higher
            the optimal time difference.

            As long as an adequately large value has been provided,
            this parameter will not change the result value; only how fast the result is computed

            For most cases, sending None is the most optimal. When unsure about the value, use None.
            Defaults to None.
        access_token (str, optional): Access token for the API
    """
    query = {"series_id": series_id, "time_interval": time_interval}
    if price_area:
        query["price_area"] = price_area
    try:
        data = api.request(
            f"{get_api_base_url_v2()}/data/get_latest_predictions_ref_dt",
            access_token=access_token,
            params=query,
            **kwargs,
        )["latest_preds_ref_dt"]
    except HTTPError as err:
        if "No data for provided filters." in str(err):
            return None
        raise

    return pd.to_datetime(data, utc=True)


def store_prediction(
    prediction_id: str,
    from_dt: Union[str, pd.Timestamp, datetime],
    ref_dt: Union[str, pd.Timestamp, datetime],
    run_dt: Union[str, pd.Timestamp, datetime],
    data: Dict,
    *,
    use_idempotency: bool = True,
    access_token: str = None,
    **kwargs,
) -> bool:
    """Store a prediction

    Example:
        >>> import archimedes
        >>> import pandas as pd
        >>> from dateutil.tz import gettz
        >>>
        >>> tz_oslo = gettz("Europe/Oslo")
        >>> d = {
        >>>     "direction": "D",
        >>>     "probability": 0.8632089971077396,
        >>>     "hours_ahead": 1,
        >>>     "price_area": "NO1"
        >>> }
        >>> archimedes.store_prediction(
        >>>     prediction_id="test-prediction-id",
        >>>     from_dt=pd.Timestamp("2021-04-11 23:47:16.854775807", tz=tz_oslo),
        >>>     ref_dt=pd.Timestamp("2021-04-10 23:00:00.000000000", tz=tz_oslo),
        >>>     run_dt=pd.Timestamp.now(tz=tz_oslo),
        >>>     data=d
        >>> )
        True
    """
    payload = {
        "prediction_id": prediction_id,
        "from_dt": convert_to_iso_format(from_dt),
        "ref_dt": convert_to_iso_format(ref_dt),
        "run_dt": convert_to_iso_format(run_dt),
        "data": data,
    }

    headers = {"Content-Type": "application/json"}

    if use_idempotency:
        headers["X-Idempotent-Key"] = generate_idempotency_key()

    ret = api.request(
        f"{get_api_base_url_v2()}/data/store_prediction",
        method="POST",
        data=json.dumps(payload),
        headers=headers,
        access_token=access_token,
        **kwargs,
    )

    return ret.get("success", False)


def store_predictions(
    prediction_id: str,
    prediction_data: List[PredictionData],
    *,
    use_idempotency: bool = True,
    access_token: str = None,
    **kwargs,
) -> bool:
    """Store a prediction

    Example:
        >>> import archimedes
        >>> import pandas as pd
        >>> from dateutil.tz import gettz
        >>> from archimedes.data.types import PredictionData
        >>>
        >>> tz_oslo = gettz("Europe/Oslo")
        >>> pid = "test-prediction-id"
        >>> from_dt = pd.Timestamp("2021-04-11 23:47:16.854775807", tz=tz_oslo)
        >>> ref_dt = pd.Timestamp("2021-04-10 23:00:00.000000000", tz=tz_oslo)
        >>> run_dt = pd.Timestamp.now(tz=tz_oslo)
        >>> data = {
        >>>     "direction": "D",
        >>>     "probability": 0.8632089971077396,
        >>>     "hours_ahead": 1,
        >>>     "price_area": "NO1"
        >>> }
        >>> p_data = [
        >>>    PredictionData(from_dt=from_dt, ref_dt=ref_dt, run_dt=run_dt, data=data)
        >>> ]
        >>> archimedes.store_predictions(
        >>>     prediction_id=pid,
        >>>     prediction_data=p_data
        >>> )
        True
    """

    predictions = [
        {
            "from_dt": convert_to_iso_format(p["from_dt"]),
            "ref_dt": convert_to_iso_format(p["ref_dt"]),
            "run_dt": convert_to_iso_format(p["run_dt"]),
            "data": p["data"],
        }
        for p in prediction_data
    ]

    payload = {
        "prediction_id": prediction_id,
        "data": predictions,
    }

    headers = {"Content-Type": "application/json"}

    if use_idempotency:
        headers["X-Idempotent-Key"] = generate_idempotency_key()

    ret = api.request(
        f"{get_api_base_url_v2()}/data/store_predictions",
        method="POST",
        data=json.dumps(payload),
        headers=headers,
        access_token=access_token,
        **kwargs,
    )

    return ret.get("success", False)
