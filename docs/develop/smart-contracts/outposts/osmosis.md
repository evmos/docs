---
sidebar_position: 1
---

# Osmosis Outpost

[The Osmosis Outpost](https://app.evmos.org/dapps/defi/osmosis) provides functionality that leverages
the [IBC Transfer Extension](https://docs.evmos.org/develop/smart-contracts/evm-extensions/ibc-transfer)
to interact with the Osmosis [IBC-hooks middleware](https://github.com/osmosis-labs/osmosis/tree/main/x/ibc-hooks) 
,the Osmosis SwapRouter and Cross Chain Swaps contract.
It provides an easy-to-use interface for executing token swaps between Osmosis and Evmos and routes them back to the
Evmos chain. 

## Key Components

- **`memo` field**: An extra JSON string attached to IBC Transfer packets. This additional information helps
  the IBC Hooks to identify the user and the swap being performed.
- **Osmosis IBC Hooks Middleware**: Middleware on Osmosis that interprets the memo field for specific actions.
- **Osmosis SwapRouter**: A contract that manages routes to pools on Osmosis, defining how tokens are swapped.
- **Osmosis Cross-Chain Swap V1 (XCS)**: Handles processing of the memo field.
This executes token swaps or routes tokens to their destination chains.
Evmos has its own XCS contract deployed on the Osmosis chain. 
You can find it
[here](https://celatone.osmosis.zone/osmosis-1/contracts/osmo18rj46qcpr57m3qncrj9cuzm0gn3km08w5jxxlnw002c9y7xex5xsu74ytz).

## How it works

Users can interact with the Osmosis Outpost directly using the Osmosis Instant dApp
from the [Evmos dApp store](https://app.evmos.org/dapps/defi/osmosis). The dApp will automatically build
the correct `memo` field for the user and send the IBC transfer to the Osmosis chain. The possible actions are:

1. **Swap Osmosis for Evmos** - Send your Osmosis tokens to the Osmosis Outpost and receive Evmos tokens in return.
2. **Swap Evmos for Osmosis** - Send your Evmos tokens to the Osmosis Outpost and receive Osmosis tokens in return.

## Fallback Mechanism

The Osmosis Outpost has a fallback mechanism in case the IBC Hooks middleware is not working correctly.
This is why the `memo` field contains a special field called `local_recovery_addr` that will be used as a fallback
predetermined address in case of failures. This address is a multi-sig account controlled by the AP team
that will return any stuck funds to the original sender. 

## For Developers

If you are a developer and want to integrate the Osmosis Outpost into your dApp, you can find
an example Solidity Outpost implementation on our
extension repo [here](https://github.com/evmos/extensions/tree/main/outposts/osmosis)
