"""
These are the functions available when importing __archimedes__.
"""

from archimedes.auth import NoneAuth, get_auth
from archimedes.configuration import ArchimedesConstants  # config
from archimedes.data.api import rk_within_day
from archimedes.data.api.forecast import (
    forecast_diff,
    forecast_get,
    forecast_get_by_ref_time_interval,
    forecast_list_ref_times,
)
from archimedes.data.api.intraday import get_intraday_trades
from archimedes.data.api.metadata import (
    list_ids,
    list_ids_expanded,
    list_prediction_ids,
    list_series_price_areas,
)
from archimedes.data.api.observation import get, get_latest
from archimedes.data.api.prediction import (
    get_latest_predictions_ref_dt,
    get_predictions,
    get_predictions_ref_dts,
    store_prediction,
    store_predictions,
)
from archimedes.data.api.rk_within_day import (
    comparison_by_price as rk_comparison_by_price,
)
from archimedes.data.api.rk_within_day import directions as rk_within_day_directions
from archimedes.data.api.rk_within_day import (
    distributions as rk_within_day_distributions,
)
from archimedes.data.api.rk_within_day import (
    large_down_fps as rk_within_day_large_down_fps,
)
from archimedes.data.api.rk_within_day import large_up_fps as rk_within_day_large_up_fps
from archimedes.data.api.umm import (
    umm_get,
    umm_get_area_codes,
    umm_get_by_id,
    umm_get_series_list,
    umm_get_summary,
)
from archimedes.utils import compact_print, environ, full_print
from archimedes.version import __version__

__all__ = [
    "__version__",
    "ArchimedesConstants",
    "get_auth",
    "NoneAuth",
    "compact_print",
    "full_print",
    "environ",
    "get",
    "get_intraday_trades",
    "get_latest",
    "list_ids",
    "list_ids_expanded",
    "list_series_price_areas",
    "get_predictions",
    "get_predictions_ref_dts",
    "list_prediction_ids",
    "store_prediction",
    "store_predictions",
    "forecast_list_ref_times",
    "forecast_get",
    "forecast_diff",
    "forecast_get_by_ref_time_interval",
    "rk_within_day_directions",
    "rk_within_day_large_up_fps",
    "rk_within_day_large_down_fps",
    "rk_within_day_distributions",
    "rk_comparison_by_price",
    "rk_within_day",
    "umm_get_series_list",
    "umm_get_area_codes",
    "umm_get_summary",
    "umm_get",
    "umm_get_by_id",
]
