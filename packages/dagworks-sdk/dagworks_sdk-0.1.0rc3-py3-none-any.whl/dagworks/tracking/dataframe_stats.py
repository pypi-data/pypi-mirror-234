# Copyright (C) 2023-Present DAGWorks Inc.
#
# For full terms email support@dagworks.io.
#
# This software and associated documentation files (the "Software") may only be
# used in production, if you (and any entity that you represent) have agreed to,
# and are in compliance with, the DAGWorks Enterprise Terms of Service, available
# via email (support@dagworks.io) (the "Enterprise Terms"), or other
# agreement governing the use of the Software, as agreed by you and DAGWorks,
# and otherwise have a valid DAGWorks Enterprise license for the
# correct number of seats and usage volume.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import Union, Dict, Any
from dataclasses import dataclass
import numpy as np
import pandas as pd


def type_converter(obj: Any) -> Any:
    # obj = getattr(self, key)
    if isinstance(obj, np.ndarray):
        result = obj.tolist()
    elif isinstance(obj, np.integer):
        result = int(obj)
    elif isinstance(obj, np.floating):
        result = float(obj)
    elif isinstance(obj, np.complex_):
        result = complex(obj)
    elif isinstance(obj, dict):
        result = {}
        for k, v in obj.items():
            result[k] = type_converter(v)
    else:
        result = obj
    # nans
    is_null = pd.isnull(result)
    # this ensures we skip evaluating the truthiness of lists/series/arrays
    if isinstance(is_null, bool) and is_null:
        return None
    return result


@dataclass
class BaseColumnStatistics:
    name: str  # Name of the column
    pos: int  # Position in the dataframe. Series will mean 0 position.
    data_type: str
    count: int
    missing: float

    def to_dict(self) -> dict:
        result = {}
        for key, obj in self.__dict__.items():
            result[key] = type_converter(obj)
        return result


@dataclass
class UnhandledColumnStatistics(BaseColumnStatistics):
    base_data_type: str = "unhandled"
    pass


@dataclass
class BooleanColumnStatistics(BaseColumnStatistics):
    """Simplified numeric column statistics."""

    zeros: int
    base_data_type: str = "boolean"


@dataclass
class NumericColumnStatistics(BaseColumnStatistics):
    """Inspired by TFDV's ColumnStatistics proto."""

    zeros: int
    min: Union[float, int]
    max: Union[float, int]
    mean: float
    std: float
    quantiles: Dict[float, float]
    histogram: Dict[str, int]
    base_data_type: str = "numeric"


@dataclass
class DatetimeColumnStatistics(NumericColumnStatistics):
    """Placeholder class."""

    base_data_type: str = "datetime"


@dataclass
class CategoryColumnStatistics(BaseColumnStatistics):
    """Inspired by TFDV's ColumnStatistics proto."""

    empty: int
    domain: Dict[str, int]
    top_value: str
    top_freq: int
    unique: int
    base_data_type: str = "category"


@dataclass
class StringColumnStatistics(BaseColumnStatistics):
    """Similar to category, but we don't do domain, top_value, top_freq, unique."""

    avg_str_len: float
    std_str_len: float
    empty: int
    base_data_type: str = "str"
