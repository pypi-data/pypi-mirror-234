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

import abc
import functools
import inspect
import logging
import os
import time
from typing import Any, Callable, Dict, List, Tuple

import posthog
from hamilton import base

# This is OK to put in plaintext, publicly, as it is a write-only API key
POSTHOG_API_KEY = "phc_uXYDLLLnTxiCf91IGa2vdNqjH4nU9eJ9cROlmg7kUDH"
POSTHOG_URL = "https://app.posthog.com"

posthog.project_api_key = POSTHOG_API_KEY
posthog.host = POSTHOG_URL

logger = logging.getLogger(__name__)


def get_adapter_representation(adapter: base.HamiltonGraphAdapter) -> str:
    """Get the representation of the adapter.

    :param adapter: The adapter to get the representation of.
    :return: The representation of the adapter.
    """
    return f"{adapter.__class__.__module__}.{adapter.__class__.__name__}"


def get_event_name(fn: Callable) -> str:
    """Get the event name for the function.

    :param fn:
    :return:
    """
    return f"{fn.__module__}.{fn.__name__}"


def serialize_error(error: Exception) -> str:
    """Serialize an error.

    TODO -- grab and sanitize the traceback like we do in hamilton...

    :param error:
    :return:
    """
    return str(error)


class TrackingClient(abc.ABC):
    def track(self, username: str, event_name: str, params: Dict[str, Any]):
        """Track an event.

        :param username: Name of the user calling this.
        :param event_name: Name of the event
        :param params: Parameters for the event.
        """
        pass


class PostHogTrackingClient(TrackingClient):
    def track(self, username: str, event_name: str, params: Dict[str, Any]):
        """Tracks an event to posthog

        :param username: Unique user ID
        :param event_name: Name of the event
        :param params: Parameters for the event
        """
        posthog.capture(username, event_name + " called", params)


class UsageTracker:
    def __init__(self, enabled: bool, tracking_client: TrackingClient):
        """Initializes a UsageTracker. This delegates to a tracking client.

        :param enabled: Whether to enable tracking.
        :param tracking_client: The tracking client to use.
        """
        self.common_properties = None
        self.username = None
        self.initialized = False
        self.enabled = enabled
        self.tracking_client = tracking_client

    def initialize(self, username: str, **common_properties: str):
        """Initializes the tracking client with some
        common properties and a username.

        :param username: Username to track with
        :param common_properties: Properties attached to every request
        """
        self.username = username
        self.common_properties = common_properties
        self.initialized = True

    def track(self, event_name: str, params: Dict[str, Any]):
        """Tracks an event.

        :param event_name: Name of the event to track
        :param params: Parameters to track with
        """
        if not self.initialized:
            raise ValueError("UsageTracker has not been initialized")
        if self.enabled:
            logger.debug(f"tracking {event_name}", {**params, **self.common_properties})
            self.tracking_client.track(
                self.username, event_name, {**params, **self.common_properties}
            )

    def track_calls(
        self,
        *,
        event_name: str = None,
        params_to_capture_raw: List[str] = None,
        tracking_generators: Dict[str, List[Tuple[str, Callable[[Any], Any]]]] = None,
    ):
        """Decorator to track calls to a function.

        :param event_name: Event name to capture
        :param params_to_capture_raw: Parameters to capture raw
        :param convert_param: Functions to stringify parameters. Takes the form of a dict of
        parameter name to a list of functions to apply to the parameter.
        :return: The decorator.
        """
        if tracking_generators is None:
            tracking_generators = {}
        if params_to_capture_raw is None:
            params_to_capture_raw = []

        def decorator(fn):
            @functools.wraps(fn)
            def wrapper(*args, **kwargs):
                event_name_to_log = event_name if event_name is not None else get_event_name(fn)
                if self.enabled:
                    time_start = time.time()
                    success = True
                    error = None
                    bound_arguments = inspect.signature(fn).bind(*args, **kwargs).arguments
                    params_to_log = {
                        key: value
                        for key, value in bound_arguments.items()
                        if key in params_to_capture_raw
                    }
                    for key, param_derivers in tracking_generators.items():
                        for param_deriver in param_derivers:
                            to_write, param_deriver = param_deriver
                            if key in bound_arguments:
                                # This allows us to deal with default values
                                params_to_log[to_write] = param_deriver(bound_arguments[key])
                    try:
                        out = fn(*args, **kwargs)
                        return out
                    except Exception as e:
                        success = False
                        error = serialize_error(e)
                        raise e
                    finally:
                        time_end = time.time()
                        params_to_log["success"] = success
                        params_to_log["error_message"] = error
                        params_to_log["time_elapsed"] = time_end - time_start
                        self.track(event_name_to_log, params_to_log)

                return fn(*args, **kwargs)

            return wrapper

        return decorator


def should_track() -> bool:
    """Tells whether we should use tracking.
    This must be called before anything

    :return:
    """
    if os.environ.get("DW_DISABLE_TRACKING", "false").lower() == "true":
        return False
    return True


posthog.api_key = "foo"
global_tracker = UsageTracker(should_track(), tracking_client=PostHogTrackingClient())


def set_tracking(tracking: bool):
    """Toggles tracking.

    :param tracking:
    :return:
    """
    global_tracker.enabled = tracking


def disable_tracking():
    set_tracking(False)
