---
sidebar_position: 1
---

# Validator Security

Each validator is encouraged to run its operations independently, as diverse setups increase the resilience of the network.
Validator candidates should put aside meaningful time to guarantee a secure validator launch.

In this section, you can learn about best practices for operating a validator securely without sacrificing block sign performance.
This includes information on how to secure your private keys, run a cluster of nodes with remote access,
mitigate the risk of double signing and contribute to DDOS protection on the network through sentry nodes.

Also, a [validator security checklist](./validator-security-checklist.md) is provided
to conduct a survey on the current security measures of a validator.

## Horcrux

Horcrux is a [multi-party-computation (MPC)](https://en.wikipedia.org/wiki/Secure_multi-party_computation)
signing service for Tendermint nodes, that improves your validator infrastructure in terms of security and availability.
It offers

- Composed of a cluster of signer nodes in place of the remote signer,
enabling High Availability (HA) for block signing through fault tolerance.
- Secure your validator private key by splitting it across multiple private signer nodes using threshold Ed25519 signatures
- Add security and availability without sacrificing block sign performance.

See the documentation [here](https://github.com/strangelove-ventures/horcrux/blob/main/docs/migrating.md)
to learn how to upgrade your validator infrastructure with Horcrux.

## Hardware HSM

It is mission-critical that an attacker cannot steal a validator's key.
If this is possible, it puts the entire stake delegated to the compromised validator at risk.
Hardware security modules are an important strategy for mitigating this risk.

HSM modules must support `ed25519` signatures for Evmos.
The [YubiHSM 2](https://www.yubico.com/products/hardware-security-module/) supports `ed25519`
and can be used with this YubiKey [library](https://github.com/iqlusioninc/yubihsm.rs).

:::info
🚨 **IMPORTANT**:
The YubiHSM can protect a private key but **cannot ensure** in a secure setting that it won't sign the same block twice.
:::

## Tendermint KMS

Tendermint KMS is a signature service with support for Hardware Security Modules (HSMs),
such as YubiHSM2 and Ledger Nano.
It is intended to be run alongside Cosmos Validators,
ideally on separate physical hosts, providing defense-in-depth for online validator signing keys,
double signing protection,
and functioning as a central signing service that can be used when operating multiple validators in several Cosmos Zones.

Learn how to set up a Key Management System for Evmos with Tendermint KMS [here](./tendermint-kms).

## Sentry Nodes (DDOS Protection)

Validators are responsible for ensuring that the network can sustain denial-of-service attacks. One recommended way
to mitigate these risks is for validators to carefully structure their network topology in a so-called sentry node architecture.

Validator nodes should only connect to full nodes they trust because they operate them themselves
or are run by other validators they know socially.
A validator node will typically run in a data center.
Most data centers provide direct links to the networks of major cloud providers.
The validator can use those links to connect to sentry nodes in the cloud.
This shifts the burden of denial-of-service from the validator's node directly to its sentry nodes
and may require new sentry nodes to be spun up or activated to mitigate attacks on existing ones.

Sentry nodes can be quickly spun up or change their IP addresses.
Because the links to the sentry nodes are in private IP space,
an internet-based attack cannot disturb them directly.
This will ensure validator block proposals and votes always make it to the rest of the network.

:::tip
Read more about Sentry Nodes on the [forum](https://forum.cosmos.network/t/sentry-node-architecture-overview/454)
:::

To set up your sentry node architecture you can follow the instructions below:

Validator nodes should edit their `config.toml`:

```bash
# Comma separated list of nodes to keep persistent connections to
# Do not add private peers to this list if you don't want them advertised
persistent_peers =[list of sentry nodes]

# Set true to enable the peer-exchange reactor
pex = false
```

Sentry Nodes should edit their config.toml:

```bash
# Comma separated list of peer IDs to keep private (will not be gossiped to other peers)
# Example ID: 3e16af0cead27979e1fc3dac57d03df3c7a77acc@3.87.179.235:26656

private_peer_ids = "node_ids_of_private_peers"
```

## Validator Backup

It is **crucial** to back up your validator's private key. It's the only way to restore your validator in the event of a
 disaster. The validator private key is a Tendermint Key: a unique key used to sign consensus votes.

To backup everything you need to restore your validator, note that if you are using the "software sign" (the default
signing method of Tendermint), your Tendermint key is located at:

```bash
~/.evmosd/config/priv_validator_key.json
```

Then do the following:

1. Back up the `json` file mentioned above (or backup the whole `config` folder).
2. Back up the self-delegator wallet. See [backing up wallets with the Evmos Daemon](./../../protocol/concepts/key-management).

To see your validator's associated public key:

```bash
evmosd tendermint show-validator
```

To see your validator's associated bech32 address:

```bash
evmosd tendermint show-address
```

You can also use hardware to store your Tendermint Key much more safely, such as [YubiHSM2](https://developers.yubico.com/YubiHSM2/).

## Environment Variables

By default, uppercase environment variables with the following prefixes will replace lowercase command-line flags:

- `EVMOS` (for Evmos flags)
- `TM` (for Tendermint flags)
- `BC` (for democli or basecli flags)

For example, the environment variable `EVMOS_CHAIN_ID` will map to the command line flag `--chain-id`. Note that while
explicit command-line flags will take precedence over environment variables, environment variables will take precedence
over any of your configuration files. For this reason,  you must lock down your environment such that any critical
parameters are defined as flags on the binary or prevent modification of any environment variables.
