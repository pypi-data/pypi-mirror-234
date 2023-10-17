import collections
from typing import Any, Dict

import pytest

from dagworks.telemetry.telemetry import TrackingClient, UsageTracker


class StoreTrackingClient(TrackingClient):
    def __init__(self):
        self.calls = collections.defaultdict(list)

    def track(self, username: str, event_name: str, params: Dict[str, Any]):
        self.calls[event_name].append((username, params))


@pytest.fixture
def tracker(mocker):
    return mocker.patch("telemetry.global_tracker", UsageTracker(True, StoreTrackingClient()))


def test_telemetry_gets_called():
    tracker = UsageTracker(True, StoreTrackingClient())
    tracker.initialize("test_user", test_property="test_value")
    tracker.track("test_event", {"test_param": "test_value"})
    assert tracker.tracking_client.calls["test_event"] == [
        ("test_user", {"test_param": "test_value", "test_property": "test_value"})
    ]


def test_telemetry_does_not_get_called():
    tracker = UsageTracker(False, StoreTrackingClient())
    tracker.initialize("test_user", test_property="test_value")
    tracker.track("test_event", {"test_param": "test_value"})
    assert tracker.tracking_client.calls["test_event"] == []


def test_telemetry_decorator():
    tracker = UsageTracker(True, StoreTrackingClient())
    tracker.initialize("test_user", test_property="test_value")

    @tracker.track_calls(
        event_name="test_event",
        params_to_capture_raw=["param_to_capture_raw"],
        tracking_generators={
            "param_to_derive_from": [("derived", lambda x: "foo")],
        },
    )
    def to_track(param_to_capture_raw: str, param_to_derive_from: str) -> int:
        return 1

    to_track("a", "b")
    (call,) = tracker.tracking_client.calls["test_event"]
    name, logged_data = call
    assert name == "test_user"
    assert logged_data["param_to_capture_raw"] == "a"
    assert logged_data["derived"] == "foo"
    assert logged_data["test_property"] == "test_value"


def test_telemetry_handles_exceptions():
    tracker = UsageTracker(True, StoreTrackingClient())
    tracker.initialize("test_user", test_property="test_value")

    @tracker.track_calls(
        event_name="test_event",
        params_to_capture_raw=["param_to_capture_raw"],
        tracking_generators={
            "param_to_derive_from": [("derived", lambda x: "foo")],
        },
    )
    def to_track(param_to_capture_raw: str, param_to_derive_from: str) -> int:
        raise ValueError("test")

    with pytest.raises(ValueError):
        to_track("a", "b")
    (call,) = tracker.tracking_client.calls["test_event"]
    name, logged_data = call
    assert name == "test_user"
    assert logged_data["param_to_capture_raw"] == "a"
    assert logged_data["derived"] == "foo"
    assert logged_data["test_property"] == "test_value"
    assert logged_data["success"] is False
    assert "test" in logged_data["error_message"]


def test_telemetry_decorator_with_no_params():
    tracker = UsageTracker(True, StoreTrackingClient())
    tracker.initialize("test_user", test_property="test_value")

    @tracker.track_calls(event_name="test_event")
    def to_track() -> int:
        return 1

    to_track()
    (call,) = tracker.tracking_client.calls["test_event"]
    name, logged_data = call
    assert name == "test_user"
    assert logged_data["test_property"] == "test_value"
