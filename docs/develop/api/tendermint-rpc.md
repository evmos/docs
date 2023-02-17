---
sidebar_position: 4
---

# Tendermint RPC

Query transactions, blocks, consensus state, broadcast transactions, etc.

https://docs.tendermint.com/v0.34/rpc/

## Tendermint Websocket

Tendermint Core provides a Websocket connection to subscribe or unsubscribe to Tendermint ABCI events.

:::tip
For more info about how to subscribe to events, please refer to the official [Tendermint documentation](https://docs.tendermint.com/v0.34/tendermint-core/subscription.html).
:::

```json
{
    "jsonrpc": "2.0",
    "method": "subscribe",
    "id": "0",
    "params": {
        "query": "tm.event='<event_value>' AND eventType.eventAttribute='<attribute_value>'"
    }
}
```

### List of Tendermint Events

The main events you can subscribe to are:

- `NewBlock`: Contains `events` triggered during `BeginBlock` and `EndBlock`.
- `Tx`: Contains `events` triggered during `DeliverTx` (i.e. transaction processing).
- `ValidatorSetUpdates`: Contains validator set updates for the block.

:::tip
👉 The list of events types and values for each Cosmos SDK module can be found in the [Modules Specification](./../../../../protocol/modules/) section.
Check the `Events` page to obtain the event list of each supported module on Evmos.
:::

List of all Tendermint event keys:

|                                                      | Event Type       | Categories  |
| ---------------------------------------------------- | ---------------- | ----------- |
| Subscribe to a specific event                        | `"tm.event"`     | `block`     |
| Subscribe to a specific transaction                  | `"tx.hash"`      | `block`     |
| Subscribe to transactions at a specific block height | `"tx.height"`    | `block`     |
| Index `BeginBlock` and `Endblock` events             | `"block.height"` | `block`     |
| Subscribe to ABCI `BeginBlock` events                | `"begin_block"`  | `block`     |
| Subscribe to ABCI `EndBlock` events                  | `"end_block"`    | `consensus` |

Below is a list of values that you can use to subscribe for the `tm.event` type:

|                        | Event Value             | Categories  |
| ---------------------- | ----------------------- | ----------- |
| New block              | `"NewBlock"`            | `block`     |
| New block header       | `"NewBlockHeader"`      | `block`     |
| New Byzantine Evidence | `"NewEvidence"`         | `block`     |
| New transaction        | `"Tx"`                  | `block`     |
| Validator set updated  | `"ValidatorSetUpdates"` | `block`     |
| Block sync status      | `"BlockSyncStatus"`     | `consensus` |
| lock                   | `"Lock"`                | `consensus` |
| New consensus round    | `"NewRound"`            | `consensus` |
| Polka                  | `"Polka"`               | `consensus` |
| Relock                 | `"Relock"`              | `consensus` |
| State sync status      | `"StateSyncStatus"`     | `consensus` |
| Timeout propose        | `"TimeoutPropose"`      | `consensus` |
| Timeout wait           | `"TimeoutWait"`         | `consensus` |
| Unlock                 | `"Unlock"`              | `consensus` |
| Block is valid         | `"ValidBlock"`          | `consensus` |
| Consensus vote         | `"Vote"`                | `consensus` |

### Example

```bash
ws ws://localhost:26657/websocket
> { "jsonrpc": "2.0", "method": "subscribe", "params": ["tm.event='ValidatorSetUpdates'"], "id": 1 }
```

Example response:

```json
{
    "jsonrpc": "2.0",
    "id": 0,
    "result": {
        "query": "tm.event='ValidatorSetUpdates'",
        "data": {
            "type": "tendermint/event/ValidatorSetUpdates",
            "value": {
              "validator_updates": [
                {
                  "address": "09EAD022FD25DE3A02E64B0FE9610B1417183EE4",
                  "pub_key": {
                    "type": "tendermint/PubKeyEd25519",
                    "value": "ww0z4WaZ0Xg+YI10w43wTWbBmM3dpVza4mmSQYsd0ck="
                  },
                  "voting_power": "10",
                  "proposer_priority": "0"
                }
              ]
            }
        }
    }
}
```



:::tip
**Note:** When querying Ethereum transactions versus Cosmos transactions, the transaction hashes are different.
When querying Ethereum transactions, users need to use event query.
Here's an example with the CLI:

```bash
curl -X GET "http://localhost:26657/tx_search?query=ethereum_tx.ethereumTxHash%3D0x8d43464891fac6c113e809e14dff1a3e608eae124d629799e42ca0e36562d9d7&prove=false&page=1&per_page=30&order_by=asc" -H "accept: application/json"
```
:::