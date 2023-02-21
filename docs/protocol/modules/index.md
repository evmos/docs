---
sidebar_position: 3
---

# List of Modules

Here is a list of all production-grade modules that can be used on the Evmos blockchain, along with their respective documentation:

- [claims](./claims/index.md) - Rewards status and claiming process for the mainnet release.
- [epochs](./epochs/index.md) - Executes custom state transitions every period (*aka* epoch).
- [erc20](./erc20/index.md) - Trustless, on-chain bidirectional internal conversion of tokens
  between Evmos' EVM and Cosmos runtimes.
- [evm](./evm/index.md) - Smart Contract deployment and execution on Cosmos
- [feemarket](./feemarket/index.md) - Fee market implementation based on the EIP1559 specification.
- [revenue](./revenue/index.md) - Split EVM transaction fees between block proposer and smart contract developers.
- [incentives](./incentives/index.md) - Incentivize user interaction with governance-approved smart contracts.
- [inflation](./inflation/index.md) - Mint tokens and allocate them to staking rewards,
  usage incentives and community pool.
- [vesting](./vesting/index.md) - Vesting accounts with lockup and clawback capabilities.

## Cosmos SDK

Evmos uses the following Cosmos SDK modules:

- [evidence](https://docs.cosmos.network/main/modules/evidence) - Evidence handling for double signing, misbehaviour, etc.
- [gov](https://docs.cosmos.network/main/modules/gov) - On-chain proposals and voting.
- [slashing](https://docs.cosmos.network/main/modules/slashing) - Validator punishment mechanisms.
- [staking](https://docs.cosmos.network/main/modules/staking) - Proof-of-Stake layer for public blockchains.
- [upgrade](https://docs.cosmos.network/main/modules/upgrade) - Software upgrades handling and coordination.

## IBC

Evmos uses the following the IBC modules for the SDK:

- [interchain-accounts](https://ibc.cosmos.network/main/apps/interchain-accounts/overview.html)
- [transfer](https://ibc.cosmos.network/main/apps/transfer/overview.html)