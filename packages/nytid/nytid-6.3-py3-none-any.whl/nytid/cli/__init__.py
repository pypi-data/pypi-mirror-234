"""The CLI of nytid"""

import typer
from nytid.cli import courses
import typerconf
from nytid.cli import schedule
from nytid.cli import signupsheets
from nytid.cli import hr

import logging
import sys

logging.basicConfig(format=f"nytid: %(levelname)s: %(message)s")

cli = typer.Typer(
    help=f"""
                       A CLI for managing TAs and courses.
                       """,
    epilog="Copyright (c) 2022--2023 Daniel Bosk, " "2022 Alexander Baltatzis.",
)

cli.add_typer(courses.cli, name="courses")
typerconf.add_config_cmd(cli)
cli.add_typer(schedule.cli, name="schedule")
cli.add_typer(signupsheets.cli, name="signupsheets")
cli.add_typer(hr.cli, name="hr")

if __name__ == "__main__":
    cli()
