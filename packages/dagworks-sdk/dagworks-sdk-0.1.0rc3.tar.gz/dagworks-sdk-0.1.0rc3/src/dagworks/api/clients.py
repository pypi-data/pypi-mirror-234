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
import dataclasses
import datetime
import logging
import urllib
from typing import Dict, Any, List, Callable, Tuple
from urllib.parse import urlencode

import requests
from requests import HTTPError

from dagworks.api.projecttypes import GitInfo
from dagworks.tracking.utils import make_json_safe

logger = logging.getLogger(__name__)


class ResourceDoesNotExistException(Exception):
    def __init__(self, resource_type: str, resource_id: str):
        message = f"Resource {resource_type} with id {resource_id} does not exist."
        super().__init__(message)


class UnauthorizedException(Exception):
    def __init__(self, path: str, user: str):
        message = f"Unauthorized to access {path}."
        super().__init__(message)


class DAGWorksClient:
    @abc.abstractmethod
    def validate_auth(self):
        """Validates that authentication works against the DW API.
        Quick "phone-home" to ensure that everything is good to go.

        :raises UnauthorizedException: If the user is not authorized to access the DAGWorks API.
        """
        pass

    @abc.abstractmethod
    def project_exists(self, project_id: int) -> bool:
        """Queries whether the project exists

        :param project_id: Project to ensure
        :return: True if the project exists, False if it was created.
        :raises UnauthorizedException: If the user is not authorized to access the DAGWorks API.
        """
        pass

    @abc.abstractmethod
    def register_dag_template_if_not_exists(
            self,
            project_id: int,
            dag_hash: str,
            code_hash: str,
            nodes: List[dict],
            code_artifacts: List[dict],
            name: str,
            config: dict,
            tags: Dict[str, Any],
            code: List[dict],
            vcs_info: GitInfo,  # TODO -- separate this out so we can support more code version types -- just pass it directly to the client
    ):
        """Registers a project version with the DAGWorks API.

        @param project_id: Project to register to
        @param dag_hash: Unique merkel hash of the DAG
        @param code_hash: Unique hash of the code used in the DAG/passed to the driver
        @param nodes: List of node objects
        @param code_artifacts:  List of code artifacts that we associate with this
        @param name: Name of the DAG
        @param config: Config used to create DAG
        @param tags: Tags to associate with the DAG
        @param code: List of tuples of (filename, file contents) for the code
        @param vcs_info: Version control information -- currently this is Git but we will likely add more
        @return: Version ID of the DAG template, for later use
        """
        pass

    @abc.abstractmethod
    def create_and_start_dag_run(
            self,
            dag_template_id: int,
            tags: Dict[str, str],
            inputs: Dict[str, Any],
            outputs: List[str],
    ) -> int:
        """Logs a DAG run to the DAGWorks API.

        :param dag_template_id:
        :param dag_run: DAG run to log
        :param tags: Tags to log with the DAG run
        :param inputs: Inputs used to pass into the DAG
        :param outputs: Outputs used to query the DAG

        :return: Run ID
        """
        pass

    @abc.abstractmethod
    def update_tasks(
            self,
            dag_run_id: int,
            attributes: List[dict],
            task_updates: List[dict],
    ):
        """Updates the tasks + attributes in a DAG run. Does not change the DAG run's status.

        @param dag_run_id: ID of the DAG run
        @param attributes: List of attributes
        @param task_updates:
        @return:
        """

    @abc.abstractmethod
    def log_dag_run_end(
            self,
            dag_run_id: int,
            status: str,
    ):
        """Logs the end of a DAG run.

        @param dag_run_id: ID of the DAG run.
        @param status: status of the DAG run.
        """
        pass


class BasicSynchronousDAGWorksClient(DAGWorksClient):
    def __init__(self, api_key: str, username: str, dw_api_url: str, base_path: str = "/api/v1"):
        """Initializes a DAGWorks client

         project: Project to save to
        :param api_key: API key to save to
        :param username: Username to authenticate against
        :param dw_api_url: API URL for DAGWorks API.
        """
        self.api_key = api_key
        self.username = username
        self.base_url = dw_api_url + base_path

    def _common_headers(self) -> Dict[str, Any]:
        """Yields the common headers for all requests.

        @return: a dictionary of headers.
        """
        return {"x-api-user": self.username, "x-api-key": self.api_key}

    def validate_auth(self):
        logger.debug(f"Validating auth against {self.base_url}/phone_home")
        response = requests.get(f"{self.base_url}/phone_home", headers=self._common_headers())
        try:
            response.raise_for_status()
            logger.debug(f"Successfully validated auth against {self.base_url}/phone_home")
        except HTTPError as e:
            logger.error(f"Failed to validate auth against {self.base_url}/phone_home")
            if response.status_code // 100 == 4:
                raise UnauthorizedException("api/v1/auth/phone_home", self.username) from e
            raise

    def register_code_version_if_not_exists(
            self,
            project_id: int,
            code_hash: str,
            vcs_info: GitInfo,
            slurp_code: Callable[[], Dict[str, str]],
    ) -> int:
        logger.debug(f"Checking if code version {code_hash} exists for project {project_id}")
        response = requests.get(
            f"{self.base_url}/project_versions/exists?project_id={project_id}&code_hash={code_hash}",
            headers=self._common_headers(),
        )
        try:
            response.raise_for_status()
            logger.debug(f"Code version {code_hash} exists for project {project_id}")
            data = response.json()
            exists = data is not None
        except HTTPError as e:
            logger.debug(
                f"Failed to access project version {project_id} when looking for code hash: {code_hash}"
            )
            if response.status_code // 100 == 4:
                raise ResourceDoesNotExistException("code_version", code_hash) from e
            raise

        if exists:
            return data["id"]
        code_slurped = slurp_code()
        code_version_created = requests.post(
            f"{self.base_url}/project_versions?project_id={project_id}",
            headers=self._common_headers(),
            json={
                "code_hash": code_hash,
                "version_info": {
                    "git_hash": vcs_info.commit_hash,
                    "git_repo": vcs_info.repository,
                    "git_branch": vcs_info.branch,
                    "committed": vcs_info.committed,
                },  # TODO -- ensure serializable
                "version_info_type": "git",  # TODO -- wire this through appropriately
                "version_info_schema": 1,  # TODO -- wire this through appropriately
                "code_log": {"files": code_slurped},
            },
        )
        try:
            code_version_created.raise_for_status()
            logger.debug(f"Created code version {code_hash} for project {project_id}")
            return code_version_created.json()["id"]
        except HTTPError:
            logger.exception(
                f"Failed to create code version {code_hash} for project {project_id}. "
                f"Error was: {code_version_created.text}"
            )
            raise

    def project_exists(self, project_id: int) -> bool:
        logger.debug(f"Checking if project {project_id} exists")
        response = requests.get(
            f"{self.base_url}/projects/{project_id}", headers=self._common_headers()
        )
        try:
            response.raise_for_status()
            logger.debug(f"Project {project_id} exists")
            return True
        except HTTPError as e:
            logger.debug(f"Project {project_id} does not exist")
            if response.status_code // 100 == 4:
                raise ResourceDoesNotExistException("project", str(project_id)) from e
            raise

    def register_dag_template_if_not_exists(
            self,
            project_id: int,
            dag_hash: str,
            code_hash: str,
            nodes: List[dict],
            code_artifacts: List[dict],
            name: str,
            config: dict,
            tags: Dict[str, Any],
            code: List[dict],
            vcs_info: GitInfo,
    ) -> int:
        logger.debug(f"Checking if DAG template {dag_hash} exists for code hash: {code_hash}, dag hash: {dag_hash}, project {project_id}")
        params = urlencode(
            {
                "project_id": project_id,
                "dag_hash": dag_hash,
                "code_hash": code_hash,
                "dag_name": name,
            }
        )
        response = requests.get(
            f"{self.base_url}/dag_templates/exists/?dag_hash={dag_hash}&{params}",
            headers=self._common_headers(),
        )
        response.raise_for_status()
        logger.debug(f"DAG template {dag_hash} exists for project {project_id}")
        data = response.json()
        exists = data is not None
        if exists:
            return data["id"]
        dag_template_created = requests.post(
            f"{self.base_url}/dag_templates?project_id={project_id}",
            json={
                "name": name,
                "template_type": "HAMILTON",
                "config": make_json_safe(config),
                "dag_hash": dag_hash,
                "tags": make_json_safe(tags),
                "nodes": nodes,
                "code_artifacts": code_artifacts,
                "code_log": {"files": code},
                "code_hash": code_hash,
                # Support more code version types
                "code_version_info_type": "git",
                "code_version_info": {
                    "git_hash": vcs_info.commit_hash,
                    "git_repo": vcs_info.repository,
                    "git_branch": vcs_info.branch,
                },
                "code_version_info_schema": 1,
            },
            headers=self._common_headers(),
        )
        try:
            dag_template_created.raise_for_status()
            logger.debug(f"Created DAG template {dag_hash} for project {project_id}")
            return dag_template_created.json()["id"]
        except HTTPError:
            logger.exception(
                f"Failed to create DAG template {dag_hash} for project {project_id}. Error: {dag_template_created.text}"
            )
            raise

    def create_and_start_dag_run(
            self, dag_template_id: int, tags: Dict[str, str], inputs: Dict[str, Any], outputs: List[str]
    ) -> int:
        logger.debug(f"Creating DAG run for project version {dag_template_id}")
        response = requests.post(
            f"{self.base_url}/dag_runs?dag_template_id={dag_template_id}",
            headers=self._common_headers(),
            json=make_json_safe(
                {
                    "run_start_time": datetime.datetime.now(),  # TODO -- ensure serializable
                    "tags": tags,  # TODO -- ensure serializable
                    "inputs": inputs,  # TODO -- ensure serializable
                    "outputs": outputs,
                    "run_status": "RUNNING",
                }
            ),
        )
        try:
            response.raise_for_status()
            logger.debug(f"Created DAG run for project version {dag_template_id}")
            return response.json()["id"]
        except HTTPError:
            logger.exception(
                f"Failed to create DAG run for project version {dag_template_id}. Error: {response.text}"
            )
            raise

    def update_tasks(self, dag_run_id: int, attributes: List[dict], task_updates: List[dict]):
        logger.debug(
            f"Updating tasks for DAG run {dag_run_id} with {len(attributes)} "
            f"attributes and {len(task_updates)} task updates"
        )
        response = requests.put(
            f"{self.base_url}/dag_runs_bulk?dag_run_id={dag_run_id}",
            json={
                "attributes": make_json_safe(attributes),
                "task_updates": make_json_safe(task_updates),
            },
            headers=self._common_headers(),
        )
        try:
            response.raise_for_status()
            logger.debug(f"Updated tasks for DAG run {dag_run_id}")
        except HTTPError:
            logger.exception(f"Failed to update tasks for DAG run {dag_run_id}")
            raise

    def log_dag_run_end(self, dag_run_id: int, status: str):
        logger.debug(f"Logging end of DAG run {dag_run_id} with status {status}")
        response = requests.put(
            f"{self.base_url}/dag_runs/{dag_run_id}/",
            json=make_json_safe({"run_status": status, "run_end_time": datetime.datetime.now()}),
            headers=self._common_headers(),
        )
        try:
            response.raise_for_status()
            logger.debug(f"Logged end of DAG run {dag_run_id}")
        except HTTPError:
            logger.exception(f"Failed to log end of DAG run {dag_run_id}. Error: {response.text}")
            raise
