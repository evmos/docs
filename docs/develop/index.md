---
sidebar_position: 0
---

# Introduction
<!--
Evmos is a Cosmos-based chain with full Ethereum Virtual Machine (EVM) support. Because of this [architecture](), tokens and assets in the network may come from different independent sources.

Evmos is a scalable, high-throughput Proof-of-Stake blockchain that is fully compatible and
interoperable with Ethereum. It's built using the [Cosmos SDK](https://github.com/cosmos/cosmos-sdk/) which runs on top of [Tendermint Core](https://github.com/tendermint/tendermint) consensus engine.

Evmos allows for running vanilla Ethereum as a [Cosmos](https://cosmos.network/)
application-specific blockchain. This allows developers to have all the desired features of
Ethereum, while at the same time, benefit from Tendermint’s Proof of Stake implementation. Also, because it is
built on top of the Cosmos SDK, it will be able to exchange value with the rest of the Cosmos
Ecosystem through the Inter Blockchain Communication Protocol (IBC).

## Features

Here’s a glance at some of the key features of Evmos:

* Web3 and EVM compatibility
* High throughput via [Tendermint Core](https://github.com/tendermint/tendermint)
* Horizontal scalability via [IBC](https://cosmos.network/ibc)
* Fast transaction finality

Evmos enables these key features by:

* Implementing Tendermint Core's Application Blockchain Interface ([ABCI](https://docs.tendermint.com/master/spec/abci/)) to manage the blockchain
* Leveraging [modules](https://docs.cosmos.network/main/building-modules/intro.html) and other mechanisms implemented by the [Cosmos SDK](https://docs.cosmos.network/).
* Utilizing [`geth`](https://github.com/ethereum/go-ethereum) as a library to promote code reuse and improve maintainability.
* Exposing a fully compatible Web3 [JSON-RPC](./apis/ethereum-JSON-RPC/JSON-RPC.md) layer for interacting with existing Ethereum clients and tooling ([Metamask](../use/connect-your-wallet/metamask.mdx), Remix, Truffle, etc). -->


<!-- The sum of these features allows developers to leverage existing Ethereum ecosystem tooling and
software to seamlessly deploy smart contracts which interact with the rest of the Cosmos
[ecosystem](https://cosmos.network/ecosystem)!

import ProjectValue from '../../src/components/ProjectValue.js';


## The EVMOS Token

The denomination used for staking, governance and gas consumption on the EVM is the EVMOS. The EVMOS provides the utility of: securing the Proof-of-Stake chain, token used for governance proposals, distribution of fees to validator and users, and as a mean of gas for running smart contracts on the EVM.

Evmos uses [Atto](https://en.wikipedia.org/wiki/Atto-) EVMOS as the base denomination to maintain parity with Ethereum.

1 evmos = 10<sup>18</sup> aevmos

This matches Ethereum denomination of:

1 ETH = 10<sup>18</sup> wei

## Cosmos Coins

Accounts can own Cosmos coins in their balance, which are used for operations with other Cosmos and transactions. Examples of these are using the coins for staking, IBC transfers, governance deposits and EVM.

## EVM Tokens

Evmos is compatible with ERC20 tokens and other non-fungible token standards (EIP721, EIP1155)
that are natively supported by the EVM.

## Quick Facts Table

| Property               | Value                                           |
| ---------------------- | ----------------------------------------------- |
| Evmos Testnet          | <ProjectValue keyword="testnet_chain_id" />     |
| Evmos Mainnet          | <ProjectValue keyword="chain_id" />             |
| Blockchain Explorer(s) | [List of Block Explorers](./tools/explorers.md) |
| Block Time             | `~2s`                                           | -->


<!--
## List of Resources

Please find the following resources for in-depth information:

- **[Networks & Connections](/develop/networks)**: List of publicly available endpoints.
- **[Evmos Clients](/develop/build-a-dApp/clients/ethereum-JSON-RPC/clients)**: Description of available clients.
- **[Block Explorers](/develop/build-a-dApp/tools/block-explorers)**: List of block explorers available for Evmos.
- **[Testnet Faucet](/develop/testnet/faucet)**: Explaination of faucet use to obtain testnet tokens.
- **Localnet**: Instructions on how to configure a local instance of the Evmos blockchain.
  - **[Single Node](develop/build-a-dApp/run-a-node/single-node)**: Run a single local node.
  - **[Multi Node](develop/build-a-dApp/run-a-node/multi-nodes)**: Run a local testnet with multiple nodes.
  - **[Testnet](develop/build-a-dApp/run-a-node/testnet-commands)**: Use the testnet command of the Evmos daemon.
- **Libraries**:
  - **[EvmosJS](develop/build-a-dApp/tools/evmosjs)**: Javascript library for Evmos.

### Remote Procedure Calls (RPCs)

As Evmos lives at the crossroads of Cosmos and Ethereum, there are RPC connections available for all corresponding interfaces:

- **[JSON-RPC Server](develop/build-a-dApp/clients/ethereum-JSON-RPC/JSON-RPC)**: General information about the JSON-RPC server provided by Evmos.
- **[Running The Server](develop/build-a-dApp/clients/ethereum-JSON-RPC/running-the-server)**: Instructions on how to set up the server when running a node.
- **[Namespaces](develop/build-a-dApp/clients/ethereum-JSON-RPC/namespaces)**: Description of the available JSON-RPC namespaces.
- **[JSON-RPC Methods](develop/build-a-dApp/clients/ethereum-JSON-RPC/JSON-RPC-methods)**: List of supported JSON-RPC endpoints and methods.
- **[Events](develop/build-a-dApp/clients/ethereum-JSON-RPC/events)**: Information about the available events and instructions to subscribe to them.
- **[Cosmos gRPC & REST](https://api.evmos.org/)**: Documentation of the available gRPC implementation on Evmos.
- **[Tendermint RPC](https://docs.tendermint.com/v0.34/rpc/)**: Documentation for the RPC protocols supported by Tendermint.

### Tutorials For Ethereum Developers

TODO: Redirect learnings & Guides to ACADEMY -->
