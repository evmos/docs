import ProjectValue from '@site/src/components/ProjectValue';

# Evmos CLI

`evmosd` is the all-in-one command-line interface (CLI). It allows you to run an Evmos node, manage wallets and interact
 with the Evmos network through queries and transactions. This introduction will explain how to install the `evmosd`
 binary onto your system and guide you through some simple examples how to use evmosd.

## Prerequisites

#### Go

Evmos is built using [Go](https://golang.org/dl/) version `1.19+`. Check your version with:

```bash
go version
```

Once you have installed the right version, confirm that your [`GOPATH`](https://golang.org/doc/gopath_code#GOPATH)
 is correctly configured by running the following command and adding it to your shell startup script:

```bash
export PATH=$PATH:$(go env GOPATH)/bin
```

#### jq

Evmos scripts are using [jq](https://stedolan.github.io/jq/download/) version `1.6+`. Check your version with:

```
jq --version
```

## Installation

You can build and install the `evmosd` binaries from source or using Docker.

### Github

Clone and build the Evmos from source using `git`. The `<tag>` refers to a release tag on Github. The latest Evmos
 [version](https://github.com/evmos/evmos/releases) is <ProjectValue keyword='latest_version'/>:

```bash
git clone https://github.com/evmos/evmos.git
cd evmos
git fetch
git checkout <tag>
make install
```

After installation is done, check that the evmosd binaries have been successfully installed:

```bash
evmosd version
```

:::info
If the `evmosd: command not found` error message is returned, confirm that you have configured [Go](#go) correctly.
:::

### Docker

To build Evmos using Docker, check out the latest version as described above and create a docker container
`tharsishq/evmos:latest` with:

```bash
make build-docker
```

Now you can run `evmosd` in the container.

```bash
docker run -it -p 26657:26657 -p 26656:26656 -v ~/.evmosd/:/root/.evmosd tharsishq/evmos:latest evmosd version
```

<!--
TODO: The docker setup is missing a script that lets you run a local node -> requires a better description

```bash
# To initialize
docker run -it -p 26657:26657 -p 26656:26656 -v ~/.evmosd/:/root/.evmosd tharsishq/evmos:latest evmosd init test-chain 
--chain-id test_9000-2

# To run
docker run -it -p 26657:26657 -p 26656:26656 -v ~/.evmosd/:/root/.evmosd tharsishq/evmos:latest evmosd start

Following just this, causes running into

`panic: validator set is empty after InitGenesis, please ensure at least one validator is initialized with a delegation 
greater than or equal to the DefaultPowerReduction ({824649071904})`
``` -->

## Run an Evmos node

To become familiar with Evmos, you can run a local blockchain node that produces blocks and exposes EVM and Cosmos
endpoints. This allows you to deploy and interact with smart contracts locally or test core protocol functionality.

Run the local node by executing the `local_node.sh` script in the base directory of the repository:

```bash
./local_node.sh
```

The script stores the node configuration including the local default endpoints under `~/.tmp-evmosd/config/config.toml`.
 If you have previously run the script, the script allows you to overwrite the existing configuration and start a new
 local node.

Once your node is running you will see it validating and producing blocks in your local Evmos blockchain:

```bash
12:59PM INF executed block height=1 module=state num_invalid_txs=0 num_valid_txs=0 server=node
# ...
1:00PM INF indexed block exents height=7 module=txindex server=node
```

## Using `evmosd`

After installing the `evmosd` binary, you can run commands using:

```bash
evmosd [command]
```

There is also a `-h`, `--help` command available

```bash
evmosd -h
```

It is possible to maintain multiple node configurations at the same time. To specify a configuration use the `--home`
flag. In the following examples we will be using the default config for a local node, located at `~/.tmp-evmosd`.

### Manage wallets

You can manage your wallets using the evmosd binary to store private keys and sign transactions over CLI. To view all
keys use:

```bash
evmosd keys list \
--home ~/.tmp-evmosd \
--keyring-backend test

# Example Output:
# - address: evmos19xnmslvl0pcmydu4m52h2gf0std5ee5pfgpyuf
#   name: dev0
#   pubkey: '{"@type":"/ethermint.crypto.v1.ethsecp256k1.PubKey","key":"AzKouyoUL0UUS1qRUZdqyVsTPkCAFWwxx3+BTOw36nKp"}'
#   type: local
```

You can generate a new key/mnemonic with a `$NAME` with:

```bash
evmosd keys add [name] \
--home ~/.tmp-evmosd \
--keyring-backend test
```

To export your evmos key as an Ethereum private key (for use with [Metamask](./../../../use/connect-your-wallet/metamask)
 for example):

```bash
evmosd keys unsafe-export-eth-key [name] \
--home ~/.tmp-evmosd \
--keyring-backend test
```

For more about the available key commands, use the `--help` flag

```bash
evmosd keys -h
```

<!-- TODD: Add link to node configurations
:::tip
For more information about the Keyring and its backend options, click [here](../../../protocol/concepts/keyring).
:::
-->

### Interact with a Network

You can use evmosd to query information or submit transactions on the blockchain. Queries and transactions are requests
 that you send to an Evmos node through the Tendermint RPC.

:::tip
👉 To use the CLI, you will need to provide a Tendermint RPC address for the `--node` flag.
Look for a publicly available addresses for testnet and mainnet in the [Networks](./../../develop/api/networks) page.
:::

#### Set Network Config

In the local setup the node is set to `tcp://localhost:26657`. You can view your node configuration with:

```bash
evmosd config \
--home ~/.tmp-evmosd
# Example Output
# {
# 	"chain-id": "evmos_9000-1",
# 	"keyring-backend": "test",
# 	"output": "text",
# 	"node": "tcp://localhost:26657",
# 	"broadcast-mode": "sync"
# }
```

You can set your node configuration to send requests to a different network by changing the endpoint with:

```bash
evmosd config node [tendermint-rpc-endpoint] \
--home ~/.tmp-evmosd
```

<!-- TODD Add Link to learn about more node configurations -->

#### Queries

You can query information on the blockchain using `evmosd query` (short `evmosd q`). To view the account balances by its
 address stored in the bank module, use:

```bash
evmosd q bank balances [adress] \
--home ~/.tmp-evmosd
# # Example Output
 Output:
# balances:
# - amount: "99999000000000000000002500"
#   denom: aevmos
```

To view other available query commands, use:

```bash
# for all Queries
evmosd q

# for querying commands in the bank module
evmosd q bank
```

#### Transactions

You can submit transactions to the network using `evmosd tx`. This creates, signs and broadcasts a tx in one command. To
 send tokens from an account in the keyring to another address with the bank module, use:

```bash
evmosd tx bank send [from_key_or_address] [to_address] [amount] \
--home ~/.tmp-evmosd \
--fees 50000000000aevmos \
-b block

# Example Output:
# ...
# txhash: 7BA2618295B789CC24BB13E654D9187CDD264F61FC446EB756EAC07AF3E7C40A
```

To view other available transaction commands, use:

```bash
# for all transaction commands
evmosd tx

# for Bank transaction subcommands
evmosd tx bank
```

<!-- TODO add CTA for

- Academy
- Node configurations
- Manual node setup
- Running Validator node
-  -->