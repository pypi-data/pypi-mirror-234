import functools
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List

import pytest
from hamilton import base

import tests.resources.basic_dag_with_config
from dagworks import driver
from dagworks.api.api_client.models import (
    ProjectOut,
    ProjectOutTags,
    ProjectVersionOut,
    ProjectVersionOutVersionInfo,
    VisibilityFull,
)
from dagworks.api.clients import DAGWorksClient
from dagworks.api.projecttypes import GitInfo
from dagworks.parsing.dagtypes import LogicalDAG
from dagworks.tracking.runs import TrackingState
from dagworks.tracking.trackingtypes import DAGRun, Status, TaskRun


# Yeah, I should probably use a mock library but this is simple and does what I want
def track_calls(fn: Callable):
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        setattr(self, f"{fn.__name__}_latest_kwargs", kwargs)
        setattr(self, f"{fn.__name__}_latest_args", args)
        setattr(self, f"{fn.__name__}_call_count", getattr(fn, "call_count", 0) + 1)
        return fn(self, *args, **kwargs)

    return wrapper


class MockDAGWorksClient(DAGWorksClient):
    """Basic no-op DAGWorks client -- mocks out the above DAGWorks client for testing"""

    @track_calls
    def register_project_version(
        self, project: int, vcs_info: GitInfo, dag: LogicalDAG, name: str, tags: Dict[str, Any]
    ) -> ProjectVersionOut:
        version_info = ProjectVersionOutVersionInfo()
        version_info.additional_properties = dict(
            git_repo="repo", git_hash="hash", git_branch="branch"
        )
        return ProjectVersionOut(
            project=0,
            name=name,
            version_info=version_info,
            version_info_schema=0,
            version_info_type="git",
            dag_pointer="s3://path/to/dag",
            dag_schema_version=0,
            logged_by=0,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            id=0,
            slug="slug",
        )

    @track_calls
    def validate_auth(self):
        pass

    @track_calls
    def ensure_project_exists(self, project_id: int) -> ProjectOut:
        tags = ProjectOutTags()
        tags.additional_properties = {}
        return ProjectOut(
            name="",
            description="",
            tags=ProjectOutTags(),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            owner="elijah",
            permissions=VisibilityFull([], [], [], []),
            documentation=[],
            can_write=True,
        )

    @track_calls
    def log_dag_run(
        self,
        dag_run: DAGRun,
        project_version_id: int,
        config: Dict[str, Any],
        tags: Dict[str, Any],
        inputs: Dict[str, Any],
        outputs: List[str],
    ):
        return 0


def test_tracking_state():
    state = TrackingState("test")
    state.clock_start()
    state.update_task(
        task_name="foo",
        task_run=TaskRun(
            node_name="node_1",
            status=Status.RUNNING,
            start_time=datetime.now(timezone.utc),
        ),
    )
    task = state.task_map["foo"]
    task.end_time = datetime.now(timezone.utc)
    task.status = Status.SUCCESS
    state.update_task(task_name="foo", task_run=task)
    state.clock_end(Status.SUCCESS)
    run = state.get()
    assert len(run.tasks) == 1
    assert run.status == Status.SUCCESS
    assert run.run_id == "test"
    assert run.tasks[0].status == Status.SUCCESS


def test_tracking_auto_initializes():
    dr = driver.Driver(
        {"foo": "baz"},
        tests.resources.basic_dag_with_config,
        project_id=1,
        api_key="foo",
        username="elijah@dagworks.io",
        client_factory=MockDAGWorksClient,
        adapter=base.SimplePythonGraphAdapter(result_builder=base.DictResult()),
        dag_name="test-tracking-auto-initializes",
    )
    dr.execute(final_vars=["c"], inputs={"a": 1})
    assert dr.initialized


def test_tracking_doesnt_break_standard_execution():
    dr = driver.Driver(
        {"foo": "baz"},
        tests.resources.basic_dag_with_config,
        project_id=1,
        api_key="foo",
        username="elijah@dagworks.io",
        client_factory=MockDAGWorksClient,
        adapter=base.SimplePythonGraphAdapter(result_builder=base.DictResult()),
        dag_name="test-tracking-doesnt-break-standard-execution",
    )
    result = dr.execute(final_vars=["c"], inputs={"a": 1})
    assert result["c"] == 6  # 2 + 3 + 1


def test_tracking_apis_get_called():
    """Just tests that the API methods get called
    This method of testing is slightly brittle (kwargs versus args) but will do for now.
    """
    dr = driver.Driver(
        {"foo": "baz"},
        tests.resources.basic_dag_with_config,
        project_id=1,
        api_key="foo",
        username="elijah@dagworks.io",
        client_factory=MockDAGWorksClient,
        adapter=base.SimplePythonGraphAdapter(result_builder=base.DictResult()),
        dag_name="test-tracking-apis-get-called",
    )
    dr.initialize()
    client = dr.client

    assert client.validate_auth_call_count == 1
    assert client.validate_auth_latest_args == ()
    assert client.validate_auth_latest_kwargs == {}

    assert client.ensure_project_exists_call_count == 1
    assert client.ensure_project_exists_latest_args == (1,)
    assert client.ensure_project_exists_latest_kwargs == {}

    dr.execute(final_vars=["c"], inputs={"a": 1})
    assert client.log_dag_run_call_count == 1


class NonSerializable:
    def __str__(self):
        return "non-serializable-string-rep"

    def __repr__(self):
        return self.__str__()


@pytest.mark.parametrize(
    "config,expected",
    [
        ({"foo": "bar"}, {"foo": "bar"}),
        ({"foo": NonSerializable()}, {"foo": "non-serializable-string-rep"}),
        ({"foo": {"bar": "baz"}}, {"foo": {"bar": "baz"}}),
        ({"foo": {"bar": NonSerializable()}}, {"foo": {"bar": "non-serializable-string-rep"}}),
        (None, {}),
    ],
)
def test_json_filter_config(config, expected):
    assert driver.filter_json_dict_to_serializable(config) == expected
