"""CLI functions involving sending RPC requests to a rippled node."""

import subprocess
from typing import Optional, Tuple

import click

from xbridge_cli.exceptions import XBridgeCLIException
from xbridge_cli.utils import ChainConfig, get_config


@click.command(name="request")
@click.option(
    "--name", required=True, prompt=True, help="The name of the chain to query."
)
@click.argument("command", required=True)
@click.argument("args", nargs=-1)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Whether or not to print more verbose information.",
)
def request_server(
    name: str, command: str, args: Tuple[str], verbose: bool = False
) -> None:
    """
    Send a command-line request to a rippled or witness node.
    \f

    Args:
        name: The name of the server to query.
        command: The rippled RPC command.
        args: The arguments for the RPC command.
        verbose: Whether or not to print more verbose information.
    """  # noqa: D301
    arg_string = " ".join([command, *args])
    if verbose:
        click.echo(f"{name}: {arg_string}")
    config = get_config()
    server = config.get_server(name)

    if isinstance(server, ChainConfig):  # is a rippled node
        if server.is_docker():
            to_run = ["docker", "exec", name, "/opt/rippled/bin/rippled"]
        else:
            to_run = [server.rippled, "--conf", server.config]
        to_run.extend([command, *args])
        click.echo(subprocess.check_output(to_run, stderr=subprocess.DEVNULL))
    else:  # is a witness node
        click.echo("Cannot query witness nodes from the command line right now.")


@click.command(name="status")
@click.option("--name", help="The name of the server to query.")
@click.option("--all", is_flag=True, help="Whether to query all of the servers.")
def get_server_status(name: Optional[str] = None, query_all: bool = False) -> None:
    """
    Get the status of a rippled or witness node(s).
    \f

    Args:
        name: The name of the server to query.
        query_all: Whether to stop all of the servers.

    Raises:
        XBridgeCLIException: If neither a name or `--all` is specified.
    """  # noqa: D301
    if name is None and query_all is False:
        raise XBridgeCLIException("Must specify a name or `--all`.")
    click.echo(f"{name} {query_all}")
