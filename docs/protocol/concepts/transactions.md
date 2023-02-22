---
sidebar_position: 11
---
# Transactions

A transaction refers to an action initiated by an account which changes the state of the blockchain.
To effectively perform the state change, every transaction is broadcasted to the whole network.
Any node can broadcast a request for a transaction to be executed on the blockchain state machine;
after this happens, a validator will validate, execute the transaction and propagate the resulting state change
to the rest of the network.

To process every transaction, computation resources on the network are consumed.
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

Nowadays, transactions can not only perform state transitions on the chain in which are submitted,
but also can execute transactions on another blockchains.
Interchain transactions are possible through the [Inter-Blockchain Communication protocol (IBC)](https://ibcprotocol.org/).
Find a more detailed explanation on the section below.

## Transaction Types

Evmos supports two transaction types:

1. Cosmos transactions
2. Ethereum transactions

This is possible because Evmos uses the [Cosmos-SDK](https://docs.cosmos.network/main)
and implements the [Ethereum Virtual Machine](https://ethereum.org/en/developers/docs/evm/) as a module.
In this way, Evmos provides the features and functionalities of Ethereum and Cosmos chains combined, and more.

Although most of the information included on both of these transaction types is similar,
there are differences among them.
An important difference, is that Cosmos transactions allow multiple messages on the same transaction.
Conversely, Ethereum transactions don't have this possibility.
To bring these two types together, Evmos implements Ethereum transactions as a single [`sdk.Msg`](https://godoc.org/github.com/cosmos/cosmos-sdk/types#Msg)
contained in an [`auth.StdTx`](https://pkg.go.dev/github.com/cosmos/cosmos-sdk/x/auth#StdTx).
All relevant Ethereum transaction information is contained in this message.
This includes the signature, gas, payload, etc.

Find more information about these two types on the following sections.

### Cosmos Transactions

On Cosmos chains, transactions are comprised of metadata held in contexts and `sdk.Msg`s
that trigger state changes within a module through the module's Protobuf [Msg service](https://docs.cosmos.network/main/building-modules/msg-services).

When users want to interact with an application and make state changes (e.g. sending coins), they create transactions.
Cosmos transactions can have multiple `sdk.Msg`s.
Each of these must be signed using the private key associated with the appropriate account(s),
before the transaction is broadcasted to the network.

A Cosmos transaction includes the following information:

- `Msgs`: an array of msgs (`sdk.Msg`)
- `GasLimit`: option chosen by the users for how to calculate how much gas they will need to pay
- `FeeAmount`: max amount user is willing to pay in fees
- `TimeoutHeight`: block height until which the transaction is valid
- `Signatures`: array of signatures from all signers of the tx
- `Memo`: a note or comment to send with the transaction

To submit a Cosmos transaction, users must use one of the provided clients.

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

An Ethereum transaction includes the following information:

- `recipient`: receiving address
- `signature`: sender's signature
- `nonce`: counter of tx number from account
- `value`: amount of ETH to transfer (in wei)
- `data`: include arbitrary data. Used when deploying a smart contract or making a smart contract method call
- `gasLimit`: max amount of gas to be consumed
- `maxPriorityFeePerGas`: mas gas to be included as tip to validators
- `maxFeePerGas`: max amount of gas to be paid for tx

For more information on Ethereum transactions and the transaction lifecycle, [go here](https://ethereum.org/en/developers/docs/transactions/).

Evmos supports the following Ethereum transactions.

:::tip
**Note**: Unprotected legacy transactions are not supported by default.
:::

- Dynamic Fee Transactions ([EIP-1559](https://eips.ethereum.org/EIPS/eip-1559))
- Access List Transactions ([EIP-2930](https://eips.ethereum.org/EIPS/eip-2930))
- Legacy Transactions ([EIP-2718](https://eips.ethereum.org/EIPS/eip-2718))

Evmos is capable of processing Ethereum transactions by wrapping them on a `sdk.Msg`.
Evmos achieves this by using the `MsgEthereumTx`.
This message encapsulates an Ethereum transaction as an SDK message and contains the necessary transaction data fields.

One remark about the `MsgEthereumTx` is that it implements both the `sdk.Msg` and `sdk.Tx` interfaces
(generally SDK messages only implement the former, while the latter is a group of messages bundled together).
The reason of this, is because the `MsgEthereumTx` must not be included in a `auth.StdTx`
(SDK's standard transaction type) as it performs gas and fee checks using the Ethereum logic
from Geth instead of the Cosmos SDK checks done on the auth module `AnteHandler`.

### Interchain Transactions

<!-- TODO: transactions that use IBC or bridges to send them to other chains -->

## Transaction Receipts

A transaction receipt shows data returned by an Ethereum client to represent the result of a particular transaction,
including a hash of the transaction, its block number, the amount of gas used, and,
in case of deployment of a smart contract, the address of the contract.
Additionally, it includes custom information from the events emitted in the smart contract.

A receipt contains the following information:

- `transactionHash` : hash of the transaction.
- `transactionIndex`: integer of the transactions index position in the block.
- `blockHash`: hash of the block where this transaction was in.
- `blockNumber`: block number where this transaction was in.
- `from`: address of the sender.
- `to`: address of the receiver. null when its a contract creation transaction.
- `cumulativeGasUsed` : The total amount of gas used when this transaction was executed in the block.
- `effectiveGasPrice` : The sum of the base fee and tip paid per unit of gas.
- `gasUsed` : The amount of gas used by this specific transaction alone.
- `contractAddress` : The contract address created, if the transaction was a contract creation, otherwise null.
- `logs`: Array of log objects, which this transaction generated.
- `logsBloom`: Bloom filter for light clients to quickly retrieve related logs.
- `type`: integer of the transaction type, 0x00 for legacy transactions, 0x01 for access list types,
  0x02 for dynamic fees. It also returns either.
- `root` : transaction stateroot (pre Byzantium)
- `status`: either 1 (success) or 0 (failure)
