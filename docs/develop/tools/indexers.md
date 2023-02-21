---
sidebar_position: 5
---

# Indexers

A graph indexer allows developers to efficiently query the network for information about transactions, addresses,
and other data stored on the blockchain. This enables developers to build decentralized applications that can access
 and display the data in a meaningful way, without having to search through the entire blockchain for each query.

For example, a graph indexer could be used to search for all transactions associated with a particular address or to
 find all transactions that include a specific token. This type of indexing can greatly improve the speed and efficiency
  of decentralized applications and make it easier for users to access and analyze the data stored on the blockchain.

<!-- TODO Link the transactions to their right page -->

At Evmos, we have both Cosmos-based and EVM-based transactions and not all indexers provide both types of transactions.

## Graph

Transactions covered: `EVM`

The Graph is a decentralized open-source protocol for indexing blockchain protocol data and developers can create, publish,
and access indexed data through queries like GraphQL. Reach out to the team for an access key.

## Numia

Transactions covered: `EVM` and `Cosmos`

Numia Data indexes the EVM and Cosmos transactions and provide the users with SQL to query. Numia leverages Google BigQuery
as an intermediary data hosting service to leverage powerful tooling and convenience. In order to utilize Numia Data, users
will need to create a Google Cloud Platform (GCP) account and use BigQuery. Head over to the 
[Numia's Page on Evmos](https://docs.numia.xyz/using-numia/chains/evmos) to discover the latest fields and attributes.

## Covalent

Transactions covered: `EVM`

Covalent indexes over [80 EVM chains](https://www.covalenthq.com/docs/networks/) and provides an unifying experience through
an API. 