---
sidebar_position: 3
---

# Single Node

Following this page, you can run a single node local network manually or
by using the already prepared automated script. Running a single node setup is useful
for developers who want to test their applications and protocol features because of 
its simplicity and speed. For more complex setups, please refer to the [Multi Node Setup](./multi-nodes) page.

## Prerequisite Readings

- [Install Binary](./)

## Automated Script

You can customize the local node script by changing values for convenience for example:

```bash
# customize the name of your key, the chain-id, moniker of the node, keyring backend, and log level
KEY="dev0"
CHAINID="evmos_9000-4"
MONIKER="localtestnet"
KEYRING="test"
LOGLEVEL="info"


# Allocate genesis accounts (cosmos formatted addresses)
evmosd add-genesis-account $KEY 100000000000000000000000000aevmos --keyring-backend $KEYRING

# Sign genesis transaction
evmosd gentx $KEY 1000000000000000000000aevmos --keyring-backend $KEYRING --chain-id $CHAINID
```

The default configuration will generate a single validator localnet with the chain-id
`evmosd-1` and one predefined account (`dev0`) with some allocated funds at the genesis.

You can start the local chain using:

```bash
 $ local_node.sh
...
```

:::tip
To avoid overwriting any data for a real node used in production, it was decided to store the automatically generated testing configuration at `~/.tmp-evmosd` instead of the default `~/.evmosd`.
:::

When working with the `local_node.sh` script, it is necessary to extend all `evmosd` commands, that target the local test node, with the `--home ~/.tmp-evmosd` flag. This is mandatory, because the `home` directory cannot be stored in the `evmosd` configuration, which can be seen in the output below. For ease of use, it might be sensible to export this directory path as an environment variable:

```
 $ export TMP=$HOME/.tmp-evmosd`
 $ evmosd config --home $TMP
{
	"chain-id": "evmos_9000-1",
	"keyring-backend": "test",
	"output": "text",
	"node": "tcp://localhost:26657",
	"broadcast-mode": "sync"
}
```

## Manual Deployment

This guide helps you create a single validator node that runs a network locally for testing and other development related uses.

### Initialize the chain

Before actually running the node, we need to initialize the chain, and most importantly its genesis file. This is done with the `init` subcommand:

```bash
$MONIKER=testing
$KEY=dev0
$CHAINID="evmos_9000-4"

# The argument $MONIKER is the custom username of your node, it should be human-readable.
evmosd init $MONIKER --chain-id=$CHAINID
```

:::tip
You can [edit](./evmosd#configuring-the-node) this `moniker` later by updating the `config.toml` file.
:::

The command above creates all the configuration files needed for your node and validator to run, as well as a default genesis file, which defines the initial state of the network. All these [configuration files](./evmosd#configuring-the-node) are in `~/.evmosd` by default, but you can overwrite the location of this folder by passing the `--home` flag.

### Genesis Procedure

### Adding Genesis Accounts

Before starting the chain, you need to populate the state with at least one account using the [keyring](./../../protocol/concepts/keyring#add-keys):

```bash
evmosd keys add my_validator
```

Once you have created a local account, go ahead and grant it some `aevmos` tokens in your chain's genesis file. Doing so will also make sure your chain is aware of this account's existence:

```bash
evmosd add-genesis-account my_validator 10000000000aevmos
```

Now that your account has some tokens, you need to add a validator to your chain.

 For this guide, you will add your local node (created via the `init` command above) as a validator of your chain. Validators can be declared before a chain is first started via a special transaction included in the genesis file called a `gentx`:

```bash
# Create a gentx
# NOTE: this command lets you set the number of coins.
# Make sure this account has some coins with the genesis.app_state.staking.params.bond_denom denom
evmosd add-genesis-account my_validator 1000000000stake,10000000000aevmos
```

A `gentx` does three things:

1. Registers the `validator` account you created as a validator operator account (i.e. the account that controls the validator).
2. Self-delegates the provided `amount` of staking tokens.
3. Link the operator account with a Tendermint node pubkey that will be used for signing blocks. If no `--pubkey` flag is provided, it defaults to the local node pubkey created via the `evmosd init` command above.

For more information on `gentx`, use the following command:

```bash
evmosd gentx --help
```

### Collecting `gentx`

By default, the genesis file do not contain any `gentxs`. A `gentx` is a transaction that bonds
staking token present in the genesis file under `accounts` to a validator, essentially creating a
validator at genesis. The chain will start as soon as more than 2/3rds of the validators (weighted
by voting power) that are the recipient of a valid `gentx` come online after `genesis_time`.

A `gentx` can be added manually to the genesis file, or via the following command:

```bash
# Add the gentx to the genesis file
evmosd collect-gentxs
```

This command will add all the `gentxs` stored in `~/.evmosd/config/gentx` to the genesis file.

### Run Single Node

Finally, check the correctness of the `genesis.json` file:

```bash
evmosd validate-genesis
```

Now that everything is set up, you can finally start your node:

```bash
evmosd start
```

:::tip
To check all the available customizable options when running the node, use the `--help` flag.
:::

You should see blocks come in.

The previous command allow you to run a single node. This is enough for the next section on interacting with this node, but you may wish to run multiple nodes at the same time, and see how consensus happens between them.

You can then stop the node using `Ctrl+C`.




## Further Configuration

### Key Management

To run a node with the same key every time: replace `evmosd keys add $KEY` in `./local_node.sh` with:

```bash
echo "your mnemonic here" | evmosd keys add $KEY --recover
```

:::tip
Evmos currently only supports 24 word mnemonics.
:::

You can generate a new key/mnemonic with:

```bash
evmosd keys add $KEY
```

To export your Evmos key as an Ethereum private key (for use with [Metamask](./../../../use/connect-your-wallet/metamask) for example):

```bash
evmosd keys unsafe-export-eth-key $KEY
```

For more about the available key commands, use the `--help` flag

```bash
evmosd keys -h
```

### Keyring backend options

The instructions above include commands to use `test` as the `keyring-backend`. This is an unsecured
keyring that doesn't require entering a password and should not be used in production. Otherwise,
Evmos supports using a file or OS keyring backend for key storage. To create and use a file
stored key instead of defaulting to the OS keyring, add the flag `--keyring-backend file` to any
relevant command and the password prompt will occur through the command line. This can also be saved
as a CLI config option with:

```bash
evmosd config keyring-backend file
```

:::tip
For more information about the Keyring and its backend options, click [here](./../concepts/keyring).
:::

### Enable Tracing

 To enable tracing when running the node, modify the last line of the `local_node.sh` script to be the following command, where:

- `$TRACER` is the EVM tracer type to collect execution traces from the EVM transaction execution (eg. `json|struct|access_list|markdown`)
- `$TRACESTORE` is the output file which contains KVStore tracing (eg. `store.txt`)

```bash
evmosd start --evm.tracer $TRACER --tracestore $TRACESTORE --pruning=nothing $TRACE --log_level $LOGLEVEL --minimum-gas-prices=0.0001aevmos --json-rpc.api eth,txpool,personal,net,debug,web3
```

## Clearing data from chain

### Reset Data

Alternatively, you can **reset** the blockchain database, remove the node's address book files, and reset the `priv_validator.json` to the genesis state.

:::danger
If you are running a **validator node**, always be careful when doing `evmosd unsafe-reset-all`. You should never use this command if you are not switching `chain-id`.
:::

:::danger
**IMPORTANT**: Make sure that every node has a unique `priv_validator.json`. **Do not** copy the `priv_validator.json` from an old node to multiple new nodes. Running two nodes with the same `priv_validator.json` will cause you to double sign!
:::

First, remove the outdated files and reset the data.

```bash
rm $HOME/.evmosd/config/addrbook.json $HOME/.evmosd/config/genesis.json
evmosd tendermint unsafe-reset-all --home $HOME/.evmosd
```

Your node is now in a pristine state while keeping the original `priv_validator.json` and `config.toml`. 
If you had any sentry nodes or full nodes setup before, your node will still try to connect to them, 
but may fail if they haven't also been upgraded.

### Delete Data

import Highlighter from '@site/src/components/Highlighter';
import ProjectValue from '@site/src/components/ProjectValue';

Data for the <ProjectValue keyword="binary" /> binary should be stored at <Highlighter pretext="~/." keyword="binary" />,
 respectively by default. To **delete** the existing binaries and configuration, run:

```bash
rm -rf ~/.evmosd
```

To clear all data except key storage (if keyring backend chosen) and then you can rerun the full node installation 
commands from above to start the node again.

## Recording Transactions Per Second (TPS)

In order to get a progressive value of the transactions per second, we use Prometheus to return the values.
The Prometheus exporter runs at address <http://localhost:8877> so please add this
section to your [Prometheus installation](https://opencensus.io/codelabs/prometheus/#1) config.yaml file like this

```yaml
global:
  scrape_interval: 10s

  external_labels:
    monitor: 'evmos'

scrape_configs:
  - job_name: 'evmos'

    scrape_interval: 10s

    static_configs:
      - targets: ['localhost:8877']
```

and then run Prometheus like this

```shell
prometheus --config.file=prom_config.yaml
```

and then visit the Prometheus dashboard at <http://localhost:9090/> then navigate to the expression area and enter the following expression

```shell
rate(evmosd_transactions_processed[1m])
```

which will show the rate of transactions processed.


:::tip
Evmos currently only supports 24 word mnemonics.
:::
