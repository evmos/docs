---
sidebar_position: 6
---

# Metrics

Evmos nodes can enable [Cosmos SDK telemetry](https://docs.cosmos.network/main/learn/advanced/telemetry)
to allow for observing and gathering insights about the Evmos application.
Under the hood, it uses the [`go-metrics`](https://github.com/hashicorp/go-metrics) package
and the Prometheus client library to expose different [types of metrics](https://prometheus.io/docs/concepts/metric_types/)
like gauges and counters.
For best practices on how to use different metrics types,
check this [blog article](https://blog.pvincent.io/2017/12/prometheus-blog-series-part-2-metric-types/).

Find below a list of supported Evmos modules with custom metrics and telemetry.
Using the metrics you can e.g. run performance profiles
and display them in a [Grafana](https://grafana.com/) dashboard.

## Supported Metrics

| Metric                                         | Description                                                                                                  | Unit     | Type      |
| :--------------------------------------------- | :----------------------------------------------------------------------------------------------------------- | :------- | :-------- |
| `feemarket_base_fee`                           | Amount of base fee per EIP-1559 block                                                                        | token    | gauge     |
| `feemarket_block_gas`                          | Amount of gas used in an EIP-1559 block                                                                      | token    | gauge     |
| `erc20_ibc_on_recv_total`                      | Total amount of times an IBC coin was autoconverted to an ERC20 token in the ibc `onRecvPacket` callback     | transfer | counter   |
| `erc20_ibc_err_total`                          | Total amount of times an IBC coin autoconvertion to ERC20 token failed during an ibc transaction             | transfer | counter   |
| `erc20_ibc_transfer_total`                     | Total amount of times an IBC coin or its ERC20 representation was transferred via ibc (outgoing transaction) | transfer | counter   |
| `tx_msg_convert_coin_amount_total`             | Total amount of converted coins using a `ConvertCoin` msg                                                    | token    | counter   |
| `tx_msg_convert_coin_total`                    | Total number of txs with a `ConvertCoin` msg                                                                 | tx       | counter   |
| `tx_msg_convert_erc20_amount_total`            | Total amount of converted erc20 using a `ConvertERC20` msg                                                   | token    | counter   |
| `tx_msg_convert_erc20_total`                   | Total number of txs with a `ConvertERC20` msg                                                                | tx       | counter   |
| `tx_msg_ethereum_tx_total`                     | Total number of txs processed via the EVM                                                                    | tx       | counter   |
| `tx_msg_ethereum_tx_gas_used_total`            | Total amount of gas used by an ethereum tx                                                                   | gas      | counter   |
| `tx_msg_ethereum_tx_gas_limit_per_gas_used`    | Ratio of gas limit to gas used for an ethereum tx                                                            | ratio    | gauge     |
| `tx_msg_ethereum_tx_incentives_total`          | Total number of txs with an incentivized contract processed via the EVM                                      | tx       | counter   |
| `tx_msg_ethereum_tx_incentives_gas_used_total` | Total amount of gas used by txs with an incentivized contract processed via the EVM                          | gas      | counter   |
| `inflation_allocate_total`                     | Total amount of tokens allocated through inflation                                                           | token    | counter   |
| `inflation_allocate_staking_total`             | Total amount of tokens allocated through inflation to staking                                                | token    | counter   |
| `inflation_allocate_incentives_total`          | Total amount of tokens allocated through inflation to incentives                                             | token    | counter   |
| `inflation_allocate_community_pool_total`      | Total amount of tokens allocated through inflation to community pool                                         | token    | counter   |
| `tx_create_clawback_vesting_account_gas_used`  | Total amount of gas used by a `CreateClawbackVestingAccount` msg                                             | gas      | counter   |
| `tx_fund_vesting_account_gas_used`             | Total amount of gas used by a `FundVestingAccount` msg                                                       | gas      | counter   |
| `tx_clawback_gas_used`                         | Total amount of gas used by a `Clawback` msg                                                                 | gas      | counter   |
| `tx_update_vesting_funder_gas_used`            | Total amount of gas used by a `UpdateVestingFunder` msg                                                      | gas      | counter   |
| `epochs_begin_blocker`                         | Time spent during `BeginBlocker` of the `x/epochs` module                                                    | ms       | histogram |
| `burned_tx_fee_amount`                         | Total amount of fees burned on a tx                                                                          | token    | counter   |
