from enum import Enum
from typing import List, Optional


class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    FINISHED = "finished"
    CANCELLING = "cancelling"
    CANCELLED = "cancelled"
    ERROR = "error"
    UNKNOWN = "unknown"
    NOT_FOUND = "not found"
    UNAUTHORIZED = "unauthorized"
    UNREACHABLE = "unreachable"
    # this status is for local jobs that were not created on the current computer
    NOT_AVAILABLE_CURRENT_COMPUTER = "not_available_on_current_computer"


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


class ClientException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class TooManyNodes(ClientException):
    def __init__(self, max_supported_replicas: int):
        super().__init__(
            f"Backend only supports up to {max_supported_replicas} node{'s' if max_supported_replicas > 1 else ''}"
        )


class JobNotFoundException(ClientException):
    def __init__(self):
        super().__init__("Job not found")


class JobNotInDesiredStateException(ClientException):
    def __init__(self):
        super().__init__("Job not in desired state")


class OverlayImageBuildException(ClientException):
    def __init__(self):
        super().__init__("Overlay image failed to build")


class OverlayImagePushException(ClientException):
    def __init__(self):
        super().__init__(
            "Overlay image failed to push. Please make sure you are logged in with Docker and have the correct permissions to push to your registry."
        )


class Job:
    def __init__(
        self,
        backend_name: str,
        resource_name: Optional[str],
        id: str,
        backend_job_id: Optional[str],
        command: str,
        image: str,
        status: JobStatus,
        num_nodes: int,
    ):
        self.backend_name = backend_name
        self.resource_name = resource_name
        self.id = id
        self.backend_job_id = backend_job_id
        self.command = command
        self.image = image
        self.status = status
        self.num_nodes = num_nodes

    @classmethod
    def from_dict(cls, d):
        obj = cls(**d)
        obj.status = JobStatus(d["status"])
        return obj

    def to_dict(self):
        return {
            "backend_name": self.backend_name,
            "resource_name": self.resource_name,
            "id": self.id,
            "backend_job_id": self.backend_job_id,
            "command": self.command,
            "image": self.image,
            "status": self.status.name,
            "num_nodes": self.num_nodes,
        }


class Machine:
    def __init__(
        self,
        name: str,
        backend_name: str,
        resource_name: Optional[str],
        image: str,
        status: JobStatus,
        backend_job_id: str,
    ):
        self.name = name
        self.backend_name = backend_name
        self.resource_name = resource_name
        self.image = image
        self.status = status
        self.backend_job_id = backend_job_id

    @classmethod
    def from_dict(cls, d):
        obj = cls(**d)
        obj.status = JobStatus(d["status"])
        return obj

    def to_dict(self):
        return {
            "name": self.name,
            "backend_name": self.backend_name,
            "resource_name": self.resource_name,
            "backend_job_id": self.backend_job_id,
            "image": self.image,
            "status": self.status.name,
        }


class Resource:
    def __init__(
        self,
        name: str,
        config: dict,
    ):
        self.name = name
        self.config = config

    @classmethod
    def from_dict(cls, d):
        obj = cls(**d)
        return obj

    def to_dict(self):
        d = {
            "name": self.name,
            "config": self.config,
        }
        return d


class Backend:
    def __init__(
        self,
        name: str,
        type: str,
        config: dict,
        resources: List[Resource],
    ):
        self.name = name
        self.type = type
        self.config = config
        self.resources = resources

    @classmethod
    def from_dict(cls, d):
        resources_dicts = d["resources"]
        resources = [Resource.from_dict(r) for r in resources_dicts]
        obj = cls(
            name=d["name"],
            type=d["type"],
            config=d["config"],
            resources=resources,
        )
        return obj

    def to_dict(self):
        d = {
            "name": self.name,
            "type": self.type,
            "config": self.config,
            "resources": [r.to_dict() for r in self.resources],
        }
        return d
