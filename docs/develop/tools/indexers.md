---
sidebar_position: 5
---

# Indexers

A graph indexer allows developers to efficiently query the network for information about transactions, addresses, and
other data stored on the blockchain. This enables developers to build decentralized applications that can access and
display the data in a meaningful way, without having to search through the entire blockchain for each query.

For example, a graph indexer could be used to search for all transactions associated with a particular address or to
find all transactions that include a specific token. This type of indexing can greatly improve the speed and efficiency
of decentralized applications and make it easier for users to access and analyze the data stored on the blockchain.

## Covalent

Covalent is an indexing service that provides a unified API for accessing data from multiple blockchain
networks. Covalent's API allows developers to access rich, structured blockchain data in a simple and efficient manner.
Covalent provides indexes service for all EVM transactions on Evmos. They have data set of over 60 blockchains. Covalent
provides an easy interface to query data via APIs.

- Get an [API Key](https://www.covalenthq.com/platform/#/auth/register/)
- [Docs](https://www.covalenthq.com/docs/api/#/0/0/USD/1)
- Cost: Free to use with 100,000 credits to use their API endpoints.

## Numia

Numia is a public good service that indexes various chains on the Cosmos ecosystem. For Evmos, Numia indexes both
EVM and Cosmos transactions. The service runs on Google BigQuery and requires users to sign up for their own accounts.

:::note
[Google Cloud](https://cloud.google.com/) provides free trial with ample credits ($300) to run many queries for
at least a few months.
:::

- [Get started with GCP instruction](https://docs.numia.xyz/using-numia/getting-started-with-gcp)
- [Pulling Numia Data Image](https://docs.numia.xyz/using-numia/querying-numia-datasets)
- [Evmos chain](https://docs.numia.xyz/using-numia/chains/evmos)
