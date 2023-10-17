"""CLI for regscale-dev commands."""
import contextlib
import sys

import click
from rich.console import Console


@click.group()
def cli() -> click.Group:
    """RegScale-Dev CLI."""
    pass


@cli.command()
@click.option(
    "--iterations", default=100, help="The number of times to run the function"
)
def profile(iterations: int) -> None:
    """Profile the CLI."""
    from regscale.dev.profiling import profile_about_command, profile_my_function

    profile_my_function(profile_about_command, iterations=iterations)
    console = Console()
    console.print(
        "Profiling complete, you can view the file in [yellow]profile_stats.csv[reset] or [yellow]profile_stats.pstat[reset]"
    )


@cli.command()
@click.option(
    "--iterations", default=100, help="The number of times to run the function"
)
def calculate_start_time(iterations: int) -> None:
    """Calculate the start time for the CLI."""
    from regscale.dev.profiling import calculate_load_times

    calculate_load_times(iterations=iterations)


@cli.command()
@click.option("--raw", is_flag=True, help="Output raw results")
def calculate_import_time(raw: bool) -> None:
    """Calculate the import time for the CLI."""
    from regscale.dev.profiling import calculate_cli_import_time

    load_time = calculate_cli_import_time()
    if raw:
        print(load_time)
    else:
        console = Console()
        console.print(f"It took {load_time:.6f} seconds to import the CLI.")


with contextlib.suppress(ImportError, SystemExit):
    from regscale.airflow.azure.cli import cli as azure_cli

    cli.add_command(azure_cli)


if __name__ == "__main__":
    cli()
