---
sidebar_position: 2
---

# Oracles

Oracles are a crucial component of the decentralized web, enabling smart contracts to access off-chain data and interact
 with the real world.
These oracles serve as a bridge between the decentralized, trustless environment of blockchain and the centralized,
traditional internet.

An oracle is a piece of software that retrieves data from external sources and feeds it into smart contracts on the blockchain.
This enables smart contracts to respond to real-world events, trigger automated actions, and execute their intended functions.

Evmos partners with several oracles providers to help provide value feed services and more.

Our oracles include:

- [Adrastia](https://docs.adrastia.io/)
- [Dia](https://docs.diadata.org/introduction/readme)
- [SEDA Network](https://docs.seda.xyz/seda-network/introduction/the-oracle-problem) - Flux has renamed to SEDA Network
- [Redstone](https://docs.redstone.finance/docs/introduction)
- [Pyth](https://docs.pyth.network/)

``` sql
   +------------+         +------------+         +-------------+
   | External   |         |   Oracle   |         |  Smart      |
   | Data Source|         | Service    |         | Contract    |
   +------------+         +------------+         +-------------+
        |                       |                       |
        |  API Call             |                       |
        |---------------------> |                       |
        |                       |    Retrieve External  |
        |                       |    Data via API Call  |
        |                       |---------------------->|
        |                       |                       |
        |                       |    Use External Data  |
        |                       |    in Smart Contract  |
        |                       |<----------------------|
        |                       |                       |
        |                       |    Return Result to   |
        |                       |    Smart Contract     |
        |                       |<----------------------|
        |                       |                       |

```

In this diagram:

External Data Source refers to a source of data outside the blockchain network, such as a stock market, weather service,
 or other external API.

Oracle Service is a third-party service that acts as a bridge between the external data source and the smart contract.
 It retrieves the data from the external source and provides it to the smart contract.

Smart Contract is a self-executing contract that is deployed on the blockchain network. It uses the data provided by the
 oracle to perform certain actions, such as releasing funds or triggering events.

API Call refers to the request made by the smart contract to the oracle service, asking for the required external data.

Retrieve External Data refers to the process of retrieving the requested data from the external data source via the API call.

Use External Data refers to the process of using the retrieved data in the smart contract to perform actions, such as
condition checking and state changes.

Return Result refers to the process of returning the result of the action performed in the smart contract back to the oracle.

## Features of Oracles

- Data Feeds
    - Token
    - NFT
    - TradFi
- Randomness

## Partner Details

### Adrastia

Evmos data and contract address can be found [here](https://docs.adrastia.io/deployments/evmos).

The ultimate goal of Adrastia is to provide a decentralized and permissionless oracle network that is secure, reliable,
and easy to use. Anyone should be able to start a price feed for any asset by simply sending a transaction, provided
there is enough decentralized exchange (DEX) liquidity. Merely send the chain's gas token to an Adrastia contract, and
 a network of updater bots will start providing price feeds for that asset.

Evmos data feed can be found [here](https://adrastia.io/app/price-feeds/evmos).

Adrastia uses three types of contracts to provide secure data feeds. [These three](https://docs.adrastia.io/structure/contracts)
are:

1. Accumulators: At the lowest level, accumulators collect observations from various DEXs.
2. Intermediate oracles: Intermediate oracles use data from accumulators to collect, produce, and store derived data
such as time-weighted average price and liquidity at a single source.
3. Aggregator oracles: Aggregators combine data from multiple sources and reduce them to singular data points.

The interaction can be shown as a flow-chart below:

![adrastia-overview.png](/img/adrastia-overview.png)

### DIA

The DIA platform enables the sourcing, validation and sharing of transparent and verified data feeds for traditional and
 digital financial applications. DIA’s institutional-grade data feeds cover asset prices, metaverse data, lending rates
  and more.
DIA’s data is directly sourced from a broad array of on-chain and off-chain sources at individual trade-level. This
 allows DIA feeds to be fully customized with regards to the mix of sources and methodologies, resulting in tailor-made,
  high resilience feeds and thereby setting a new paradigm for oracles.

![dia-architecture.png](/img/dia-architecture.png)

The [Evmos](https://docs.diadata.org/documentation/oracle-documentation/deployed-contracts#evmos) Mainnet and Testnet
contract are available for use. The update frequency is 2 hours. To use their API, head over to [here](https://docs.diadata.org/documentation/api-1).

### Redstone

RedStone offers a radically different design of Oracles catering for the needs of modern Defi protocols.

- Data providers can avoid the requirement of continuous on-chain data delivery
- Allow end users to self-deliver signed Oracle data on-chain
- Use the decentralized Streamr network to deliver signed oracle data to the end users
- Use token incentives to motivate data providers to maintain data integrity and uninterrupted service
- Leverage the Arweave blockchain as a cheap and permanent storage for archiving Oracle data and maintaining data
providers' accountability

```
# Using yarn
yarn add @redstone-finance/evm-connector

# Using NPM
npm install @redstone-finance/evm-connector
```

Examples of Redstone EVM Connector can be found [here](https://github.com/redstone-finance/redstone-evm-connector-examples/blob/main/contracts/example-custom-urls.sol).

### Pyth

Pyth leverages over [70 first-party publishers](https://pyth.network/publishers) to publish financial market data to numerous blockchains.
They provide data feeds to various assets classes, such as [US equities, commodities, and cryptocurrencies](https://pyth.network/price-feeds/). The service has undergone several audits and more information can be found [here](https://github.com/pyth-network/audit-reports).

- [Developer Docs](https://docs.pyth.network/)
- [Pyth Client for Linux](https://github.com/pyth-network/pyth-client)
- [Pyth TS client NPM](https://www.npmjs.com/package/@pythnetwork/client)

### SEDA network

[SEDA Rust library](https://github.com/sedaprotocol/seda-rust)

Going beyond today’s definition of an oracle, SEDA is a multi-chain-native data transmission protocol built on an
entirely decentralized foundation. The SEDA network is a Proof-of-Stake on-chain data provision solution that
allows anyone to provide and access high-quality data on all blockchain networks. It is a living market and transport
layer that enables access and flow for any type of data through a transparent and secure medium, free of centralized intermediaries.
