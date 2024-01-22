---
sidebar_position: 2
---

# Stride Outpost

[The Stride Outpost](https://app.evmos.org/dapps/staking/stride) is an Outpost that leverages 
the [IBC Transfer Extension](https://docs.evmos.org/develop/smart-contracts/evm-extensions/ibc-transfer) to interact 
with the [Autopilot](https://docs.stride.zone/docs/integrate-liquid-staking) feature of the Stride protocol. 
It simplifies using Stride Autopilot for liquid staking and claiming EVMOS tokens with a single transaction 
and helps return stEVMOS back to the Evmos chain. This Outpost automatically builds the correct packet data so users
can easily interact with the Stride protocol without leaving the Evmos chain.

## Key Components

- **`memo` field**: An extra JSON string attached to IBC Transfer packets. This additional information helps 
the Stride Autopilot to identify the user and action to be performed.


- **IBC Extension**: A precompiled contract that allows users to send IBC transfers to other chains through the EVM.


- **ICS20 Transfers**: Protocol for transferring fungible tokens using Inter-Blockchain Communication (IBC).


- **Stride Autopilot Middleware**: A module simplifying user steps for using Stride services like liquid staking 
and redeeming.

## How it works
Users can interact with the Stride Outpost directly using the Stride instant dApp
from the [Evmos dApp store](https://app.evmos.org/dapps/staking/stride). The dApp will automatically build 
the correct `memo` field for the user and send the IBC transfer to the Stride chain. The possible actions are:

1. **Liquid Stake** - Stake EVMOS tokens and receive stEVMOS tokens in return.

2. **Redeem** - Unstake stEVMOS tokens and receive EVMOS tokens back within 14-16 days. Check
the Stride documentation for more info on [redeeming](https://docs.stride.zone/docs/unstaking).


## Fallback Mechanism
The Stride Outpost has a fallback mechanism in case the Autopilot middleware is not available or is not working
correctly. This is why each IBC Transfer is send to a specific address on the Stride chain. This address is 
a multi-sig account that will return any stuck funds to the original sender. 

## For Developers
If you are a developer and want to integrate the Stride Outpost into your dApp, you can find 
an example Solidity Outpost implementation on our 
extension repo [here](https://github.com/evmos/extensions/tree/main/outposts/stride)