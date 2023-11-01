# `incentives`

## Abstract

This document specifies the internal `x/incentives` module of the Evmos Hub.

The `x/incentives` module is part of the Evmos tokenomics and aims
to increase the growth of the network by distributing rewards
to users who interact with incentivized smart contracts.
The rewards drive users to interact with applications on Evmos and reinvest their rewards in more services in the network.

The usage incentives are taken from block reward emission (inflation)
and are pooled up in the Incentives module account (escrow address).
The incentives functionality is fully governed by native EVMOS token holders
who manage the registration of `Incentives`,
so that native EVMOS token holders decide which application should be part of the usage incentives.
This governance functionality is implemented using the Cosmos-SDK `gov` module
with custom proposal types for registering the incentives.

Users participate in incentives by submitting transactions to an incentivized contract.
The module keeps a record of how much gas the participants spent on their transactions and stores these in gas meters.
Based on their gas meters, participants in the incentive are rewarded in regular intervals (epochs).

## Contents

1. **[Concepts](#concepts)**
2. **[State](#state)**
3. **[State Transitions](#state-transitions)**
4. **[Transactions](#transactions)**
5. **[Hooks](#hooks)**
6. **[Events](#events)**
7. **[Parameters](#parameters)**
8. **[Clients](#clients)**

## Concepts

### Incentive

The purpose of the `x/incentives` module is to provide incentives to users who interact with smart contracts.
An incentive allows users to earn rewards up to `rewards = k * sum(tx fees)`,
where `k` defines a reward scaler parameter that caps the incentives allocated to a single user
by multiplying it with the sum of transaction fees
that they’ve spent in the current epoch.

An `incentive` describes the conditions under which rewards are allocated and distributed for a given smart contract.
At the end of every epoch, rewards are allocated from an Inflation pool
and distributed to participants of the incentive, depending on how much gas every participant spent and the scaling parameter.

The incentive for a given smart contract can be enabled or disabled via governance.

### Inflation Pool

The inflation pool holds `rewards` that can be allocated to incentives.
On every block, inflation rewards are minted and added to the inflation pool.
Additionally, rewards may also be transferred to the inflation pool on top of inflation.
The details of how rewards are added to the inflation pool are described in the `x/inflation` module.

### Epoch

Rewarding users for smart contract interaction is organized in epochs.
An `epoch` is a fixed duration in which rewards are added to the inflation pool and smart contract interaction is logged.
At the end of an epoch, rewards are allocated and distributed to all participants.
This creates a user experience, where users check their balance for new rewards regularly (e.g.
every day at the same time).

### Allocation

Before rewards are distributed to users, each incentive allocates rewards from the inflation pool.
The `allocation` describes the portion of rewards in the inflation pool,
that is allocated to an incentive for a specified coin.

Users can be rewarded in several coin denominations.
These are organized in `allocations`.
An allocation includes the coin denomination and the percentage of rewards that are allocated from the inflation pool.

- There is a cap on how high the reward percentage can be per allocation.
  It is defined via the chain parameters and can be modified via governance
- The amount of incentives is limited by the sum of all active incentivized contracts' allocations.
  If the sum is > 100%, no further incentive can be proposed until another allocation becomes inactive.

### Distribution

The allocated rewards for an incentive are distributed
according to how much gas participants spend on interaction with the contract during an epoch.
The gas used per address is recorded using transaction hooks and stored on the KV store.
At the end of an epoch, the allocated rewards in the incentive are distributed
by transferring them to the participants accounts.

:::tip
💡 We use hooks instead of the transaction hash to measure the gas spent
because the hook has access to the actual gas spent and the hash only includes the gas limit.
:::


## State

### State Objects

The `x/incentives` module keeps the following objects in state:

| State Object    | Description                                   | Key                                                    | Value               | Store |
| --------------- | --------------------------------------------- | ------------------------------------------------------ | ------------------- | ----- |
| Incentive       | Incentive bytecode                            | `[]byte{1} + []byte(contract)`                         | `[]byte{incentive}` | KV    |
| GasMeter        | Incentive id bytecode by erc20 contract bytes | `[]byte{2} + []byte(contract) + []byte(participant)` | `[]byte{gasMeter}`  | KV    |
| AllocationMeter | Total allocation bytes by denom bytes         | `[]byte{3} + []byte(denom)`                            | `[]byte{sdk.Dec}`   | KV    |

#### Incentive

An instance that organizes distribution conditions for a given smart contract.

```go
type Incentive struct {
	// contract address
	Contract string `protobuf:"bytes,1,opt,name=contract,proto3" json:"contract,omitempty"`
	// denoms and percentage of rewards to be allocated
	Allocations github_com_cosmos_cosmos_sdk_types.DecCoins `protobuf:"bytes,2,rep,name=allocations,proto3,castrepeated=github.com/cosmos/cosmos-sdk/types.DecCoins" json:"allocations"`
	// number of remaining epochs
	Epochs uint32 `protobuf:"varint,3,opt,name=epochs,proto3" json:"epochs,omitempty"`
	// distribution start time
	StartTime time.Time `protobuf:"bytes,4,opt,name=start_time,json=startTime,proto3,stdtime" json:"start_time"`
	// cumulative gas spent by all gasmeters of the incentive during the epoch
	TotalGas uint64 `protobuf:"varint,5,opt,name=total_gas,json=totalGas,proto3" json:"total_gas,omitempty"`
}
```

As long as an incentive has remaining epochs, it distributes rewards according to its allocations.
The allocations are stored as `sdk.DecCoins` where each containing
[`sdk.DecCoin`](https://github.com/cosmos/cosmos-sdk/blob/master/types/dec_coin.go) describes the percentage of rewards
(`Amount`) that are allocated to the contract for a given coin denomination (`Denom`).
An incentive can contain several allocations, resulting in users to receive rewards in form of several different denominations.

#### GasMeter

Tracks the cumulative gas spent in a contract per participant during one epoch.

```go
type GasMeter struct {
	// hex address of the incentivized contract
	Contract string `protobuf:"bytes,1,opt,name=contract,proto3" json:"contract,omitempty"`
	// participant address that interacts with the incentive
	Participant string `protobuf:"bytes,2,opt,name=participant,proto3" json:"participant,omitempty"`
	// cumulative gas spent during the epoch
	CumulativeGas uint64 `protobuf:"varint,3,opt,name=cumulative_gas,json=cumulativeGas,proto3" json:"cumulative_gas,omitempty"`
}
```

#### AllocationMeter

An allocation meter stores the sum of all registered incentives’ allocations for a given denomination
and is used to limit the amount of registered incentives.

Say, there are several incentives that have registered an allocation for the EVMOS coin
and the allocation meter for EVMOS is at 97%.
Then a new incentve proposal can only include an EVMOS allocation at up to 3%,
claiming the last remaining allocation capacity from the EVMOS rewards in the inflation pool.

### Genesis State

The `x/incentives` module's `GenesisState` defines the state
necessary for initializing the chain from a previously exported height.
It contains the module parameters and the list of active incentives and their corresponding gas meters:

```go
// GenesisState defines the module's genesis state.
type GenesisState struct {
	// module parameters
	Params Params `protobuf:"bytes,1,opt,name=params,proto3" json:"params"`
	// active incentives
	Incentives []Incentive `protobuf:"bytes,2,rep,name=incentives,proto3" json:"incentives"`
	// active Gasmeters
	GasMeters []GasMeter `protobuf:"bytes,3,rep,name=gas_meters,json=gasMeters,proto3" json:"gas_meters"`
}
```


## State Transitions

The `x/incentive` module allows for two types of registration state transitions:
`RegisterIncentiveProposal` and `CancelIncentiveProposal`.
The logic for *gas metering* and *distributing rewards* is handled through [Hooks](#hooks).

### Incentive Registration

A user registers an incentive defining the contract, allocations, and number of epochs.
Once the proposal passes (i.e is approved by governance),
the incentive module creates the incentive and distributes rewards.

1. User submits a `RegisterIncentiveProposal`.
2. Validators of the Evmos Hub vote on the proposal using `MsgVote` and proposal passes.
3. Create incentive for the contract with a `TotalGas = 0` and set its `startTime` to `ctx.Blocktime`
   if the following conditions are met:
    1. Incentives param is globally enabled
    2. Incentive is not yet registered
    3. Balance in the inflation pool is > 0 for each allocation denom except for the mint denomination.
       We know that the amount of the minting denom (e.g. EVMOS) will be added to every block
       but for other denominations (IBC vouchers, ERC20 tokens using the `x/erc20` module)
       the module account needs to have a positive amount to distribute the incentives
    4. The sum of all registered allocations for each denom (current + proposed) is < 100%


## Transactions

This section defines the `sdk.Msg` concrete types that result in the state transitions defined on the previous section.

## `RegisterIncentiveProposal`

A gov `Content` type to register an Incentive for a given contract for the duration of a certain number of epochs.
Governance users vote on this proposal
and it automatically executes the custom handler for `RegisterIncentiveProposal` when the vote passes.

```go
type RegisterIncentiveProposal struct {
	// title of the proposal
	Title string `protobuf:"bytes,1,opt,name=title,proto3" json:"title,omitempty"`
	// proposal description
	Description string `protobuf:"bytes,2,opt,name=description,proto3" json:"description,omitempty"`
	// contract address
	Contract string `protobuf:"bytes,3,opt,name=contract,proto3" json:"contract,omitempty"`
	// denoms and percentage of rewards to be allocated
	Allocations github_com_cosmos_cosmos_sdk_types.DecCoins `protobuf:"bytes,4,rep,name=allocations,proto3,castrepeated=github.com/cosmos/cosmos-sdk/types.DecCoins" json:"allocations"`
	// number of remaining epochs
	Epochs uint32 `protobuf:"varint,5,opt,name=epochs,proto3" json:"epochs,omitempty"`
}
```

The proposal content stateless validation fails if:

- Title is invalid (length or char)
- Description is invalid (length or char)
- Contract address is invalid
- Allocations are invalid
    - no allocation included in Allocations
    - invalid amount of at least one allocation (below 0 or above 1)
- Epochs are invalid (zero)

## `CancelIncentiveProposal`

A gov `Content` type to remove an Incentive.
Governance users vote on this proposal
and it automatically executes the custom handler for `CancelIncentiveProposal` when the vote passes.

```go
type CancelIncentiveProposal struct {
	// title of the proposal
	Title string `protobuf:"bytes,1,opt,name=title,proto3" json:"title,omitempty"`
	// proposal description
	Description string `protobuf:"bytes,2,opt,name=description,proto3" json:"description,omitempty"`
	// contract address
	Contract string `protobuf:"bytes,3,opt,name=contract,proto3" json:"contract,omitempty"`
}
```

The proposal content stateless validation fails if:

- Title is invalid (length or char)
- Description is invalid (length or char)
- Contract address is invalid


## Hooks

The `x/incentives` module implements two transaction hooks from the `x/evm` and `x/epoch` modules.

### EVM Hook - Gas Metering

The EVM hook updates the logs that keep track of much gas was used
for interacting with an incentivized contract during one epoch.
An [EVM hook](evm.md#hooks) executes custom logic
after each successful evm transaction.
In this case it updates the incentive’s total gas count and the participant's own gas count.

1. User submits an EVM transaction to an incentivized smart contract and the transaction is finished successfully.
2. The EVM hook’s `PostTxProcessing` method is called on the incentives module.
   It is passed a transaction receipt
   that includes the cumulative gas used by the transaction sender to pay for the gas fees.
   The hook
    1. adds `gasUsed` to an incentive's cumulated `totalGas` and
    2. adds `gasUsed` to a participant's gas meter's cumulative gas used.

### Epoch Hook - Distribution of Rewards

The Epoch hook triggers the distribution of usage rewards for all registered incentives at the end of each epoch
(one day or one week).
This distribution process first 1) allocates the rewards for each incentive from the allocation pool
and then 2) distributes these rewards to all participants of each incentive.

1. A `RegisterIncentiveProposal` passes and an `incentive` for the proposed contract is created.
2. An `epoch` begins and `rewards` (EVMOS and other denoms) that are minted on every block for inflation
   are added to the inflation pool every block.
3. Users submit transactions and call functions on the incentivized smart contracts to interact
   and gas gets logged through the EVM Hook.
4. A block, which signalizes the end of an `epoch`, is proposed
   and the `DistributeIncentives` method is called through `AfterEpochEnd` hook.
   This method:
    1. Allocates the amount to be distributed from the inflation pool
    2. Distributes the rewards to all participants.
       The rewards of each participant are limited by the amount of gas they spent on transaction fees
       during the current epoch and the reward scaler parameter.
    3. Deletes all gas meters for the contract
    4. Updates the remaining epochs of each incentive.
       If an incentive’s remaining epochs equals to zero,
       the incentive is removed and the allocation meters are updated.
    5. Sets the cumulative totalGas to zero for the next epoch
5. Rewards for a given denomination accumulate in the inflation pool
   if the denomination’s allocation capacity is not fully exhausted
   and the sum of all active incentivized contracts' allocation is < 100%.
   The accumulated rewards are added to the allocation in the following epoch.


## Events

The `x/incentives` module emits the following events:

### Register Incentive Proposal

| Type                 | Attribute Key | Attribute Value                                |
| -------------------- | ------------ | --------------------------------------------- |
| `register_incentive` | `"contract"` | `{erc20_address}`                             |
| `register_incentive` | `"epochs"`   | `{strconv.FormatUint(uint64(in.Epochs), 10)}` |

### Cancel Incentive Proposal

| Type               | Attribute Key | Attribute Value    |
| ------------------ | ------------ | ----------------- |
| `cancel_incentive` | `"contract"` | `{erc20_address}` |

### Incentive Distribution

| Type                    | Attribute Key | Attribute Value                                |
| ----------------------- | ------------ | --------------------------------------------- |
| `distribute_incentives` | `"contract"` | `{erc20_address}`                             |
| `distribute_incentives` | `"epochs"`   | `{strconv.FormatUint(uint64(in.Epochs), 10)}` |


## Parameters

The `x/incentives` module contains the parameters described below. All parameters can be modified via governance.

| Key                         | Type    | Default Value                      |
| --------------------------- | ------- | ---------------------------------- |
| `EnableIncentives`          | bool    | `true`                             |
| `AllocationLimit`           | sdk.Dec | `sdk.NewDecWithPrec(5,2)` // 5%    |
| `IncentivesEpochIdentifier` | string  | `week`                             |
| `rewardScaler`              | sdk.Dec | `sdk.NewDecWithPrec(12,1)` // 120% |

### Enable Incentives

The `EnableIncentives` parameter toggles all state transitions in the module.
When the parameter is disabled, it will prevent all Incentive registration and cancellation and distribution functionality.

### Allocation Limit

The `AllocationLimit` parameter defines the maximum allocation that each incentive can define per denomination.
For example, with an `AllocationLimit` of 5%,
there can be at most 20 active incentives per denom if they all max out the limit.

There is a cap on how high the reward percentage can be per allocation.

### Incentives Epoch Identifier

The `IncentivesEpochIdentifier` parameter specifies the length of an epoch.
It is the interval at which incentive rewards are regularly distributed.

### Reward Scaler

The `rewardScaler` parameter defines  each participant’s reward limit, relative to their gas used.
An incentive allows users to earn rewards up to `rewards = k * sum(txFees)`,
where `k` defines the reward scaler parameter that caps the incentives allocated to a single user
by multiplying it to the sum of transaction fees that they’ve spent in the current epoch.


## Clients

A user can query the `x/incentives` module using the CLI, JSON-RPC, gRPC or REST.

### CLI

Find below a list of `evmosd` commands added with the `x/incentives` module.
You can obtain the full list by using the `evmosd -h` command.

#### Queries

The `query` commands allow users to query `incentives` state.

**`incentives`**

Allows users to query all registered incentives.

```go
evmosd query incentives incentives [flags]
```

**`incentive`**

Allows users to query an incentive for a given contract.

```go
evmosd query incentives incentive CONTRACT_ADDRESS [flags]
```

**`gas-meters`**

Allows users to query all gas meters for a given incentive.

```bash
evmosd query incentives gas-meters CONTRACT_ADDRESS [flags]
```

**`gas-meter`**

Allows users to query a gas meter for a given incentive and user.

```go
evmosd query incentives gas-meter CONTRACT_ADDRESS PARTICIPANT_ADDRESS [flags]
```

**`params`**

Allows users to query incentives params.

```bash
evmosd query incentives params [flags]
```

#### Proposals

The `tx gov submit-legacy-proposal` commands allow users to query create a proposal using the governance module CLI:

**`register-incentive`**

Allows users to submit a `RegisterIncentiveProposal`.

```bash
evmosd tx gov submit-legacy-proposal register-incentive CONTRACT_ADDRESS ALLOCATION EPOCHS [flags]
```

**`cancel-incentive`**

Allows users to submit a `CanelIncentiveProposal`.

```bash
evmosd tx gov submit-legacy-proposal cancel-incentive CONTRACT_ADDRESS [flags]
```

**Update Params**

Allows users to submit a `MsgUpdateParams` with the desired changes on the `x/incentives` module parameters.
To do this, you will have to provide a JSON file with the proposal.

```bash
evmosd tx gov submit-proposal proposal.json [flags]
```

:::tip
To generate the required JSON file, you can use the following command:

```bash
evmosd tx gov draft-proposal 
Use the arrow keys to navigate: ↓ ↑ → ← 
? Select proposal type: 
    text
    community-pool-spend
    software-upgrade
    cancel-software-upgrade
  ▸ other
```

Select `other` option and look for the `/evmos.incentives.v1.MsgUpdateParams` message

```bash
✔ other
Use the arrow keys to navigate: ↓ ↑ → ← 
? Select proposal message type:: 
↑   /evmos.erc20.v1.MsgUpdateParams
  ▸ /evmos.incentives.v1.MsgUpdateParams
    /evmos.inflation.v1.MsgUpdateParams
    /evmos.recovery.v1.MsgUpdateParams
↓   /evmos.revenue.v1.MsgCancelRevenue
```

Follow the instructions. Once you're done with it, it will generate a JSON file.
Make any changes if necessary and use that file in the `submit-proposal` transaction
:::

### gRPC

#### Queries

| Verb   | Method                                                     | Description                                   |
| ------ | ---------------------------------------------------------- | --------------------------------------------- |
| `gRPC` | `evmos.incentives.v1.Query/Incentives`                     | Gets all registered incentives                |
| `gRPC` | `evmos.incentives.v1.Query/Incentive`                      | Gets incentive for a given contract           |
| `gRPC` | `evmos.incentives.v1.Query/GasMeters`                      | Gets gas meters for a given incentive         |
| `gRPC` | `evmos.incentives.v1.Query/GasMeter`                       | Gets gas meter for a given incentive and user |
| `gRPC` | `evmos.incentives.v1.Query/AllocationMeters`               | Gets all allocation meters                    |
| `gRPC` | `evmos.incentives.v1.Query/AllocationMeter`                | Gets allocation meter for a denom             |
| `gRPC` | `evmos.incentives.v1.Query/Params`                         | Gets incentives params                        |
| `GET`  | `/evmos/incentives/v1/incentives`                          | Gets all registered incentives                |
| `GET`  | `/evmos/incentives/v1/incentives/{contract}`               | Gets incentive for a given contract           |
| `GET`  | `/evmos/incentives/v1/gas_meters`                          | Gets gas meters for a given incentive         |
| `GET`  | `/evmos/incentives/v1/gas_meters/{contract}/{participant}` | Gets gas meter for a given incentive and user |
| `GET`  | `/evmos/incentives/v1/allocation_meters`                   | Gets all allocation meters                    |
| `GET`  | `/evmos/incentives/v1/allocation_meters/{denom}`           | Gets allocation meter for a denom             |
| `GET`  | `/evmos/incentives/v1/params`                              | Gets incentives params                        |
