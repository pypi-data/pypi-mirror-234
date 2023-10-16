"""Helper methods regarding attestations."""

import time
from pprint import pformat
from typing import Dict, Optional, Set, Union

import click
from xrpl.clients import JsonRpcClient
from xrpl.models import Amount, GenericRequest, Ledger, LedgerData
from xrpl.wallet import Wallet

from xbridge_cli.exceptions import AttestationTimeoutException, XBridgeCLIException
from xbridge_cli.utils.config_file import BridgeConfig

_ATTESTATION_TIME_LIMIT = 20  # in seconds
_WAIT_STEP_LENGTH = 1

_EXTERNAL_ATTESTATION_TIME_LIMIT = 30
_EXTERNAL_WAIT_STEP_LENGTH = 1


def wait_for_attestations(
    is_transfer: bool,
    bridge_config: BridgeConfig,
    to_client: JsonRpcClient,
    from_wallet: Wallet,
    to_account: str,
    amount: Amount,
    xchain_claim_id: Optional[int] = None,
    close_ledgers: bool = True,
    verbose: int = 0,
) -> None:
    """
    Helper method to wait for attestations.

    Args:
        is_transfer: True if the attestation is for a transfer, False if it is for an
            account create.
        bridge_config: The bridge details.
        to_client: The client on the chain the transfer is going to.
        from_wallet: The account that the transfer is coming from.
        to_account: The account that the transfer is going to.
        amount: The amount that the transfer is for.
        xchain_claim_id: The XChainClaimID for a transfer (not needed for an account
            create).
        close_ledgers: Whether to close ledgers manually (via `ledger_accept`) or wait
            for ledgers to close automatically. A standalone node requires ledgers to
            be closed; an external network does not support ledger closing.
        verbose: The verbosity of the output.

    Raises:
        AttestationTimeoutException: If the method times out while waiting for an
            attestation.
        XBridgeCLIException: If the method is waiting for a transfer and there is no
            claim ID provided.
    """
    if is_transfer and xchain_claim_id is None:
        raise XBridgeCLIException("Must have XChain Claim ID if is transfer.")

    if isinstance(amount, str):
        transfer_amount: Union[str, Dict[str, str]] = amount
    else:
        transfer_amount = amount.to_dict()

    if is_transfer:
        tx_type = "XChainAddClaimAttestation"
    else:
        tx_type = "XChainAddAccountCreateAttestation"

    if close_ledgers:
        wait_time = _WAIT_STEP_LENGTH
        attestation_time_limit = _ATTESTATION_TIME_LIMIT
    else:
        wait_time = _EXTERNAL_WAIT_STEP_LENGTH
        attestation_time_limit = _EXTERNAL_ATTESTATION_TIME_LIMIT

    if verbose > 0:
        click.echo(f"Attestation quorum is {bridge_config.quorum}")

    time_count = 0.0
    attestations_seen: Set[str] = set()
    while True:
        time.sleep(wait_time)
        if close_ledgers:
            to_client.request(GenericRequest(method="ledger_accept"))
        ledger = to_client.request(
            Ledger(ledger_index="validated", transactions=True, expand=True)
        )

        new_txs = ledger.result["ledger"]["transactions"]
        for tx in new_txs:
            if tx["TransactionType"] == tx_type:
                if tx["XChainBridge"] != bridge_config.to_xrpl():
                    # make sure attestation is for this bridge
                    continue
                # check that the attestation actually matches this transfer
                if tx["OtherChainSource"] != from_wallet.classic_address:
                    continue
                if tx["Amount"] != transfer_amount:
                    continue
                if tx["Destination"] != to_account:
                    continue
                if is_transfer:
                    if tx["XChainClaimID"] != xchain_claim_id:
                        continue
                if tx["PublicKey"] in attestations_seen:
                    # already seen this attestation, skip
                    continue
                attestations_seen.add(tx["PublicKey"])
                if verbose > 1:
                    click.echo(pformat(tx))
                if verbose > 0:
                    click.secho(
                        f"Received {len(attestations_seen)} attestations",
                        fg="bright_green",
                    )
        if len(new_txs) > 0:  # TODO: only count attestations
            time_count = 0
        else:
            time_count += wait_time

        if len(attestations_seen) >= bridge_config.quorum:
            # received enough attestations for quorum
            break

        if time_count > attestation_time_limit:
            if verbose >= 2:
                click.echo(pformat(to_client.request(LedgerData()).result))
            raise AttestationTimeoutException()
