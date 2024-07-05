---
sidebar_position: 2
---

# EIP-155: Replay Protection

As Cosmos SDK based blockchains use Bech32 representations for address, which contain a unique prefix per chain,
replay protection of transactions is inherently present.
However, as Ethereum based transactions rely on the Hex representation of addresses, this unique property is evaded.
This means, that theoretically transactions signed on a different network are valid transactions on other networks too.
This potential exploit is addressed by including the chain ID information in the transaction data that is signed.

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
