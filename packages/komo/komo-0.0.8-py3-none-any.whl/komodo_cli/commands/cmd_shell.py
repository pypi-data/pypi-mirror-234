import sys

import click
from loguru import logger

import komodo_cli.printing as printing
from komodo_cli.backends.backend import Backend
from komodo_cli.backends.backend_factory import BackendFactory
from komodo_cli.types import JobStatus
from komodo_cli.utils import APIClient, handle_errors, update_context_with_api_client


@click.command("shell")
@click.argument(
    "job_id",
    type=str,
)
@click.option(
    "--node-index",
    "-i",
    type=int,
    default=0,
    help="The index of the node to get logs from",
)
@click.pass_context
@handle_errors
def cmd_shell(ctx: click.Context, job_id: str, node_index: int):
    """Open a shell into a running Komodo job."""
    update_context_with_api_client(ctx)
    logger.info(f"Starting a shell into job {job_id}")

    api_client: APIClient = ctx.obj["api_client"]

    job = api_client.get_job(job_id)

    if job.status != JobStatus.RUNNING:
        printing.error(f"Job {job.id} is not running", bold=True)
        return

    backend_schema = api_client.get_backend(job.backend_name)
    backend: Backend = BackendFactory.get_backend(
        backend_schema,
        api_client,
    )

    printing.header(f"Shelling into job {job_id}", bold=True)
    backend.shell(job.backend_job_id, node_index)
