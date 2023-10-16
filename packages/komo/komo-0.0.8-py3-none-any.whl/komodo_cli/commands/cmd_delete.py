import click
from loguru import logger

import komodo_cli.printing as printing
from komodo_cli.backends.backend import Backend
from komodo_cli.backends.backend_factory import BackendFactory
from komodo_cli.types import (
    JobNotFoundException,
    JobNotInDesiredStateException,
    JobStatus,
)
from komodo_cli.utils import APIClient, handle_errors, update_context_with_api_client


@click.command("delete")
@click.argument(
    "job_id",
    type=str,
)
@click.option(
    "--force",
    "-f",
    type=bool,
    is_flag=True,
    help="Set this flag if you want to delete the job even if the job is still running",
)
@click.pass_context
@handle_errors
def cmd_delete(ctx: click.Context, job_id: str, force: bool):
    """Delete a Komodo job."""
    update_context_with_api_client(ctx)
    logger.info(f"Deleting job {job_id}")

    api_client: APIClient = ctx.obj["api_client"]

    if job_id == "all":
        jobs = api_client.list_jobs(limit=-1)
    else:
        jobs = [api_client.get_job(job_id)]

    for job in jobs:
        backend_schema = api_client.get_backend(job.backend_name)
        backend: Backend = BackendFactory.get_backend(
            backend_schema,
            api_client,
        )

        printing.warning(f"Deleting job {job.id}", bold=True)
        api_client.delete_job(job.id, force)
        # only the local backend actually does anything here
        backend.delete(job.backend_job_id)
