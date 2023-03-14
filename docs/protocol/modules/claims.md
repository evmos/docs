
# `claims`

## Abstract

This document specifies the internal `x/claims` module of the Evmos Hub.

The `x/claims` module is part of the Evmos [Rektdrop](https://evmos.blog/the-evmos-rektdrop-abbe931ba823)
and aims to increase the distribution of the network tokens to a large number of users.

Users are assigned with an initial amount of tokens from the airdrop allocation,
and then are able to automatically claim higher percentages as they perform certain tasks on-chain.

For the Evmos Rektdrop, users are required to claim their airdrop by participating in core network activities.
A Rektdrop recipient has to perform the following activities to get the allocated tokens:

* 25% is claimed by staking
* 25% is claimed by voting in governance
* 25% is claimed by using the EVM (deploy or interact with contract, transfer EVMOS through a web3 wallet)
* 25% is claimed by sending or receiving an IBC transfer

Furthermore, these claimable assets 'expire' if not claimed.
Users have two months (`DurationUntilDecay`) to claim their full airdrop amount.
After two months, the reward amount available will decline over 1 month (`DurationOfDecay`) in real time,
until it hits `0%` at 3 months from launch (`DurationUntilDecay + DurationOfDecay`).

# Contents

1. **[Concepts](#concepts)**
2. **[State](#state)**
3. **[State Transitions](#state-transitions)**
4. **[Hooks](#hooks)**
5. **[Events](#events)**
6. **[Parameters](#parameters)**
7. **[Clients](#clients)**

## Concepts

### Rektdrop

The Evmos [Rektdrop](https://evmos.blog/the-evmos-rektdrop-abbe931ba823) is the genesis airdrop
for the EVMOS token to Cosmos Hub, Osmosis and Ethereum users.

> The end goal of Evmos is to bring together the Cosmos and Ethereum community
and thus the Rektdrop has been designed to reward past participation in both networks under this theme of “getting rekt”.

The Rektdrop is the first airdrop that:

- Implements the [gasdrop](https://www.sunnya97.com/blog/gasdrop) mechanism by Sunny Aggarwal
- Covers the most number of chains and applications involved in an airdrop
- Airdrops to bridge users
- Includes reparations for users in exploits and negative market externalities (i.e. MEV)

The snapshot of the airdrop was on **November 25th, 2021 at 19:00 UTC**

### Actions

An `Action` corresponds to a given transaction that the user must perform to receive the allocated tokens from the airdrop.

There are 4 types of actions, each of which release 25% of their remaining corresponding airdrop allocation.
The 4 actions are as follows (`ActionUnspecified` is not considered for claiming):

```go
// UNSPECIFIED defines an invalid action. NOT claimable
ActionUnspecified Action = 0
// VOTE defines a proposal vote.
ActionVote Action = 1
// DELEGATE defines an staking delegation.
ActionDelegate Action = 2
// EVM defines an EVM transaction.
ActionEVM Action = 3
// IBC Transfer defines a fungible token transfer transaction via IBC.
ActionIBCTransfer Action = 4
```

These actions are monitored by registering claim post transaction **hooks** to the governance, staking, and EVM modules.
Once the user performs an action, the `x/claims` module will unlock the corresponding portion of the assets
and transfer them to the balance of the user.

These actions can be performed in any order and the claims module will not grant any additional tokens
after the corresponding action is performed.

#### Vote Action

After voting on a proposal, the corresponding proportion will be airdropped
to the user's balance by performing a transfer from the claim escrow account (`ModuleAccount`) to the user.

#### Staking (i.e Delegate) Action

After staking Evmos tokens (i.e delegating), the corresponding proportion will be airdropped to the user's balance
by performing a transfer from the claim escrow account (`ModuleAccount`) to the user.

#### EVM Action

If the user deploys or interacts with a smart contract (via an application or wallet integration),
the corresponding proportion will be airdropped to the user's balance by performing a transfer
from the claim escrow account (`ModuleAccount`) to the user.
This also applies when the user performs a transfer using Metamask or another web3 wallet of their preference.

#### IBC Transfer Action

If a user submits an IBC transfer to a recipient on a counterparty chain
or receives an IBC transfer from a counterparty chain,
the corresponding proportion will be airdropped to the user's balance submitting or receiving the transfer.

### Claim Records

A Claims Records is the metadata of claim data per address.
It keeps track of all the actions performed by the the user as well as the total amount of tokens allocated to them.
All users that have an address with a corresponding `ClaimRecord` are eligible to claim the airdrop.

### Claiming Process

As described in the [Actions](#actions) section, a user must submit transactions
to receive the allocated tokens from the airdrop.
However, since Evmos only supports Ethereum keys and not default Tendermint keys,
this process differs for Ethereum and Cosmos eligible users.

#### Ethereum Users

Evmos shares the coin type (`60`) and key derivation (Ethereum `secp256k1`) with Ethereum.
This allows users (EOA accounts) that have been allocated EVMOS tokens
to directly claim their tokens using their preferred web3 wallet.

#### Cosmos Hub and Osmosis Users

Cosmos Hub and Osmosis users who use the default Tendermint `secp256k1` keys,
need to perform a "cross-chain attestation" of their Evmos address.

This can be done by submitting an IBC transfer from Cosmos Hub and Osmosis,
which is signed by the addresses, that have been allocated the tokens.

The recipient Evmos address of this IBC transfer is the address, that the tokens will be airdropped to.

:::warning
**IMPORTANT**

Only submit an IBC transfer to an Evmos address that you own. Otherwise, you will lose your airdrop allocation.
:::

### Decay Period

A decay period defines the duration of the period during which the amount of claimable tokens
by the user decays decrease linearly over time.
It's goal is to incentivize users to claim their tokens and interact with the blockchain early.

The start is of this period is defined
as the sum of the `AirdropStartTime` and `DurationUntilDecay` parameter
and the duration of the linear decay is defined as `DurationOfDecay`, as described below:

```go
decayStartTime = AirdropStartTime + DurationUntilDecay
decayEndTime = decayStartTime + DurationOfDecay
```

By default, users have two months (`DurationUntilDecay`) to claim their full airdrop amount.
After two months, the reward amount available will decline over 1 month (`DurationOfDecay`) in real time,
until it hits `0%` at 3 months from launch (end).

### Airdrop Clawback

After the claim period ends, the tokens that were not claimed by users will be transferred to the community pool treasury.
In the same way, users with tokens allocated but no transactions (i.e nonce = 0),
will have their balance clawbacked to the community pool.


## State

### State Objects

The `x/claims` module keeps the following objects in state:

| State Object   | Description            | Key                           | Value                  | Store |
|----------------|------------------------|-------------------------------|------------------------|-------|
| `ClaimsRecord` | Claims record bytecode | `[]byte{1} + []byte(address)` | `[]byte{claimsRecord}` | KV    |

#### Claim Record

A `ClaimRecord` defines the initial claimable airdrop amount and the list of completed actions to claim the tokens.

```protobuf
message ClaimsRecord {
  // total initial claimable amount for the user
  string initial_claimable_amount = 1 [
    (gogoproto.customtype) = "github.com/cosmos/cosmos-sdk/types.Int",
    (gogoproto.nullable) = false
  ];
  // slice of the available actions completed
  repeated bool actions_completed = 2;
}
```

### Genesis State

The `x/claims` module's `GenesisState` defines the state necessary
for initializing the chain from a previously exported height.
It contains the module parameters and a slice containing all the claim records by user address:

```go
// GenesisState defines the claims module's genesis state.
type GenesisState struct {
	// params defines all the parameters of the module.
	Params Params `protobuf:"bytes,1,opt,name=params,proto3" json:"params"`
	// list of claim records with the corresponding airdrop recipient
	ClaimsRecords []ClaimsRecordAddress `protobuf:"bytes,2,rep,name=claims_records,json=claimsRecords,proto3" json:"claims_records"`
}
```

### Invariants

The `x/claims` module registers an [`Invariant`](https://docs.cosmos.network/main/building-modules/invariants)
to ensure that a property is true at any given time.
These functions are useful to detect bugs early on and act upon them to limit their potential consequences (e.g.
by halting the chain).

#### ClaimsInvariant

The `ClaimsInvariant` checks that the total amount of all unclaimed coins held
in claims records is equal to the escrowed balance held in the claims module
account. This is important to ensure that there are sufficient coins to claim for all claims records.

```go
balance := k.bankKeeper.GetBalance(ctx, moduleAccAddr, params.ClaimsDenom)
isInvariantBroken := !expectedUnclaimed.Equal(balance.Amount.ToDec())
```


## State Transitions

### ABCI

#### End Block

The ABCI EndBlock checks if the airdrop has ended in order to process the clawback of unclaimed tokens.

1. Check if the airdrop has concluded. This is the case if:
    - the global flag is enabled
    - the current block time is greater than the airdrop end time
2. Clawback tokens from the escrow account that holds the unclaimed tokens
   by transferring its balance to the community pool
3. Clawback tokens from empty user accounts
   by transferring the balance from empty user accounts with claims records to the community pool if:
    - the account is an ETH account
    - the account is not a vesting account
    - the account has a sequence number of 0, i.e. no transactions submitted, and
    - the balance amount is the same as the dust amount sent in genesis
    - the account does not have any other balances on other denominations except for the claims denominations.
4. Prune all the claim records from the state
5. Disable any further claim by setting the global parameter to `false`


## Hooks

The `x/claims` module implements transaction hooks for each of the four actions
from the `x/staking`, `x/gov` and  `x/evm` modules.
It also implements an IBC Middleware in order to claim the IBC transfer action
and to claim the tokens for Cosmos Hub and Osmosis users by migrating the claims record to the recipient address.

### Governance Hook - Vote Action

The user votes on a Governance proposal using their Evmos account.
Once the vote is successfully included, the claimable amount corresponding
to the vote action is transferred to the user address:

1. The user submits a `MsgVote`.
2. Begin claiming process for the `ActionVote`.
3. Check if the claims is allowed:
    - global parameter is enabled
    - current block time is before the end of the claims period
    - user has a claims record (i.e allocation) for the airdrop
    - user hasn't already claimed the action
    - claimable amount is greater than zero
4. Transfer the claimable amount from the escrow account to the user balance
5. Mark the `ActionVote` as completed on the claims record.
6. Update the claims record and retain it, even if all the actions have been claimed.

### Staking Hook - Delegate Action

The user delegates their EVMOS tokens to a validator.
Once the tokens are staked, the claimable amount corresponding to the delegate action is transferred to the user address:

1. The user submits a `MsgDelegate`.
2. Begin claiming process for the `ActionDelegate`.
3. Check if the claims is allowed:
    - global parameter is enabled
    - current block time is before the end of the claims period
    - user has a claims record (i.e allocation) for the airdrop
    - user hasn't already claimed the action
    - claimable amount is greater than zero
4. Transfer the claimable amount from the escrow account to the user balance
5. Mark the `ActionDelegate` as completed on the claims record.
6. Update the claims record and retain it, even if all the actions have been claimed.

### EVM Hook - EVM Action

The user deploys or interacts with a smart contract using their Evmos account or send a transfer using their Web3 wallet.
Once the EVM state transition is successfully processed,
the claimable amount corresponding to the EVM action is transferred to the user address:

1. The user submits a `MsgEthereumTx`.
2. Begin claiming process for the `ActionEVM`.
3. Check if the claims is allowed:
    - global parameter is enabled
    - current block time is before the end of the claims period
    - user has a claims record (i.e allocation) for the airdrop
    - user hasn't already claimed the action
    - claimable amount is greater than zero
4. Transfer the claimable amount from the escrow account to the user balance
5. Mark the `ActionEVM` as completed on the claims record.
6. Update the claims record and retain it, even if all the actions have been claimed.

### IBC Middleware - IBC Transfer Action

#### Send

The user submits an IBC transfer to a recipient in the destination chain.
Once the transfer acknowledgement package is received,
the claimable amount corresponding to the IBC transfer action is transferred to the user address:

1. The user submits a `MsgTransfer` to a recipient address in the destination chain.
2. The transfer packet is processed by the IBC ICS20 Transfer app module and relayed.
3. Once the packet acknowledgement is received, the IBC transfer module `OnAcknowledgementPacket` callback is executed.
   After which the claiming process for the `ActionIBCTransfer` begins.
4. Check if the claims is allowed:
    - global parameter is enabled
    - current block time is before the end of the claims period
    - user has a claims record (i.e allocation) for the airdrop
    - user hasn't already claimed the action
    - claimable amount is grater than zero
5. Transfer the claimable amount from the escrow account to the user balance
6. Mark the `ActionIBC` as completed on the claims record.
7. Update the claims record and retain it, even if all the actions have been claimed.

#### Receive

The user receives an IBC transfer from a counterparty chain.
If the transfer is successful,
the claimable amount corresponding to the IBC transfer action is transferred to the user address.
Additionally, if the sender address is Cosmos Hub or Osmosis address with an airdrop allocation,
the `ClaimsRecord` is merged with the recipient's claims record.

1. The user receives an packet containing an IBC transfer data.
2. The transfer is processed by the IBC ICS20 Transfer app module
3. Check if the claims is allowed:
    - global parameter is enabled
    - current block time is before the end of the claims period
4. Check if package is from a sent NON EVM channel and sender and recipient
   address are the same. If a packet is sent from a non-EVM chain, the sender
   addresss is not an ethereum key (i.e. `ethsecp256k1`). Thus, if
   `sameAddress` is true, the recipient address must be a non-ethereum key as
   well, which is not supported on Evmos. To prevent funds getting stuck,
   return an error, unless the destination channel from a connection to a chain
   is EVM-compatible or supports ethereum keys (eg: Cronos, Injective).
6. Check if destination channel is authorized to perform the IBC claim.
   Without this authorization the claiming process is vulerable to attacks.
7. Handle one of four cases by comparing sender and recipient addresses with each other
   and checking if either addresses have a claims record (i.e allocation) for the airdrop.
   To compare both addresses, the sender address's bech32 human readable prefix (HRP) is replaced with `evmos`.

    1. both sender and recipient are distinct and have a claims record ->
       merge sender's record with the recipient's record and claim actions that have been completed by one or the other
    2. only the sender has a claims record -> migrate the sender record to the recipient address and claim IBC action
    3. only the recipient has a claims record ->
       only claim IBC transfer action and transfer the claimable amount from the escrow account to the user balance
    4. neither the sender or recipient have a claims record ->
       perform a no-op by returning the original success acknowledgement


## Events

The `x/claims` module emits the following events:

### Claim

| Type    | Attribute Key | Attribute Value                                                         |
| ------- | ------------- | ----------------------------------------------------------------------- |
| `claim` | `"sender"`    | `{address}`                                                             |
| `claim` | `"amount"`    | `{amount}`                                                              |
| `claim` | `"action"`    | `{"ACTION_VOTE"/ "ACTION_DELEGATE"/"ACTION_EVM"/"ACTION_IBC_TRANSFER"}` |

### Merge Claims Records

| Type                   | Attribute Key                 | Attribute Value             |
| ---------------------- | ----------------------------- | --------------------------- |
| `merge_claims_records` | `"recipient"`                 | `{recipient.String()}`      |
| `merge_claims_records` | `"claimed_coins"`             | `{claimed_coins.String()}`  |
| `merge_claims_records` | `"fund_community_pool_coins"` | `{remainderCoins.String()}` |


## Parameters

The `x/claims` module contains the parameters described below. All parameters can be modified via governance.

:::danger
🚨 **IMPORTANT**: `time.Duration` store value is in nanoseconds but the JSON / `String` value is in seconds!
:::

| Key                  | Type            | Default Value                                               |
| -------------------- | --------------- | ----------------------------------------------------------- |
| `EnableClaim`        | `bool`          | `true`                                                      |
| `ClaimsDenom`        | `string`        | `"aevmos"`                                                  |
| `AirdropStartTime`   | `time.Time`     | `time.Time{}` // empty                                      |
| `DurationUntilDecay` | `time.Duration` | `2629800000000000` (nanoseconds) // 1 month                 |
| `DurationOfDecay`    | `time.Duration` | `5259600000000000` (nanoseconds) // 2 months                |
| `AuthorizedChannels` | `[]string`      | `[]string{"channel-0", "channel-3"}` // Osmosis, Cosmos Hub |
| `EVMChannels`        | `[]string`      | `[]string{"channel-2"}` // Injective                        |

### Enable claim

The `EnableClaim` parameter toggles all state transitions in the module.
When the parameter is disabled, it will disable all the allocation of airdropped tokens to users.

### Claims Denom

The `ClaimsDenom` parameter defines the coin denomination that users will receive as part of their airdrop allocation.

### Airdrop Start Time

The `AirdropStartTime` refers to the time when user can start to claim the airdrop tokens.

### Duration Until Decay

The `DurationUntilDecay` parameter defines the duration from airdrop start time to decay start time.

### Duration Of Decay

The `DurationOfDecay` parameter refers to the duration from decay start time to claim end time.
Users are not able to claim airdrop after this duration has ended.

### Authorized Channels

The `AuthorizedChannels` parameter describes the set of channels
that users can perform the ibc callback with to claim coins for the ibc action.

### EVM Channels

The `EVMChannels` parameter describes the list of Evmos channels
that connected to EVM compatible chains and can be used during the ibc callback action.


## Clients

A user can query the `x/claims` module using the CLI, gRPC or REST.

### CLI

Find below a list of `evmosd` commands added with the `x/claims` module.
You can obtain the full list by using the `evmosd -h` command.

#### Queries

The `query` commands allow users to query `claims` state.

**`total-unclaimed`**

Allows users to query total amount of unclaimed tokens from the airdrop.

```bash
evmosd query claims total-unclaimed [flags]
```

**`records`**

Allows users to query all the claims records available.

```bash
evmosd query claims records [flags]
```

**`record`**

Allows users to query a claims record for a given user.

```bash
evmosd query claims record ADDRESS [flags]
```

**`params`**

Allows users to query claims params.

```bash
evmosd query claims params [flags]
```

### gRPC

#### Queries

| Verb   | Method                                     | Description                                      |
|--------|--------------------------------------------|--------------------------------------------------|
| `gRPC` | `evmos.claims.v1.Query/TotalUnclaimed`     | Gets the total unclaimed tokens from the airdrop |
| `gRPC` | `evmos.claims.v1.Query/ClaimsRecords`      | Gets all registered claims records               |
| `gRPC` | `evmos.claims.v1.Query/ClaimsRecord`       | Get the claims record for a given user            |
| `gRPC` | `evmos.claims.v1.Query/Params`             | Gets claims params                               |
| `GET`  | `/evmos/claims/v1/total_unclaimed`         | Gets the total unclaimed tokens from the airdrop |
| `GET`  | `/evmos/claims/v1/claims_records`          | Gets all registered claims records               |
| `GET`  | `/evmos/claims/v1/claims_records/{address}` | Gets a claims record for a given user            |
| `GET`  | `/evmos/claims/v1/params`                  | Gets claims params                               |
