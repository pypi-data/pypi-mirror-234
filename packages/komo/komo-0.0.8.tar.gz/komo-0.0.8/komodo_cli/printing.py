import click


def info(msg: str, bold=False):
    click.secho(msg, fg="white", bold=bold)


def error(msg: str, bold=False):
    click.secho(msg, fg="red", bold=bold)


def warning(msg: str, bold=False, nl=True):
    click.secho(msg, fg="yellow", bold=bold, nl=nl)


def success(msg: str, bold=False):
    click.secho(msg, fg="green", bold=bold)


def header(msg: str, bold=False):
    click.secho(msg, fg="magenta", bold=bold)
