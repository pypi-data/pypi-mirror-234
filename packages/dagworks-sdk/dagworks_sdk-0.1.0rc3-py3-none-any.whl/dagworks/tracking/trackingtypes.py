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

import dataclasses
import enum
from datetime import datetime
from typing import List, Optional, Type


class Status(enum.Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    RUNNING = "RUNNING"
    UNINITIALIZED = "UNINITIALIZED"


@dataclasses.dataclass
class TaskRun:
    node_name: str
    status: Status = dataclasses.field(default_factory=lambda: Status.UNINITIALIZED)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    result_type: Optional[Type[Type]] = None
    # TODO -- determine the best kind of result data here
    result_summary: Optional[dict] = None
    error: Optional[List[str]] = None  # Serialization of error, broken into lines...

    def to_dict(self):
        return {
            "node_name": self.node_name,
            "status": self.status.value,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "result_type": str(self.result_type),  # TODO -- fix this serialization up
            "result_summary": self.result_summary,  # TODO -- fix this serialization up
            "error": self.error,
        }


@dataclasses.dataclass
class DAGRun:
    """Represents a DAG run"""

    run_id: str
    status: Status
    tasks: List[TaskRun]
    start_time: datetime
    end_time: datetime
    schema_version: int
