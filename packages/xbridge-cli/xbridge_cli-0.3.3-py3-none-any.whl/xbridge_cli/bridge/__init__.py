"""CLI command for starting a bridge."""

import click

from xbridge_cli.bridge.build import setup_bridge
from xbridge_cli.bridge.create_account import create_xchain_account
from xbridge_cli.bridge.register import register_bridge
from xbridge_cli.bridge.transfer import send_transfer


@click.group()
def bridge() -> None:
    """Subcommand for all commands dealing with the bridge itself."""
    pass


bridge.add_command(setup_bridge, name="build")
bridge.add_command(create_xchain_account, name="create-account")
bridge.add_command(register_bridge, name="register")
bridge.add_command(send_transfer, name="transfer")

__all__ = ["bridge"]
