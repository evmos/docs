# Oracles

Evmos supports several oracle providers to enable smart contracts to access
off-chain data and interact with the real world (e.g. price feeds or
randomness). These oracles serve as a bridge between the decentralized,
trustless environment of blockchain and the centralized, traditional internet.

An oracle is a piece of software that retrieves data from external sources and feeds it into smart contracts on the blockchain.
This enables smart contracts to respond to real-world events, trigger automated actions, and execute their intended functions.

## List of Oracles

### Mainnet

| Service      | Description                                                                                                                                                                                                                                                                                                                                      | Links & Features                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **[Pyth](https://docs.pyth.network/)**     | Leverages over [70 first-party publishers](https://pyth.network/publishers) to publish financial market data to numerous blockchains. They provide data feeds to various assets classes, such as [US equities, commodities, and cryptocurrencies](https://pyth.network/price-feeds/).                                                            | <ul><li>[Developer Docs](https://docs.pyth.network/)</li><li>[Pyth Client for Linux](https://github.com/pyth-network/pyth-client)</li><li>[Pyth TS client NPM](https://www.npmjs.com/package/@pythnetwork/client)</li><li>Find audit reports [here](https://github.com/pyth-network/audit-reports)</li></ul>                                                                                                                                                                                                                                                                                                                                                                                                    |
| **[Adrastia](https://docs.adrastia.io/)** | Provides a decentralized and permissionless oracle network that is secure, reliable, and easy to use. It uses [three types of contracts](https://docs.adrastia.io/structure/contracts) to provide secure data feeds: Accumulators, Intermediate oracles & Aggregator oracles                                                                     | <ul><li>Evmos data and contract address can be found [here](https://docs.adrastia.io/deployments/evmos)</li></ul>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **[DIA](https://docs.diadata.org/introduction/readme)**      | Enables the sourcing, validation and sharing of transparent and verified data feeds for traditional and digital financial applications. DIA’s institutional-grade data feeds cover asset prices, metaverse data, lending rates and more. Data is directly sourced from a broad array of on-chain and off-chain sources at individual trade-level | <ul><li>DIA feeds are fully customizable with regards to the mix of sources and methodologies, resulting in tailor-made, high resilience feeds</li><li>[Evmos](https://docs.diadata.org/documentation/oracle-documentation/deployed-contracts#evmos) Mainnet and Testnet contracts available for use. Update frequency is 2 hrs.</li><li>[Link to DIA's API](https://docs.diadata.org/products/token-price-feeds/access-api-endpoints/api-endpoints)</li><li>DIA has a [custom feed builder](https://app.diadata.org/feed-builder) and the supported token pairs are located [here](https://docs.diadata.org/documentation/oracle-documentation/deployed-contracts#evmos)</li><li>the [DIA team Discord](https://go.diadata.org/dev-discord)</li></ul>    |
| **[Redstone](https://docs.redstone.finance/docs/introduction)** | Offers a radically different design of Oracles catering for the needs of modern Defi protocols                                                                                                                                                                                                                                                   | <ul><li>Data providers can avoid the requirement of continuous on-chain data delivery</li><li>Allow end users to self-deliver signed Oracle data on-chain</li><li>Use the decentralized Streamr network to deliver signed oracle data to the end users</li><li>Use token incentives to motivate data providers to maintain data integrity and uninterrupted service</li><li>Leverage the Arweave blockchain as a cheap and permanent storage for archiving Oracle data and maintaining data providers' accountability</li><li>Examples of Redstone EVM Connector can be found [here](https://github.com/redstone-finance/redstone-evm-connector-examples/blob/main/contracts/example-custom-urls.sol)</li></ul> |
| **[SEDA Network](https://docs.seda.xyz/seda-network/introduction/the-oracle-problem)**     | A multi-chain-native data transmission protocol built on an entirely decentralized foundation. The SEDA network is a Proof-of-Stake on-chain data provision solution that allows anyone to provide and access high-quality data on all blockchain networks                                                                                       | <ul><li>[SEDA Chain](https://github.com/sedaprotocol/seda-chain)</li></ul>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |

## How do Oracles work?

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

* External Data Source refers to a source of data outside the blockchain network,
such as a stock market, weather service, or other external API.
* Oracle Service is a third-party service that acts as a bridge between the external data source and the smart contract.
It retrieves the data from the external source and provides it to the smart contract.
* Smart Contract is a self-executing contract that is deployed on the blockchain network.
It uses the data provided by the oracle to perform certain actions, such as releasing funds or triggering events.
* API Call refers to the request made by the smart contract to the oracle service, asking for the required external data.
* Retrieve External Data refers to the process of retrieving the requested data
from the external data source via the API call.
* Use External Data refers to the process of using the retrieved data in the smart contract to perform actions,
such as condition checking and state changes.
* Return Result refers to the process of returning the result of the action performed in the smart contract back to the oracle.
