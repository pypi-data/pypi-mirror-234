import click
from loguru import logger
from tabulate import tabulate

import komodo_cli.printing as printing
from komodo_cli.utils import APIClient, handle_errors, update_context_with_api_client


@click.command("describe")
@click.argument(
    "job_id",
    type=str,
)
@click.pass_context
@handle_errors
def cmd_describe(ctx: click.Context, job_id: str):
    """Describe a Komodo job."""
    update_context_with_api_client(ctx)
    logger.info(f"Describing job {job_id}")

    api_client: APIClient = ctx.obj["api_client"]

    job = api_client.get_job(job_id)
    jobs_to_print = [
        [
            job.id,
            job.command,
            job.status.value,
            job.backend_name,
            job.resource_name,
            job.backend_job_id,
        ]
    ]

    click.echo(
        tabulate(
            jobs_to_print,
            headers=[
                "Job ID",
                "Command",
                "Status",
                "Backend",
                "Resource",
                "Backend Job ID",
            ],
            tablefmt="simple_grid",
        ),
    )
