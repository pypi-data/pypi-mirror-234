import getpass

import click

import komodo_cli.printing as printing
from komodo_cli.utils import APIClient, handle_errors

MIN_PASSWORD_LENGTH = 8


@click.command("register")
@handle_errors
def cmd_register():
    email = input("Email: ")

    while True:
        pw1 = getpass.getpass("Password: ")
        if len(pw1) < MIN_PASSWORD_LENGTH:
            printing.error(
                "Password must be at least 8 characters, please enter a new password."
            )
            continue
        pw2 = getpass.getpass("Re-enter password: ")

        if pw1 != pw2:
            printing.error("Passwords do not match, please try again.")
            continue

        break

    APIClient.register(email, pw1)

    printing.success(f"Successfully registered user {email}")
