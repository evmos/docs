---
sidebar_position: 3
---

# List of Modules

Here is a list of all production-grade modules that can be used on the Evmos blockchain, along with their respective documentation:

- [epochs](epochs.md) - Executes custom state transitions every period (*aka* epoch).
- [erc20](erc20.md) - Trustless, on-chain bidirectional internal conversion of tokens
  between Evmos' EVM and Cosmos runtimes.
- [evm](evm.md) - Smart Contract deployment and execution on Cosmos
- [feemarket](feemarket.md) - Fee market implementation based on the EIP-1559 specification.
- [inflation](inflation.md) - Mint tokens and allocate them to staking rewards and the community pool.
- [vesting](vesting.md) - Vesting accounts with lockup and clawback capabilities.

## Cosmos SDK

Evmos uses the following Cosmos SDK modules:

- [auth](https://docs.cosmos.network/main/modules/auth) - Authentication of accounts and transactions for Cosmos SDK applications.
- [authz](https://docs.cosmos.network/main/modules/authz) -
Authorization for accounts to perform actions on behalf of other accounts.
- [bank](https://docs.cosmos.network/main/modules/bank) - Token transfer functionalities.
- [capability](https://ibc.cosmos.network/main/ibc/capability-module) - Object capability implementation.
- [distribution](https://docs.cosmos.network/main/modules/distribution) - Fee distribution, and staking token provision distribution.
- [evidence](https://docs.cosmos.network/main/modules/evidence) - Evidence handling for double signing, misbehaviour, etc.
- [feegrant](https://docs.cosmos.network/main/modules/feegrant) - Grant fee allowances for executing transactions.
- [genutil](https://github.com/cosmos/cosmos-sdk/tree/main/x/genutil) -
variety of genesis utility functionalities for usage within a blockchain application
- [gov](https://docs.cosmos.network/main/modules/gov) - On-chain proposals and voting.
- [params](https://docs.cosmos.network/main/modules/params) - Globally available parameter store.
- [slashing](https://docs.cosmos.network/main/modules/slashing) - Validator punishment mechanisms.
- [staking](https://docs.cosmos.network/main/modules/staking) - Proof-of-Stake layer for public blockchains.
- [upgrade](https://docs.cosmos.network/main/modules/upgrade) - Software upgrades handling and coordination.

## IBC

Evmos uses the following the IBC modules for the SDK:

- [interchain-accounts](https://ibc.cosmos.network/main/apps/interchain-accounts/overview.html)
- [transfer](https://ibc.cosmos.network/main/apps/transfer/overview.html)
