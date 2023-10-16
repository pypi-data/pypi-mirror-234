import sys

import click
from loguru import logger

import komodo_cli.printing as printing
from komodo_cli.backends.backend import Backend
from komodo_cli.backends.backend_factory import BackendFactory
from komodo_cli.types import JobNotFoundException, JobStatus
from komodo_cli.utils import APIClient, handle_errors, update_context_with_api_client


@click.command("logs")
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
@click.option(
    "--watch",
    "-w",
    type=bool,
    is_flag=True,
    help="Whether to watch the logs or just output current logs.",
)
@click.pass_context
@handle_errors
def cmd_logs(ctx: click.Context, job_id: str, node_index: int, watch: bool):
    """Get logs for a Komodo job."""
    update_context_with_api_client(ctx)
    logger.info(f"Getting logs for job {job_id}, watch={watch}")

    api_client: APIClient = ctx.obj["api_client"]

    job = api_client.get_job(job_id)
    if job.status == JobStatus.PENDING:
        printing.warning(
            f"Job {job_id} is currently pending",
            bold=True,
        )
        return

    if node_index >= job.num_nodes:
        printing.error(
            f"Node index {node_index} is out of range, job {job_id} only has {job.num_nodes} nodes"
        )
        exit(1)

    backend_schema = api_client.get_backend(job.backend_name)
    backend: Backend = BackendFactory.get_backend(
        backend_schema,
        api_client,
    )

    printing.info(f"Getting logs for job {job_id}", bold=True)
    for line in backend.logs(job.backend_job_id, node_index, watch):
        if type(line) != str:
            line = line.decode("utf-8")
        printing.info(f"{line.strip()}")
