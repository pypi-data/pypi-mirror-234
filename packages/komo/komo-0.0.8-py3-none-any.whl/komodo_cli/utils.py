import json
import os
import sys
from typing import Dict, List, Union
from uuid import getnode

import click
import docker
import git
import requests
import yaml
from loguru import logger
from vyper import Vyper

import komodo_cli.printing as printing
from komodo_cli.types import (
    Backend,
    ClientException,
    Job,
    JobNotFoundException,
    JobStatus,
    Machine,
    Resource,
)

API_BASE_URL = os.environ.get(
    "KOMODO_API_URL", "https://komodo-api-wprtgx67oa-uc.a.run.app"
)


class NoCredentialsException(Exception):
    pass


LOCAL_STATUS_MAPPING = {
    "cancelling": JobStatus.CANCELLING,
    "cancelled": JobStatus.CANCELLED,
    "created": JobStatus.PENDING,
    "running": JobStatus.RUNNING,
    "paused": JobStatus.RUNNING,
    "restarting": JobStatus.PENDING,
    "removing": JobStatus.FINISHED,
    "exited": JobStatus.FINISHED,
    "dead": JobStatus.FINISHED,
}


class APIClient:
    # TODO: Support API key from a KOMODO_API_KEY env variable
    def __init__(
        self,
        api_key=None,
        username=None,
        password=None,
    ):
        self.api_base_url = API_BASE_URL
        self.username = username
        self.password = password

        if api_key is None:
            if username is None or password is None:
                raise NoCredentialsException(
                    "API key or username & password are required for authentication."
                )
            else:
                try:
                    self.access_token, self.token_type = self.create_token()
                except Exception as e:
                    raise e
        else:
            self.access_token = api_key
            self.token_type = "Bearer"

    @classmethod
    def api_request(
        cls,
        method: str,
        url: str,
        headers: Dict = None,
        files: Dict = None,
        data: Dict = None,
    ) -> Union[Dict, List]:  # Not using | for > 1 return type for < Py 3.10 compat
        # Generic way to make HTTP requests w/ standard error handling
        # TODO: debug-level info logs?
        response = requests.request(
            method,
            url,
            headers=headers,
            files=files,
            data=data,
        )
        response.raise_for_status()

        retval = response.json()
        return retval

    @classmethod
    def register(cls, email: str, password: str):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        payload = json.dumps(
            {
                "email": email,
                "password": password,
            },
        )

        cls.api_request(
            "POST",
            f"{API_BASE_URL}/api/v1/auth/register",
            headers=headers,
            data=payload,
        )

    def create_token(self):
        headers = {
            # requests won't add a boundary if this header is set when you pass files=
            # 'Content-Type': 'multipart/form-data',
        }

        files = {
            "username": (None, self.username),
            "password": (None, self.password),
        }

        auth = self.api_request(
            "POST",
            f"{self.api_base_url}/api/v1/auth/token/login",
            headers=headers,
            files=files,
        )

        return auth["access_token"], auth["token_type"]

    def get_all_tokens(self):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"{self.token_type} {self.access_token}",
        }

        tokens = self.api_request(
            "GET",
            f"{self.api_base_url}/api/v1/auth/token/list",
            headers=headers,
        )

        return tokens

    def delete_token(self, token: str):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"{self.token_type} {self.access_token}",
        }

        self.api_request(
            "DELETE",
            f"{self.api_base_url}/api/v1/auth/token/{token}",
            headers=headers,
        )

    def create_backend(self, name: str, type: str, config: dict) -> Backend:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"{self.token_type} {self.access_token}",
        }

        payload = json.dumps(
            {
                "name": name,
                "type": type,
                "config": config,
            },
        )

        backend_json = self.api_request(
            "POST",
            f"{self.api_base_url}/api/v1/backends",
            headers=headers,
            data=payload,
        )

        backend = Backend.from_dict(backend_json)
        return backend

    def list_backends(self) -> List[Backend]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"{self.token_type} {self.access_token}",
        }

        backend_jsons = self.api_request(
            "GET",
            f"{self.api_base_url}/api/v1/backends",
            headers=headers,
        )

        backends = [Backend.from_dict(b) for b in backend_jsons]
        return backends

    def get_backend(self, backend_name: str) -> Backend:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"{self.token_type} {self.access_token}",
        }

        backend_json = self.api_request(
            "GET",
            f"{self.api_base_url}/api/v1/backends/{backend_name}",
            headers=headers,
        )

        backend = Backend.from_dict(backend_json)
        return backend

    def delete_backend(self, name: str, force: bool):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"{self.token_type} {self.access_token}",
        }

        self.api_request(
            "DELETE",
            f"{self.api_base_url}/api/v1/backends/{name}?force={str(force).lower()}",
            headers=headers,
        )

    def create_backend_resource(
        self, backend_name: str, resource_name: str, resource_config: dict
    ) -> Resource:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"{self.token_type} {self.access_token}",
        }

        payload = json.dumps(
            {
                "name": resource_name,
                "config": resource_config,
            },
        )

        resource_json = self.api_request(
            "POST",
            f"{self.api_base_url}/api/v1/backends/{backend_name}/resources",
            headers=headers,
            data=payload,
        )

        resource = Resource.from_dict(resource_json)
        return resource

    def delete_backend_resource(self, backend_name: str, resource_name: str):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"{self.token_type} {self.access_token}",
        }

        self.api_request(
            "DELETE",
            f"{self.api_base_url}/api/v1/backends/{backend_name}/resources/{resource_name}",
            headers=headers,
        )

    def create_job(
        self,
        backend_name: str,
        command: List[str],
        num_nodes: int,
        image: str,
        env: Dict,
        mounts: List,
        workdir: str,
        resource_name: str,
    ) -> Job:
        payload = json.dumps(
            {
                "backend_name": backend_name,
                "command": command,
                "num_nodes": num_nodes,
                "image": image,
                "env": env,
                "mounts": mounts,
                "workdir": workdir,
                "resource_name": resource_name,
            }
        )

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"{self.token_type} {self.access_token}",
        }

        job_json = self.api_request(
            "POST",
            f"{self.api_base_url}/api/v1/jobs",
            headers=headers,
            data=payload,
        )
        job_json["status"] = JobStatus(job_json["status"])
        job = Job.from_dict(job_json)

        return job

    def create_machine(
        self,
        machine_name: str,
        backend_name: str,
        image: str,
        env: Dict,
        mounts: List,
        workdir: str,
        resource_name: str,
    ) -> Job:
        payload = json.dumps(
            {
                "name": machine_name,
                "backend_name": backend_name,
                "image": image,
                "env": env,
                "mounts": mounts,
                "workdir": workdir,
                "resource_name": resource_name,
            }
        )

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"{self.token_type} {self.access_token}",
        }

        machine_json = self.api_request(
            "POST",
            f"{self.api_base_url}/api/v1/machines",
            headers=headers,
            data=payload,
        )

        machine_json["status"] = JobStatus(machine_json["status"])
        machine = Machine.from_dict(machine_json)

        return machine

    def update_job(
        self,
        job_id: str,
        status: JobStatus,
        backend_job_id: str = None,
    ):
        if status == JobStatus.NOT_AVAILABLE_CURRENT_COMPUTER:
            # this is just a client-side status
            status = None
        payload = json.dumps(
            {
                "status": (status.value if status else None),
                "backend_job_id": backend_job_id,
            }
        )
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"{self.token_type} {self.access_token}",
        }

        response = self.api_request(
            "PUT",
            f"{self.api_base_url}/api/v1/jobs/{job_id}",
            headers=headers,
            data=payload,
        )

        return response

    def update_machine(
        self,
        machine_name: str,
        status: JobStatus,
        backend_job_id: str = None,
    ):
        if status == JobStatus.NOT_AVAILABLE_CURRENT_COMPUTER:
            # this is just a client-side status
            status = None
        payload = json.dumps(
            {
                "status": (status.value if status else None),
                "backend_job_id": backend_job_id,
            }
        )
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"{self.token_type} {self.access_token}",
        }

        response = self.api_request(
            "PUT",
            f"{self.api_base_url}/api/v1/machines/{machine_name}",
            headers=headers,
            data=payload,
        )

        return response

    def delete_job(self, job_id: str, force: bool = False):
        job = self.get_job(job_id)
        if job.status == JobStatus.NOT_AVAILABLE_CURRENT_COMPUTER:
            raise ClientException(
                f"Cannot delete local job {job_id} because it was not created on this computer"
            )

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"{self.token_type} {self.access_token}",
        }

        response = self.api_request(
            "DELETE",
            f"{self.api_base_url}/api/v1/jobs/{job_id}?force={str(force).lower()}",
            headers=headers,
        )

        return response

    def cancel_job(self, job_id: str):
        job = self.get_job(job_id)
        if job.status == JobStatus.NOT_AVAILABLE_CURRENT_COMPUTER:
            raise ClientException(
                f"Cannot delete local job {job_id} because it was not created on this computer"
            )

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"{self.token_type} {self.access_token}",
        }

        response = self.api_request(
            "POST",
            f"{self.api_base_url}/api/v1/jobs/cancel/{job_id}",
            headers=headers,
        )

        return response

    def delete_machine(self, machine_name: str, force: bool = False):
        machine = self.get_machine(machine_name)
        if machine.status == JobStatus.NOT_AVAILABLE_CURRENT_COMPUTER:
            raise ClientException(
                f"Cannot delete local machine {machine_name} because it was not created on this computer"
            )

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"{self.token_type} {self.access_token}",
        }

        response = self.api_request(
            "DELETE",
            f"{self.api_base_url}/api/v1/machines/{machine_name}?force={force}",
            headers=headers,
        )

        return response

    def _update_local_job_status(self, client, job):
        backend_job_id = job.backend_job_id
        if ":" in backend_job_id:
            mac_address, docker_container_id = backend_job_id.split(":")
        else:
            # backwards compatibility
            docker_container_id = backend_job_id
            mac_address = None

        # TODO: error handling
        if mac_address and str(getnode()) != mac_address:
            status = JobStatus.NOT_AVAILABLE_CURRENT_COMPUTER
        else:
            try:
                container = client.containers.get(docker_container_id)
                status = LOCAL_STATUS_MAPPING[container.status]
            except docker.errors.NotFound:
                status = JobStatus.NOT_FOUND
            except docker.errors.NullResource:
                status = JobStatus.ERROR

        # TODO: make this async
        self.update_job(
            job.id,
            status,
        )
        job.status = status

    def _update_local_machine_status(self, client, machine):
        backend_job_id = machine.backend_job_id

        if ":" in backend_job_id:
            mac_address, docker_container_id = backend_job_id.split(":")
        else:
            # backwards compatibility
            docker_container_id = backend_job_id
            mac_address = None

        if mac_address and str(getnode()) != mac_address:
            status = JobStatus.NOT_AVAILABLE_CURRENT_COMPUTER
        else:
            try:
                container = client.containers.get(docker_container_id)
                status = LOCAL_STATUS_MAPPING[container.status]
            except docker.errors.NotFound:
                status = JobStatus.NOT_FOUND
            except docker.errors.NullResource:
                status = JobStatus.ERROR
        # TODO: make this async
        self.update_machine(
            machine.name,
            status,
        )
        machine.status = status

    def list_jobs(self, skip: int = 0, limit: int = 10):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"{self.token_type} {self.access_token}",
        }

        response = self.api_request(
            "POST",
            f"{self.api_base_url}/api/v1/jobs/all?skip={skip}&limit={limit}",
            headers=headers,
        )

        backends = self.list_backends()
        backends = {b.name: b for b in backends}

        jobs: List[Job] = []
        client = None
        for job_json in response:
            job = Job.from_dict(job_json)

            backend_name = job.backend_name
            backend_type = backends[backend_name].type
            if backend_type == "local":
                if client is None:
                    client = docker.from_env()
                self._update_local_job_status(client, job)

            jobs.append(job)

        return jobs

    def list_machines(self):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"{self.token_type} {self.access_token}",
        }

        response = self.api_request(
            "POST",
            f"{self.api_base_url}/api/v1/machines/all",
            headers=headers,
        )

        backends = self.list_backends()
        backends = {b.name: b for b in backends}

        machines: List[Machine] = []
        client = None
        for machine_json in response:
            machine = Machine.from_dict(machine_json)

            backend_name = machine.backend_name
            backend_type = backends[backend_name].type
            if backend_type == "local":
                if client is None:
                    client = docker.from_env()
                self._update_local_machine_status(client, machine)
            machines.append(machine)
        return machines

    def get_job(self, job_id: str) -> Job:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"{self.token_type} {self.access_token}",
        }

        job_json = self.api_request(
            "POST",
            f"{self.api_base_url}/api/v1/jobs/{job_id}",
            headers=headers,
        )
        job_json["status"] = JobStatus(job_json["status"])
        job = Job.from_dict(job_json)

        backend = self.get_backend(job.backend_name)

        client = None
        backend_type = backend.type
        if backend_type == "local":
            if client is None:
                client = docker.from_env()
            self._update_local_job_status(client, job)

        return job

    def get_machine(self, machine_name: str) -> Machine:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"{self.token_type} {self.access_token}",
        }

        machine_json = self.api_request(
            "POST",
            f"{self.api_base_url}/api/v1/machines/{machine_name}",
            headers=headers,
        )
        machine_json["status"] = JobStatus(machine_json["status"])
        machine = Machine.from_dict(machine_json)

        backend = self.get_backend(machine.backend_name)

        client = None
        backend_type = backend.type
        if backend_type == "local":
            if client is None:
                client = docker.from_env()
            self._update_local_machine_status(client, machine)

        return machine


def get_komodo_project_config_path() -> str:
    try:
        project_config_path = os.environ.get(
            "KOMODO_PROJECT_DIR",
            None,
        )
        if not project_config_path:
            # Project config must be at git repo root if not specified via env
            git_repo = git.Repo(os.getcwd(), search_parent_directories=True)
            project_config_path = git_repo.git.rev_parse("--show-toplevel")
        return project_config_path
    except FileNotFoundError:
        printing.error(
            f"Project config not found.\n* Have you run 'komo init'?",
            bold=True,
        )
        sys.exit(1)


def update_context_with_project_config(ctx: click.Context):
    project_config_path = get_komodo_project_config_path()
    v_project_config = Vyper()
    v_project_config.add_config_path(os.path.join(project_config_path, ".komo"))
    v_project_config.set_config_name("project")
    v_project_config.set_config_type("yaml")
    try:
        v_project_config.read_in_config()
    except FileNotFoundError as e:
        logger.error(e)
        printing.error("Project config not found.", bold=True)
        sys.exit(1)

    ctx.obj["project_config"] = v_project_config


def update_context_with_api_client(ctx: click.Context):
    try:
        if os.environ.get("KOMODO_GLOBAL_CONFIG_DIR", None):
            api_key_file = os.path.join(
                os.environ.get("KOMODO_GLOBAL_CONFIG_DIR"), ".komo", "api-key"
            )
        else:
            api_key_file = os.path.join(os.path.expanduser("~"), ".komo", "api-key")
        if not os.path.isfile(api_key_file):
            printing.error(
                f"No api key found at {api_key_file}. If you don't have an api key, run `komodo api-key create` to generate one, and then store it in ~/.komo/api-key."
            )
            exit(1)
        with open(api_key_file, "r") as f:
            api_key = f.read().strip()
        c = APIClient(api_key=api_key)
        ctx.obj["api_client"] = c
    except Exception as e:
        logger.error(e)
        printing.error("Error initializing API client", bold=True)
        sys.exit(1)


def config_args_to_dict(config_args: str):
    config = {}

    for arg in config_args.split(","):
        if not arg:
            continue

        if not "=" in arg or arg.count("=") > 1:
            printing.error(
                f"Invalid config parameter {arg}. Should be in form param=value.",
                bold=True,
            )
            sys.exit(1)

        param, value = arg.split("=")
        value = yaml.safe_load(value)
        config[param] = value

    return config


def update_context_project_config_with_backend_override(
    ctx: click.Context, backend_name: str, backend_config_override: dict
):
    backend_config = ctx.obj["project_config"].get("backends").get(backend_name, None)
    if backend_config is None:
        raise ClientException(
            f"Backend {backend_name} doesn't exist in the project config"
        )

    for key, value in backend_config_override.items():
        backend_config[key] = value


def handle_errors(fn):
    def inner(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except ClientException as e:
            printing.error(str(e))
            exit(1)
        except requests.exceptions.HTTPError as e:
            # Catch HTTP errors like 401, 500 etc.
            text = e.response.text
            try:
                j = e.response.json()
            except requests.exceptions.JSONDecodeError:
                j = None
            if j:
                if "detail" in j:
                    text = j["detail"]
            printing.error(f"Got HTTP Error Code {e.response.status_code}: {text}")
            exit(1)
        except requests.exceptions.ConnectionError as ec:
            printing.error(f"Connection Error: {str(ec)}")
            exit(1)
        except requests.exceptions.Timeout as et:
            printing.error(f"Timeout Error: {str(et)}")
            exit(1)
        except requests.exceptions.RequestException as e:
            # Panic
            printing.error(f"Unknown Error: {str(e)}")
            exit(1)
        except Exception as e:
            logger.error(str(e))
            printing.error(f"Encountered an unknown error: {str(e)}")
            raise e

    return inner
