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

import collections
import graphlib
import inspect
import itertools
import os
from types import ModuleType
from typing import Any, Callable, Dict, List, Optional, Tuple

import hamilton.graph as hamilton_graph
import hamilton.node as hamilton_node
from hamilton import base, graph

from dagworks.parsing.dagtypes import (
    Dependency,
    HamiltonFunction,
    HamiltonNode,
    LogicalDAG,
    PythonType,
)

"""
Parses a DAG. Note that this allows for parsing a "superset" using configurable
function graph. This specifically means that we return multiple node values per name.

We should also be able to run with a config, which will return one node per name.

We can then diff the nodes.

The unique key of the node is the name of the function concatenated with the name of the node.
"""


def _get_fn_identifier(node: hamilton_node.Node) -> Tuple[str]:
    """Gets the function identifier for a node.
    :param node: Node to get the identifier for
    :return: A list of strings representing the identifier
    """
    fn = node.originating_functions[0] if node.originating_functions else None
    if fn is None:
        return ()
    return tuple(fn.__module__.split(".") + [fn.__qualname__])


def convert_node(node: hamilton_node.Node) -> HamiltonNode:
    """Converts a Hamilton node to our intermediate representation.
    Note that this assumes that hit has the original_function attribute.
    We plan to add this into open-source.
    :param node: Node to convert
    :return: A dataclass representing that node but readable externally.
    """
    dependencies = {}
    for input_, (python_type, dep_type) in node.input_types.items():
        dependencies[input_] = Dependency(
            type=PythonType(typeName=str(python_type)),
            # we need to figure out a better way of represeting these...
            name=input_,
            dependencyType=dep_type.value,
        )

    return HamiltonNode(
        name=node.name,
        functionIdentifier=_get_fn_identifier(node),
        dependencies=dependencies,
        documentation=node.documentation,
        tags=node.tags,
        namespace=node.namespace,
        userDefined=node.user_defined,
        returnType=PythonType(typeName=str(node.type)),
    )


def convert_function(fn: Callable, repo_base: str) -> HamiltonFunction:
    """Converts a function (actual function pointer) into a format we can send over the wire.
    :param fn: Function to convert.
    :return: Intermediate representation of the function
    """
    source_lines, line_start = inspect.getsourcelines(fn)
    return HamiltonFunction(
        name=fn.__qualname__,
        # This is a little hacky as we change the name with the decorator, but __qualname__
        # remains the same TODO -- determine whether the name/qualname is the right one to use,
        # and if we should/should not be changing it in the decorator
        module=fn.__module__.split("."),
        contents="".join(source_lines),  # TODO -- verify if this includes decorator
        lineStart=line_start,
        lineEnd=line_start + len(source_lines),
        file=os.path.relpath(inspect.getfile(fn), repo_base),
    )


def gather_functions(*modules: ModuleType) -> List[Callable]:
    """Gathers functions from modules
    :param modules: Modules to gather functions from
    :return: A list of function objects
    """
    all_functions = []
    for module in modules:
        all_functions.extend([fn for _, fn in hamilton_graph.find_functions(module)])
    return all_functions


def topologically_sort_nodes(nodes: List[HamiltonNode]) -> List[HamiltonNode]:
    """Topologically sorts nodes for ease of use on the client side.

    Note that node names might not be unique -- so we have to handle multiple implementations...

    :param nodes: Nodes to sort
    :return: A list of nodes in topological order
    """
    # Group by possible implementations
    node_implementations = collections.defaultdict(list)
    for node in nodes:
        node_implementations[node.name].append(node)

    graph = {
        node_name: set(itertools.chain(*[list(n.dependencies.keys()) for n in implementations]))
        for node_name, implementations in node_implementations.items()
    }
    ts = graphlib.TopologicalSorter(graph)
    out = []
    for node in ts.static_order():
        out.extend(node_implementations[node])
    return out


def gather_nodes(
    *modules: ModuleType, config: Optional[Dict[str, Any]]
) -> List[hamilton_node.Node]:
    """Gathers all nodes from a set of modules
    :param modules: Modules to look through
    :param config: Config to create the DAG from
    :return: A list of Hamilton nodes (each one of which has a unique name)
    """
    dag = graph.create_function_graph(
        *modules, config=config, adapter=base.SimplePythonGraphAdapter(base.DictResult())
    )
    return list(itertools.chain(dag.values()))


# def parse_dag(*modules: ModuleType, repo_base: str, config: Dict[str, Any]) -> LogicalDAG:
#     """Parses a Hamilton DAG from a repository
#     TODO -- add optional "exclude" from this?
#     :param dag_roots: Root of the DAG -- where to look recursively for python modules
#     :param config: Configuration to use to parse the DAG. TBD on exactly how this should work
#     later on, but for now I'm requiring one.
#     :param exclude_modules: Modules to exclude from generating the DAG. glob of module names.
#     :return: A logical DAG, parsed and ready to be visualized/whatnot
#     """
#     functions = gather_functions(*modules)
#     nodes = gather_nodes(*modules, config=config)
#     functions_converted = [convert_function(function, repo_base) for function in functions]
#     nodes_converted = [convert_node(node) for node in nodes]
#     return LogicalDAG(
#         functions=functions_converted,
#         nodes=topologically_sort_nodes(nodes_converted),
#         config=None,
#         DAGRoot=["TODO", "implement", "me"],
#     )


def parse_dag(function_graph: graph.FunctionGraph, repo_base):
    nodes = list(function_graph.nodes.values())
    functions = set()
    for node_ in nodes:
        functions.update(node_.originating_functions if node_.originating_functions else [])
    functions_converted = [convert_function(function, repo_base) for function in functions]
    nodes_converted = [convert_node(node) for node in nodes]
    return LogicalDAG(
        functions=functions_converted,
        nodes=topologically_sort_nodes(nodes_converted),
        config=function_graph.config,
        DAGRoot=["TODO", "implement", "me"],
    )
