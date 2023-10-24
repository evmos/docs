---
sidebar_position: 6
---

# CLI Commands

## CLI Flags

A list of commonly used flags of `evmosd` is listed below:

| Option              | Description                                   | Type            | Default Value             |
| ------------------- | --------------------------------------------- | --------------- | ------------------------- |
| `--chain-id`        | Full Chain ID                                 | `string`        | `""`                      |
| `--home`            | Directory for config and data                 | `string`        | `~/.evmosd`               |
| `--keyring-backend` | Select keyring's backend                      | `string`        | `"os"`                    |
| `--output`          | Output format                                 | `string`        | `"text"`                  |
| `--node`            | Tendermint RPC interface                      | `<host>:<port>` | `"tcp://localhost:26657"` |
| `--from`            | Name or address of account with which to sign | `string`        | `""`                      |

## Command list

A list of commonly used `evmosd` commands. You can obtain the full list by using the `evmosd -h` command.

| Command            | Description                                                     | Subcommands (example)                                                     |
| ------------------ | --------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `keys`             | Keys management                                                 | `list`, `show`, `add`, `add --recover`, `delete`                          |
| `tx`               | Transactions subcommands                                        | `bank send`, `ibc-transfer transfer`, `distribution withdraw-all-rewards` |
| `query`            | Query subcommands                                               | `bank balance`, `staking validators`, `gov proposals`                     |
| `tendermint`       | Tendermint subcommands                                          | `show-address`, `show-node-id`, `version`                                 |
| `config`           | Client configuration                                            |                                                                           |
| `init`             | Initialize full node                                            |                                                                           |
| `start`            | Run full node                                                   |                                                                           |
| `version`          | Evmos version                                                   |                                                                           |
| `validate-genesis` | Validates the genesis file                                      |                                                                           |
| `status`           | Query remote node for status                                    |                                                                           |
| `block`            | Query a specific block persisted in the db (defaults to latest) |                                                                           |
