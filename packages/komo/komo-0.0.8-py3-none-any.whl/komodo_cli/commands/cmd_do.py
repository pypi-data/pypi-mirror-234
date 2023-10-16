import os

import click
import yaml

import komodo_cli.printing as printing
from komodo_cli.commands.cmd_run import _run_helper
from komodo_cli.utils import handle_errors


@click.command("do")
@click.option("--file", "-f", type=str, required=True)
@click.option("--detach", "-d", is_flag=True)
@click.pass_context
@handle_errors
def cmd_do(ctx: click.Context, file: str, detach: bool):
    if not os.path.isfile(file):
        printing.error(
            f"{file} does not exist",
            bold=True,
        )

    with open(file, "r") as f:
        action = yaml.load(f, yaml.FullLoader)

    kind = action["kind"]

    if kind == "task":
        # TODO: use vyper for defaults
        backend = action.get("backend", None)
        resource = action.get("resource", None)
        num_nodes = action.get("num_nodes", 1)
        backend_config_override = action.get("backend_config", {})
        command = action["command"]
        _run_helper(
            ctx,
            backend,
            resource,
            num_nodes,
            backend_config_override,
            detach,
            command,
        )
    # TODO: add support for machine actions
    else:
        printing.error(f"Action of type {kind} is not supported", bold=True)
        exit(1)
