#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the entry point for the command-line interface (CLI) application.

It can be used as a handy facility for running the task from a command line.

.. note::

    To learn more about Click visit the
    `project website <http://click.pocoo.org/5/>`_.  There is also a very
    helpful `tutorial video <https://www.youtube.com/watch?v=kNke39OZ2k0>`_.

    To learn more about running Luigi, visit the Luigi project's
    `Read-The-Docs <http://luigi.readthedocs.io/en/stable/>`_ page.

.. currentmodule:: komodo_cli.cli
.. moduleauthor:: kmushegi <mushegiani@gmail.com>
"""
import os
import sys

import click
from loguru import logger
from vyper import Vyper

import komodo_cli.printing as printing
from komodo_cli.commands.api_key.api_key import api_key
from komodo_cli.commands.backend.backend import backend
from komodo_cli.commands.cmd_cancel import cmd_cancel
from komodo_cli.commands.cmd_delete import cmd_delete
from komodo_cli.commands.cmd_describe import cmd_describe
from komodo_cli.commands.cmd_do import cmd_do
from komodo_cli.commands.cmd_list import cmd_list
from komodo_cli.commands.cmd_logs import cmd_logs
from komodo_cli.commands.cmd_register import cmd_register
from komodo_cli.commands.cmd_run import cmd_run
from komodo_cli.commands.cmd_shell import cmd_shell
from komodo_cli.commands.compute.compute import compute
from komodo_cli.commands.init.init import init
from komodo_cli.commands.machine.machine import machine
from komodo_cli.overlay_images.overlay_images import OverlayImages
from komodo_cli.utils import handle_errors

from .__init__ import __version__

LOGGING_LEVELS = {
    0: "NOTSET",
    1: "ERROR",
    2: "WARNING",
    3: "INFO",
    4: "DEBUG",
}  #: a mapping of `verbose` option counts to logging levels


@click.group()
@click.option("--verbose", "-v", count=True, help="Enable verbose output.")
@click.pass_context
@handle_errors
def cli(ctx: click.Context, verbose: int) -> None:
    """Run Komodo."""

    # Use the verbosity count to determine the logging level...
    if verbose > 0:
        logger.info(f"verbose count {verbose}")
        log_level = LOGGING_LEVELS[verbose] if verbose in LOGGING_LEVELS else "DEBUG"
        logger.remove()
        logger.add(
            sys.stdout,
            level=log_level,
        )
        printing.warning(
            f"Verbose logging is enabled. " f"(LEVEL={log_level})",
        )
    else:
        logger.remove()

    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose


@cli.command()
def version():
    """Get the library version."""
    printing.info(f"{__version__}", bold=True)


cli.add_command(cmd_register)
cli.add_command(init)
cli.add_command(cmd_run)
cli.add_command(cmd_list)
cli.add_command(cmd_logs)
cli.add_command(cmd_describe)
cli.add_command(cmd_shell)
cli.add_command(cmd_cancel)
cli.add_command(cmd_delete)
cli.add_command(machine)
cli.add_command(cmd_do)
cli.add_command(compute)
cli.add_command(api_key)
cli.add_command(backend)
