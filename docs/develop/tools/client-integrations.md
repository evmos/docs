---
sidebar_position: 6
---

# Evmos Client Integrations

Client integration libraries play a crucial role in blockchain technology by making it easier for developers to interact
with the blockchain network. Libraries abstract away complexities and provide integrations and methods to allow developers
to create product in a more consistent manner.

## Evmos-specific Client Integrations

Evmos-specific libraries are useful in aiding developers speed up development by providing interfaces, types, and methods
to signing, address converter (between `eth` and `evmos` addresses), and `EIP-712` transaction generator. There are two
library bindings, in Javascript/Typescript and Python.

- [EvmosJS](https://github.com/evmos/evmosjs) - is the official Evmos client Typescript library. This library contains
 several packages:
    - [Address Converter](https://www.npmjs.com/package/@evmos/address-converter)
    - [EIP-712](https://www.npmjs.com/package/@evmos/eip712)
    - [Proto](https://www.npmjs.com/package/@evmos/proto)
    - [Provider](https://www.npmjs.com/package/@evmos/provider)
    - [Transactions](https://www.npmjs.com/package/@evmos/transactions)
- [PyEvmos](https://github.com/sterliakov/pyevmos) - is a community-led Python library developed by [sterliakov](https://github.com/sterliakov)

## Ethereum Client Integrations

EthersJS and Web3JS are two most commonly used libraries in dApp development. Developer uses these libraries to interact
with blockchain and query JSON-RPC data, for example. Additionally, both of these libraries contain utilities to aid in
task like converting large numbers (BigNumber).

- [Ethers.js](https://docs.ethers.org/v5/) is the latest JS library that aims to be a complete and compact library for
interacting with the Ethereum Blockchain and its ecosystem.
- [web3js](https://web3js.readthedocs.io/en/v1.8.2/) is a collection of libraries that allow you to interact with a local
or remote ethereum node using HTTP, IPC or WebSocket.
