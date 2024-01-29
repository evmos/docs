# `inflation`

## Abstract

The `x/inflation` module mints new Evmos tokens and allocates them in daily
epochs according to the [Evmos Token
Model](https://evmos.blog/the-evmos-token-model-edc07014978b) distribution to

* Community Pool `50%`.
* Staking Rewards `50%`,
* Usage Incentives: `0%`,

It replaces the Cosmos SDK `x/mint` module, that other Cosmos chains are using.

The allocation of new coins incentivizes specific behaviour in the Evmos network.
Inflation allocates funds to 1) the community pool(managed by sdk `x/distr` module) to fund spending proposals,
and 2) the `Fee Collector account` (in the sdk `x/auth` module) to increase staking rewards.
The now deprecated `x/incentives` module (3) does not accrue any tokens anymore.

## Contents

1. **[Concepts](#concepts)**
2. **[State](#state)**
3. **[Hooks](#hooks)**
4. **[Events](#events)**
5. **[Parameters](#parameters)**
6. **[Clients](#clients)**

## Concepts

### Inflation

In a Proof of Stake (PoS) blockchain, inflation is used as a tool to incentivize
participation in the network. Inflation creates and distributes new tokens to
participants who can use their tokens to either interact with the protocol or
stake their assets to earn rewards and vote for governance proposals.

Especially in an early stage of a network, where staking rewards are high and
there are fewer possibilities to interact with the network, inflation can be
used as the major tool to incentivize staking and thereby securing the network.

With more stakers, the network becomes increasingly stable and decentralized. It
becomes *stable*, because assets are locked up instead of causing price changes
through trading. And it becomes *decentralized,* because the power to vote for
governance proposals is distributed amongst more people.

### Evmos Token Model

The Evmos Token Model outlines how the Evmos network is secured through a
balanced incentivized interest from users, developers and validators. In this
model, inflation plays a major role in sustaining this balance. With an initial
supply of 200 million and over 300 million tokens being issued through inflation
during the first year, the model suggests an exponential decline in inflation to
issue 1 billion Evmos tokens within the first 4 years.

We implement two different inflation mechanisms to support the token model:

1. linear inflation for team vesting and
2. exponential inflation for staking rewards and community pool.

#### Linear Inflation - Team Vesting

The Team Vesting distribution in the Token Model is implemented in a way that
minimized the amount of taxable events. An initial supply of 200M allocated to
`vesting accounts` at genesis. This amount is equal to the total inflation
allocated for team vesting after 4 years (`20% * 1B = 200M`). Over time,
`unvested` tokens on these accounts are converted into `vested` tokens at a
linear rate. Team members cannot delegate, transfer or execute Ethereum
transaction with `unvested` tokens until they are unlocked represented as
`vested` tokens.

#### Exponential Inflation - **The Half Life**

The inflation distribution for staking and community pool is
implemented through an exponential formula, a.k.a. the Half Life.

Inflation is minted in daily epochs. During a period of 365 epochs (one year),
a daily provision (`epochProvison`) of Evmos tokens is minted
and allocated to staking rewards and the community pool.
The epoch provision depends on module parameters and is recalculated at the end of every epoch.

The calculation of the epoch provision is done according to the following formula:

```latex
periodProvision = exponentialDecay       *  bondingIncentive
f(x)            = (a * (1 - r) ^ x + c)  *  (1 + maxVariance * (1 - bondedRatio / bondingTarget))


epochProvision = periodProvision / epochsPerPeriod

where (with default values):
x = variable    = year
a = 300,000,000 = initial value
r = 0.5         = decay factor
c = 9,375,000   = long term supply

bondedRatio   = variable  = fraction of the staking tokens which are currently bonded
maxVariance   = 0.0       = the max amount to increase inflation
bondingTarget = 0.66      = our optimal bonded ratio
```

```latex
Example with bondedRatio = bondingTarget:

period  periodProvision  cumulated      epochProvision
f(0)    309 375 000      309 375 000	 847 602
f(1)    159 375 000      468 750 000	 436 643
f(2)     84 375 000      553 125 000	 231 164
f(3)     46 875 000      600 000 000	 128 424
```

## State

### State Objects

The `x/inflation` module keeps the following objects in state:

| State Object    | Description                    | Key         | Value                     | Store |
| --------------- | ------------------------------ | ----------- | ------------------------- | ----- |
| Period          | Period Counter                 | `[]byte{1}` | `[]byte{period}`          | KV    |
| EpochIdentifier | Epoch identifier bytes         | `[]byte{3}` | `[]byte{epochIdentifier}` | KV    |
| EpochsPerPeriod | Epochs per period bytes        | `[]byte{4}` | `[]byte{epochsPerPeriod}` | KV    |
| SkippedEpochs   | Number of skipped epochs bytes | `[]byte{5}` | `[]byte{skippedEpochs}`   | KV    |

#### Period

Counter to keep track of amount of past periods, based on the epochs per period.

#### EpochIdentifier

Identifier to trigger epoch hooks.

#### EpochsPerPeriod

Amount of epochs in one period

### Genesis State

The `x/inflation` module's `GenesisState` defines the state necessary for
initializing the chain from a previously exported height. It contains the module
parameters, the current period, epoch identifier, epochs per period and
the number of skipped epochs.
:

```go
type GenesisState struct {
	// params defines all the parameters of the module.
	Params Params `protobuf:"bytes,1,opt,name=params,proto3" json:"params"`
	// amount of past periods, based on the epochs per period param
	Period uint64 `protobuf:"varint,2,opt,name=period,proto3" json:"period,omitempty"`
	// inflation epoch identifier
	EpochIdentifier string `protobuf:"bytes,3,opt,name=epoch_identifier,json=epochIdentifier,proto3" json:"epoch_identifier,omitempty"`
	// number of epochs after which inflation is recalculated
	EpochsPerPeriod int64 `protobuf:"varint,4,opt,name=epochs_per_period,json=epochsPerPeriod,proto3" json:"epochs_per_period,omitempty"`
	// number of epochs that have passed while inflation is disabled
	SkippedEpochs uint64 `protobuf:"varint,5,opt,name=skipped_epochs,json=skippedEpochs,proto3" json:"skipped_epochs,omitempty"`
}
```

## Hooks

The `x/inflation` module implements the `AfterEpochEnd`  hook from the
`x/epoch` module in order to allocate inflation.

### Epoch Hook: Inflation

The epoch hook handles the inflation logic which is run at the end of each
epoch. It is responsible for minting and allocating the epoch mint provision as
well as updating it:

1. Check if inflation is disabled. If it is, skip inflation, increment number
   of skipped epochs and return without proceeding to the next steps.
2. A block is committed, that signalizes that an `epoch` has ended (block
   `header.Time` has surpassed `epoch_start` + `epochIdentifier`).
3. Mint coin in amount of calculated `epochMintProvision` and allocate according to
   inflation distribution to staking rewards and community pool.
4. If a period ends with the current epoch, increment the period by `1` and set new value to the store.

## Events

The `x/inflation` module emits the following events:

### Inflation

| Type        | Attribute Key        | Attribute Value                               |
| ----------- | -------------------- | --------------------------------------------- |
| `inflation` | `"epoch_provisions"` | `{fmt.Sprintf("%d", epochNumber)}`            |
| `inflation` | `"epoch_number"`     | `{strconv.FormatUint(uint64(in.Epochs), 10)}` |
| `inflation` | `"amount"`           | `{mintedCoin.Amount.String()}`                |

## Parameters

The `x/inflation` module contains the parameters described below. All parameters
can be modified via governance.

| Key                                   | Type                   | Default Value                                        |
| ------------------------------------- | ---------------------- |------------------------------------------------------|
| `ParamStoreKeyMintDenom`              | string                 | `evm.DefaultEVMDenom` // “aevmos”                    |
| `ParamStoreKeyExponentialCalculation` | ExponentialCalculation | `A: sdk.NewDec(int64(300_000_000))`                  |
|                                       |                        | `R: sdk.NewDecWithPrec(50, 2)`                       |
|                                       |                        | `C: sdk.NewDec(int64(9_375_000))`                    |
|                                       |                        | `BondingTarget: sdk.NewDecWithPrec(66, 2)`           |
|                                       |                        | `MaxVariance: sdk.ZeroDec()`                         |
| `ParamStoreKeyInflationDistribution`  | InflationDistribution  | `StakingRewards: sdk.NewDecWithPrec(500000000, 9)`   |
|                                       |                        | `UsageIncentives: sdk.NewDecWithPrec(000000000, 9)`  |
|                                       |                        | `CommunityPool: sdk.NewDecWithPrec(500000000, 9)`    |
| `ParamStoreKeyEnableInflation`        | bool                   | `true`                                               |

### Mint Denom

The `ParamStoreKeyMintDenom` parameter sets the denomination in which new coins are minted.

### Exponential Calculation

The `ParamStoreKeyExponentialCalculation` parameter holds all values required for the
calculation of the `epochMintProvision`. The values `A`, `R` and `C` describe
the decrease of inflation over time. The `BondingTarget` and `MaxVariance`
allow for an increase in inflation, which is automatically regulated by the
`bonded ratio`, the portion of staked tokens in the network. The exact formula
can be found under
[Concepts](#concepts).

### Inflation Distribution

The `ParamStoreKeyInflationDistribution` parameter defines the distribution in which
inflation is allocated through minting on each epoch (`stakingRewards`,
`usageIncentives`,  `CommunityPool`).
The `x/inflation` excludes the team vesting distribution,
as team vesting is minted once at genesis.
<!-- This does not really apply anymore -->
To reflect this the distribution from the Evmos Token Model is recalculated into a distribution
that excludes team vesting. Note, that this does not change the inflation
proposed in the Evmos Token Model. Each `InflationDistribution` can be
calculated like this:

```markdown
stakingRewards = evmosTokenModelDistribution / (1 - teamVestingDistribution)
0.5333333      = 40%                         / (1 - 25%)
```

### Enable Inflation

The `ParamStoreKeyEnableInflation` parameter enables the daily inflation. If it is disabled,
no tokens are minted and the number of skipped epochs increases for each passed
epoch.

## Clients

A user can query the `x/inflation` module using the CLI, JSON-RPC, gRPC or
REST.

### CLI

Find below a list of `evmosd` commands added with the `x/inflation` module. You
can obtain the full list by using the `evmosd -h` command.

#### Queries

The `query` commands allow users to query `inflation` state.

**`period`**

Allows users to query the current inflation period.

```bash
evmosd query inflation period [flags]
```

**`epoch-mint-provision`**

Allows users to query the current inflation epoch provisions value.

```bash
evmosd query inflation epoch-mint-provision [flags]
```

**`skipped-epochs`**

Allows users to query the current number of skipped epochs.

```bash
evmosd query inflation skipped-epochs [flags]
```

**`total-supply`**

Allows users to query the total supply of tokens in circulation.

```bash
evmosd query inflation total-supply [flags]
```

**`inflation-rate`**

Allows users to query the inflation rate of the current period.

```bash
evmosd query inflation inflation-rate [flags]
```

**`params`**

Allows users to query the current inflation parameters.

```bash
evmosd query inflation params [flags]
```

#### Proposals

**Update Params**

Allows users to submit a `MsgUpdateParams` with the desired changes on the `x/inflation` module parameters.
To do this, you will have to provide a JSON file with the correspondiong message in the `submit-proposal` command.

For more information on how to draft a proposal, refer to the [Drafting a proposal section](../evmos-cli/proposal-draft.md).

```bash
evmosd tx gov submit-proposal proposal.json [flags]
```

### gRPC

#### Queries

| Verb   | Method                                        | Description                                   |
| ------ | --------------------------------------------- | --------------------------------------------- |
| `gRPC` | `evmos.inflation.v1.Query/Period`             | Gets current inflation period                 |
| `gRPC` | `evmos.inflation.v1.Query/EpochMintProvision` | Gets current inflation epoch provisions value |
| `gRPC` | `evmos.inflation.v1.Query/Params`             | Gets current inflation parameters             |
| `gRPC` | `evmos.inflation.v1.Query/SkippedEpochs`      | Gets current number of skipped epochs         |
| `gRPC` | `evmos.inflation.v1.Query/TotalSupply`        | Gets current total supply                     |
| `gRPC` | `evmos.inflation.v1.Query/InflationRate`      | Gets current inflation rate                   |
| `GET`  | `/evmos/inflation/v1/period`                  | Gets current inflation period                 |
| `GET`  | `/evmos/inflation/v1/epoch_mint_provision`    | Gets current inflation epoch provisions value |
| `GET`  | `/evmos/inflation/v1/skipped_epochs`          | Gets current number of skipped epochs         |
| `GET`  | `/evmos/inflation/v1/total_supply`            | Gets current total supply                     |
| `GET`  | `/evmos/inflation/v1/inflation_rate`          | Gets current inflation rate                   |
| `GET`  | `/evmos/inflation/v1/params`                  | Gets current inflation parameters             |
