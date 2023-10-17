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

from typing import Dict, Any
import pandas as pd
from hamilton import base
from hamilton import driver
from dagworks.tracking import pandas_col_stats as pcs
from dagworks.tracking import stats

"""Module that houses functions to compute statistics on pandas series/dataframes.
Notes:
 - we should assume pandas v1.0+ so that we have a string type
 - for object types we should :shrug:
"""

adapter = base.SimplePythonGraphAdapter(base.DictResult())
dr = driver.Driver({}, pcs, adapter=adapter)


def _compute_stats(df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """Compute statistics on a pandas dataframe.
    for each c in [dataframe|series]:
        if c is numeric:
            compute numeric stats
        elif c is string:
            compute string stats
        elif c is datetime:
            compute datetime stats
        elif c is object:
            # try to figure out object
        elif c is geometry:
            # try to figure out geometry
    """
    category_types = df.select_dtypes(include=["category"])
    string_types = df.select_dtypes(include=["string"])
    numeric_types = df.select_dtypes(include=["number"])
    bool_types = df.select_dtypes(include=["bool"])
    object_types = df.select_dtypes(include=["object"])
    datetime_types = df.select_dtypes(include=["datetime", "timedelta"])
    unhandled_types = df.select_dtypes(
        exclude=["string", "category", "number", "bool", "object", "datetime", "timedelta"]
    )
    column_order = {col: index for index, col in enumerate(df.columns)}
    stats = {}

    def execute_col(target_output: str, col: pd.Series, name: str, position: int) -> Dict[str, Any]:
        """Get stats on a column."""
        try:
            res = dr.execute(
                [target_output], inputs={"col": col, "name": name, "position": position}
            )
            res = res[target_output].to_dict()
        except Exception:
            # minimum that we want -- ideally we have hamilton handle errors and do best effort.
            res = {"name": name, "pos": position, "data_type": str(col.dtype)}
        return res

    for col in category_types.columns:
        stats[col] = execute_col(
            "category_column_stats", category_types[col], col, column_order[col]
        )
    for col in string_types.columns:
        stats[col] = execute_col("string_column_stats", string_types[col], col, column_order[col])
    for col in numeric_types.columns:
        stats[col] = execute_col("numeric_column_stats", numeric_types[col], col, column_order[col])
    for col in bool_types.columns:
        stats[col] = execute_col("boolean_column_stats", bool_types[col], col, column_order[col])
    for col in datetime_types.columns:
        stats[col] = execute_col(
            "datetime_column_stats", datetime_types[col], col, column_order[col]
        )
    for col in list(object_types.columns) + list(unhandled_types.columns):
        stats[col] = execute_col("unhandled_column_stats", df[col], col, column_order[col])
    return stats


@stats.compute_stats.register
def compute_stats_df(result: pd.DataFrame, node_name: str) -> Dict[str, Any]:
    return {
        "observability_type": "dagworks_describe",
        "observability_value": _compute_stats(result),
        "observability_schema_version": "0.0.3",
    }


@stats.compute_stats.register
def compute_stats_series(result: pd.Series, node_name: str) -> Dict[str, Any]:
    return {
        "observability_type": "dagworks_describe",
        "observability_value": _compute_stats(pd.DataFrame({node_name: result})),
        "observability_schema_version": "0.0.3",
    }


if __name__ == "__main__":
    df = pd.DataFrame(
        {
            # "a": [1, 2, 3, 4, 5],
            # "b": ["a", "b", "c", "d", "e"],
            # "c": [True, False, True, False, True],
            # "d": [1.0, 2.0, 3.0, 4.0, 5.0],
            # "e": pd.Categorical(["a", "b", "c", "d", "e"]),
            # "f": pd.Series(["a", "b", "c", "d", "e"], dtype="string"),
            # "g": pd.Series(["a", "b", "c", "d", "e"], dtype="object"),
            # "h": pd.Series(
            #     ["20221231", None, "20221231", "20221231", "20221231"], dtype="datetime64[ns]"
            # ),
            # "i": pd.Series([None, None, None, None, None], name="a", dtype=np.float64),
            "j": pd.Series(name="a", data=pd.date_range("20230101", "20230105")),
        }
    )
    import pprint

    res = compute_stats_df(df, "df")
    pprint.pprint(res)
    # create a pandas series of type datetime
    s = pd.Series(["20221231"], dtype="datetime64[ns]")
    import json

    json.dumps(res)
