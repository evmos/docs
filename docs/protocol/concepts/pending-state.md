---
sidebar_position: 10
---

# Pending State

When a transaction is submitted to the Ethereum network, it first goes into the pending status, waiting to be executed
by the nodes. A transaction can be in the pending state for a longer duration if the gas price is set very low in the
transaction and the nodes are busy processing other higher gas price transactions.

During the pending state, the transaction initiator is allowed to change the transaction fields at any time. They can do
so by sending another transaction with the same nonce.

## Prerequisite Readings

- [Cosmos SDK Mempool](https://docs.cosmos.network/main/building-apps/app-mempool)

## Evmos vs Ethereum

In Ethereum, pending blocks are generated as they are queued for production by miners. These pending
blocks include pending transactions that are picked out by miners, based on the highest reward paid
in gas. This mechanism exists as block finality is not possible on the Ethereum network. Blocks are
committed with probabilistic finality, which means that transactions and blocks become less likely
to become reverted as more time (and blocks) passes.

Evmos is designed quite differently on this front as there is no concept of a "pending state".
Evmos uses [Tendermint Core](https://docs.tendermint.com/) BFT consensus which provides instant
finality for transaction. For this reason, Ethermint does not require a pending state mechanism, as
all (if not most) of the transactions will be committed to the next block (avg. block time on Cosmos chains is ~8s).
However, this causes a
few hiccups in terms of the Ethereum Web3-compatible queries that can be made to pending state.

Another significant difference with Ethereum, is that blocks are produced by validators or block producers, who include
transactions from their local mempool into blocks in a
first-in-first-out (FIFO) fashion. Transactions on Evmos cannot be ordered or cherry picked out from the Tendermint node
[mempool](https://docs.tendermint.com/v0.34/tendermint-core/mempool.html).

## Pending State Queries

Evmos will make queries which will account for any unconfirmed transactions present in a node's
transaction mempool. A pending state query made will be subjective and the query will be made on the
target node's mempool. Thus, the pending state will not be the same for the same query to two
different nodes.

### JSON-RPC Calls on Pending Transactions

- [`eth_getBalance`](./../../develop/api/ethereum-json-rpc/methods#eth_getbalance)
- [`eth_getTransactionCount`](./../../develop/api/ethereum-json-rpc/methods#eth_gettransactioncount)
- [`eth_getBlockTransactionCountByNumber`](./../../develop/api/ethereum-json-rpc/methods#eth_getblocktransactioncountbynumber)
- [`eth_getBlockByNumber`](./../../develop/api/ethereum-json-rpc/methods#eth_getblockbynumber)
- [`eth_getTransactionByHash`](./../../develop/api/ethereum-json-rpc/methods#eth_gettransactionbyhash)
- [`eth_getTransactionByBlockNumberAndIndex`](./../../develop/api/ethereum-json-rpc/methods#eth_gettransactionbyblockhashandindex)
- [`eth_sendTransaction`](./../../develop/api/ethereum-json-rpc/methods#eth_sendtransaction)
