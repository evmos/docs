---
sidebar_position: 11
---
# Transactions

A transaction refers to an action initiated by an account which changes the state of the blockchain.
To effectively perform the state change, every transaction needs to be broadcasted to the whole network.
Any node can broadcast a request for a transaction to be executed on the blockchain state machine;
after this happens, a validator will validate, execute the transaction and propagate the resulting state change
to the rest of the network.

Computation resources on the network are consumed to process every transaction.
Thus, the concept of "gas" arises as a reference to the computation required to process the transaction by a validator.
Users have to pay a fee for this computation, all transactions require an associated fee.
This fee is calculated based on the gas required to execute the transaction and the gas price.

Additionally, a transaction needs to be signed using the sender's private key.
This proves that the transaction could only have come from the sender and was not sent fraudulently.

In a nutshell, the transaction lifecycle once a signed transaction is submitted to the network is the following:

- A transaction hash is cryptographically generated.
- The transaction is broadcasted to the network and added to a transaction pool consisting of all other pending network transactions.
- A validator must pick your transaction and include it in a block in order to verify the transaction and consider it "successful".

For a more detailed explanation of the transaction lifecyle, see [the corresponding section](https://docs.cosmos.network/main/basics/tx-lifecycle).

The transaction hash is a unique identifier and can be used to check transaction information,
for example, the events emitted, if was successful or not.

Transactions can fail for various reasons.
For example, the provided gas or fees may be insufficient.
Also, the transaction validation may fail.
Each transaction has specific conditions that must fullfil to be considered valid.
A widespread validation is that the sender is the transaction signer.
In such a case, if you send a transaction where the sender address is different than the signer's address,
the transation will fail, even if the fees are sufficient.

Evmos supports two transaction types:

1. Cosmos transactions
2. Ethereum transactions

Although most of the information included on both of these is similar,
there are differences among them.
In the following sections these are explained.

<!-- 
TODO: explain what transactions are on Evmos and blockchains. 
Explain that transactions can be identified by hashes and that they can 
contain multiple messages. Why can transactions fail? 

Explain that transactions can interoperate with other blockchains.
-->

## Transaction Confirmations

<!-- TODO: why are Ethereum transactions different than Cosmos -->

## Transaction Types

<!-- TODO: explain which transactions types does Evmos support (i.e modules and changes) and provide a few examples. -->

<!-- TODO: why are Ethereum transactions different than Cosmos -->

### Cosmos Transactions

On Cosmos chains, transactions are comprised of metadata held in contexts and sdk.Msgs
that trigger state changes within a module through the module's Protobuf Msg service.

When users want to interact with an application and make state changes (e.g. sending coins), they create transactions.
Each of a transaction's sdk.Msg must be signed using the private key associated with the appropriate account(s),
before the transaction is broadcasted to the network.

### Ethereum Transactions

Ethereum transactions refer to actions initiated by EOAs (externally-owned accounts, managed by humans),
rather than internal smart contract calls. Ethereum transactions transform the state of the EVM
and therefore must be broadcasted to the entire network.

Ethereum transactions also require a fee, known as `gas`. ([EIP-1559](https://eips.ethereum.org/EIPS/eip-1559))
introduced the idea of a base fee, along with a priority fee which serves as an incentive
for miners to include specific transactions in blocks.

There are several categories of Ethereum transactions:

- regular transactions: transactions from one account to another
- contract deployment transactions: transactions without a `to` address, where the contract code is sent in the `data` field
- execution of a contract: transactions that interact with a deployed smart contract,
  where the `to` address is the smart contract address

For more information on Ethereum transactions and the transaction lifecycle, [go here](https://ethereum.org/en/developers/docs/transactions/).

Evmos supports the following Ethereum transactions.

:::tip
**Note**: Unprotected legacy transactions are not supported by default.
:::

- Dynamic Fee Transactions ([EIP-1559](https://eips.ethereum.org/EIPS/eip-1559))
- Access List Transactions ([EIP-2930](https://eips.ethereum.org/EIPS/eip-2930))
- Legacy Transactions ([EIP-2718](https://eips.ethereum.org/EIPS/eip-2718))

### Interchain Transactions

<!-- TODO: transactions that use IBC or bridges to send them to other chains -->

## Transaction Receipts

<!-- TODO: explain Ethereum transaction receipts -->