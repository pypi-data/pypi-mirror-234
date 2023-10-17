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

from functools import singledispatch
import json
from typing import Dict, Any


@singledispatch
def compute_stats(result, node_name: str) -> Dict[str, Any]:
    """This is the default implementation for computing stats on a result.

    All other implementations should be registered with the `@compute_stats.register` decorator.

    :param result:
    :param node_name:
    :return:
    """
    return {
        "observability_type": "unsupported",
        "observability_value": {
            "unsupported_type": str(type(result)),
            "action": "reach out to the DAGWorks team to add support for this type.",
        },
        "observability_schema_version": "0.0.1",
    }


@compute_stats.register(str)
@compute_stats.register(int)
@compute_stats.register(float)
@compute_stats.register(bool)
def compute_stats_primitives(result, node_name: str) -> Dict[str, Any]:
    return {
        "observability_type": "primitive",
        "observability_value": {
            "type": str(type(result)),
            "value": result,
        },
        "observability_schema_version": "0.0.1",
    }


@compute_stats.register(dict)
def compute_stats_dict(result: dict, node_name: str) -> Dict[str, Any]:
    try:
        # if it's JSON serializable, take it.
        d = json.dumps(result)
        result_values = json.loads(d)
    except Exception:
        # else just string it -- max 1000 chars.
        result_values = str(result)
        if len(result_values) > 1000:
            result_values = result_values[:1000] + "..."

    return {
        "observability_type": "dict",
        "observability_value": {
            "type": str(type(result)),
            "value": result_values,
        },
        "observability_schema_version": "0.0.2",
    }
