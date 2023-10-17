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
from typing import Any, Dict, List, Optional, Tuple


@dataclasses.dataclass
class PythonType:
    """Represents a python type"""

    typeName: str


@dataclasses.dataclass
class Dependency:
    """Represents a dependency of a node"""

    type: PythonType
    name: str
    dependencyType: str  # We should be able to use an enum...


@dataclasses.dataclass
class HamiltonFunction:
    """Represents a python function that could produce to multiple nodes"""

    name: str
    module: List[str]
    contents: str
    lineStart: int
    lineEnd: int
    file: str


@dataclasses.dataclass
class HamiltonNode:
    """Represents a hamilton Node -- stores a pointer to  function"""

    name: str
    functionIdentifier: Tuple[str, ...]  # [...module_path, fn_name]
    dependencies: Dict[str, Dependency]
    documentation: Optional[str]  # broke here, made it optional.
    tags: Dict[str, Any]
    namespace: Tuple[str, ...]
    userDefined: bool
    returnType: PythonType

    def unique_name(self) -> str:
        return ".".join(self.functionIdentifier) + "." + self.name


@dataclasses.dataclass
class LogicalDAG:
    """Represents a logical DAG"""

    functions: List[HamiltonFunction]
    nodes: List[HamiltonNode]
    config: Optional[Dict[str, Any]]
    DAGRoot: List[str]
    schema_version = 0
