---
sidebar_position: 2
---

# EIP-155: Replay Protection

[EIP-155](https://eips.ethereum.org/EIPS/eip-155) is an Ethereum Improvement Proposal,
that has introduced a simple replay protection mechanism,
by including the chain ID information into the signed transaction data.
This was necessary, because Ethereum-based transactions rely on the Hex representation of addresses,
which are not necessarily unique to a given network.
This means that single signed transaction could be valid on multiple networks,
as the same addresses are involved e.g. in a token transfer.
This holds the potential for exploits and is addressed by enforcing the EIP-155 replay protection.

Cosmos SDK-based blockchains use Bech32 representations for addresses, which contain a unique prefix per chain.
This means, that for Cosmos transactions, replay protection is inherently present as addresses of a given chain
are not valid addresses on other chains.
However, as Evmos also accepts EVM transactions, handling only those transactions that conform to EIP-155
becomes a requirement again.

This requires special care to be taken when selecting an EIP-155 compliant [chain ID](./chain-id.mdx)
to avoid duplication amongst chains.

## Configuring Replay Protection

By default, replay protection is enabled on any Evmos node.
There are two distinct steps required to accept unprotected transactions, i.e. those that do not contain the chain ID
in the signed transaction data:

1. **Disable Module Parameter**:
The [EVM module](../modules/evm.md#parameters) contains a governance controlled parameter,
that globally dictates if unprotected transactions are supported.
This has to be disabled via a governance vote or
by setting the `allow_unprotected_txs` field to `true` in the genesis of a [local node](../evmos-cli/single-node.mdx).

2. **Adjust Node Configuration**:
When the global parameter is set accordingly, each node operator has the option to individually opt into allowing
unprotected transactions to be sent to their nodes.
This configuration is explained in the section on
[node configuration](../../validate/setup-and-configuration/configuration.md#eip-155-replay-protection).
