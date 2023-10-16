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


@click.command("cancel")
@click.argument(
    "job_id",
    type=str,
)
@click.pass_context
@handle_errors
def cmd_cancel(ctx: click.Context, job_id: str):
    """Cancel a Komodo job."""
    update_context_with_api_client(ctx)
    logger.info(f"Cancelling job {job_id}")

    api_client: APIClient = ctx.obj["api_client"]
    job = api_client.get_job(job_id)

    backend_schema = api_client.get_backend(job.backend_name)
    backend: Backend = BackendFactory.get_backend(
        backend_schema,
        api_client,
    )

    printing.info(f"Cancelling job {job_id}", bold=True)
    api_client.cancel_job(job_id)
    # only the local backend actually does anything here
    backend.cancel(job.backend_job_id)
