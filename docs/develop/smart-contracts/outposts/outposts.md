---
sidebar_position: 1
---

# Outposts

Outposts leverage the
[IBC Transfer Extension](https://docs.evmos.org/develop/smart-contracts/evm-extensions/ibc-transfer)
to interact with other chains through the creation of a custom `memo` field that holds instructions for the
reception chain. This allows users to interact with other chains without leaving the Evmos chain. Evmos supports
two outposts at the moment:

1. Osmosis Cross Chain Swaps Outpost
2. Stride Liquid Staking and Redeeming Outpost

## Key Components

### Common

- **`memo` field**: An extra JSON string attached to IBC Transfer packets. This additional information helps
  the receiving chain to identify the user and action to be performed.
- **IBC Extension**: A precompiled contract that allows users to send IBC transfers to other chains through the EVM.
- **ICS20 Transfers**: Protocol for transferring fungible tokens using Inter-Blockchain Communication (IBC).

### Stride Specific

- **Stride Autopilot Middleware**: A module simplifying user steps for using Stride services like liquid staking
  and redeeming.

### Osmosis Specific

- **Osmosis IBC Hooks Middleware**: Middleware on Osmosis that interprets the memo field for specific actions.
- **Osmosis SwapRouter**: A contract that manages routes to pools on Osmosis, defining how tokens are swapped.
- **Osmosis Cross-Chain Swap V1 (XCS)**: Handles processing of the memo field.
  This executes token swaps or routes tokens to their destination chains.
  Evmos has its own XCS contract deployed on the Osmosis chain.
  You can find it
  [here](https://celatone.osmosis.zone/osmosis-1/contracts/osmo18rj46qcpr57m3qncrj9cuzm0gn3km08w5jxxlnw002c9y7xex5xsu74ytz).

## Stride Outpost

[The Stride Outpost](https://app.evmos.org/dapps/staking/stride) interacts with the
[Autopilot](https://docs.stride.zone/docs/integrate-liquid-staking) middleware of the Stride protocol.
It simplifies using Stride Autopilot for liquid staking and claiming EVMOS tokens with a single transaction
and returns stEVMOS back to the Evmos chain. This Outpost automatically builds the correct packet data so users
can easily interact with the Stride protocol without leaving the Evmos chain.

Users can interact with the Stride Outpost directly using the Stride instant dApp
from the [Evmos dApp store](https://app.evmos.org/dapps/staking/stride). The dApp will automatically build
the correct `memo` field for the user and send the IBC transfer to the Stride chain. The possible actions are:

1. **Liquid Stake** - Stake EVMOS tokens and receive stEVMOS tokens in return.
2. **Redeem** - Unstake stEVMOS tokens and receive EVMOS tokens back within 14-16 days. Check
   the Stride documentation for more info on [redeeming](https://docs.stride.zone/docs/unstaking).

## Osmosis Outpost

[The Osmosis Outpost](https://app.evmos.org/dapps/defi/osmosis) interacts with the Osmosis
[IBC-hooks middleware](https://github.com/osmosis-labs/osmosis/tree/main/x/ibc-hooks), the Osmosis SwapRouter contract
and the Cross Chain Swaps contract. It provides an easy-to-use interface for executing token swaps between
Osmosis and Evmos and vice versa and routes them back to the Evmos chain.

Users can interact with the Osmosis Outpost directly using the Osmosis Instant dApp
from the [Evmos dApp store](https://app.evmos.org/dapps/defi/osmosis). The dApp will automatically build
the correct `memo` field for the user and send the IBC transfer to the Osmosis chain. The possible actions are:

1. **Swap Osmosis for Evmos** - Send your Osmosis tokens to the Osmosis Outpost and receive Evmos tokens in return.
2. **Swap Evmos for Osmosis** - Send your Evmos tokens to the Osmosis Outpost and receive Osmosis tokens in return.

## Fallback Mechanism

Each Outpost has a fallback mechanism in the extraordinary case of core protocol or middleware failures.
In case you do not receive your stEvmos back or your swap isn't executed make sure to contact the
mod team on Discord or Telegram and we will help you recover your funds.

### Stride

The Stride Outpost has a fallback mechanism in case the Autopilot middleware is not available or is not working
correctly. This is why each IBC Transfer is sent to a specific address on the Stride chain. This address is
a multi-sig account controlled by the AP team that will return any stuck funds to the original sender.

Stride Multi-sig: `stride1yzw585gd8ajymcaqt9e98k5tt66qpzspc93ghf`

- Vlad (Evmos Core Team): `stride1rhe5leyt5w0mcwd9rpp93zqn99yktsxvyaqgd0`
- Mr.Sir (Evmos Core Team): `stride1r4xzzuqewfwm4uckugcnt246xpjsv3a92epau2`
- Daniel (Evmos Core Team): `stride1wwc0fdes0y33czhg48yafmle0xpkfg860wkh9g`

### Osmosis

The Osmosis Outpost has a fallback mechanism in case the IBC Hooks middleware is not working correctly.
This is why the `memo` field contains a special field called `local_recovery_addr` that will be used as a fallback
predetermined address in case of failures. This address is a multi-sig account controlled by the AP team
that will return any stuck funds to the original sender.

Osmosis Multi-sig: `osmo1yzw585gd8ajymcaqt9e98k5tt66qpzspn4zy4h`

- Vlad (Evmos Core Team): `osmo1rhe5leyt5w0mcwd9rpp93zqn99yktsxv0dny03`
- Mr.Sir (Evmos Core Team): `osmo1r4xzzuqewfwm4uckugcnt246xpjsv3a9pfj375`
- Daniel (Evmos Core Team): `osmo1wwc0fdes0y33czhg48yafmle0xpkfg86y79m8k`

## For Developers

If you are a developer and want to integrate the Stride or Osmosis Outpost into your dApp, you can find
an example Solidity implementation on our extension repo:

1. [Osmosis Outpost](https://github.com/evmos/extensions/tree/main/outposts/osmosis)
2. [Stride Outpost](https://github.com/evmos/extensions/tree/main/outposts/stride)
