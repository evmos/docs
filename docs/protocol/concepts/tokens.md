---
sidebar_position: 11
---

# Tokens

Tokens represent a digital asset that functions on a blockchain, while coins represent a cryptocurrency that can be
exchanged and used as a medium of exchange.

Evmos uses [Atto](https://en.wikipedia.org/wiki/Atto-) EVMOS as the base denomination to maintain parity with Ethereum.

1 evmos = 10<sup>18</sup> aevmos

This matches Ethereum denomination of:

1 ETH = 10<sup>18</sup> wei

### Cosmos Coins

Accounts can own Cosmos coins in their balance, which are used for operations with other Cosmos and transactions. Examples
of these are using the coins for staking, IBC transfers, governance deposits and EVM.

### EVM Tokens

Evmos is compatible with ERC20 tokens and other non-fungible token standards (EIP721, EIP1155)
that are natively supported by the EVM.

## Evmos Assets Page

Check out how we represent ERC-20 tokens and Cosmos IBC Coins through our [Single Token Representation](https://app.evmos.org/assets)
feature on the Evmos Dashboard.

![evmos-dashboard-assets])(/img/dashboard-assets.png)

## Registration

Any non-native coins coming over via IBC and need an ERC-20 representation can look into
our process. [This](https://academy.evmos.org/developers/guides/erc20-registration) document will detail how to go
through governance. On the other hand, if you already have the ERC-20 token representation and need an
IBC representation, then head over to [here](https://academy.evmos.org/developers/guides/cosmos-coin-registration)
to discover more.
