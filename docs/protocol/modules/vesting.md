# `vesting`

## Abstract

This document specifies the internal `x/vesting` module of the Evmos Hub.

The `x/vesting` module introduces the `ClawbackVestingAccount`,  a new vesting account type
that implements the Cosmos SDK [`VestingAccount`](https://docs.cosmos.network/main/modules/auth/vesting#vesting-account-types)
interface.
This account is used to allocate tokens that are subject to vesting, lockup, and clawback.

The `ClawbackVestingAccount` allows any two parties to agree on a future rewarding schedule,
where tokens are granted permissions over time.
The parties can use this account to enforce legal contracts or commit to mutual long-term interests.

In this commitment, vesting is the mechanism for gradually earning permission to transfer and delegate allocated tokens.
Additionally, the lockup provides a mechanism to prevent the right to transfer allocated tokens
and perform Ethereum transactions from the account.
Both vesting and lockup are defined in schedules at account creation.
At any time, the funder of a `ClawbackVestingAccount` can perform a clawback to retrieve unvested tokens.
The circumstances under which a clawback should be performed can be agreed upon in a contract
(e.g. smart contract).

For Evmos, the `ClawbackVestingAccount` is used to allocate tokens to core team members and advisors
to incentivize long-term participation in the project.

## Contents

1. **[Concepts](#concepts)**
2. **[State](#state-transitions)**
3. **[State Transitions](#state-transitions)**
4. **[Transactions](#transactions)**
5. **[AnteHandlers](#antehandlers)**
6. **[Events](#events)**
7. **[Clients](#clients)**

## References

- SDK vesting specification: [https://docs.cosmos.network/main/modules/auth/vesting](https://docs.cosmos.network/main/modules/auth/vesting)
- SDK vesting implementation: [https://github.com/cosmos/cosmos-sdk/tree/master/x/auth/vesting](https://github.com/cosmos/cosmos-sdk/tree/master/x/auth/vesting)
- Agoric’s Vesting Clawback Account: [https://github.com/Agoric/agoric-sdk/issues/4085](https://github.com/Agoric/agoric-sdk/issues/4085)
- Agoric’s `vestcalc` tool: [https://github.com/agoric-labs/cosmos-sdk/tree/Agoric/x/auth/vesting/cmd/vestcalc](https://github.com/agoric-labs/cosmos-sdk/tree/Agoric/x/auth/vesting/cmd/vestcalc)

## Concepts

### Vesting

Vesting describes the process of converting `unvested` into `vested` tokens
without transferring the ownership of those tokens.
In an unvested state, tokens cannot be transferred to other accounts, delegated to validators, or used for governance.
A vesting schedule describes the amount and time at which tokens are vested.
The duration until which the first tokens are vested is called the `cliff`.

### Lockup

The lockup describes the schedule by which tokens are converted from a `locked` to an `unlocked` state.
As long as all tokens are locked, the account cannot perform any transaction
that spend EVMOS. However, the account can perform transactions that don't spend EVMOS tokens.
Additionally, locked tokens cannot be transferred to other accounts.
In the case in which tokens are both locked and vested at the same time,
it is possible to delegate them to validators, but not transfer them to other accounts.

The following table summarizes the actions that are allowed for tokens
that are subject to the combination of vesting and lockup:

| Token Status            | Transfer | Delegate | Vote | Eth Txs that spend EVMOS\*\* | Eth Txs that don't spend EVMOS (amount = 0)\*\* |
| ----------------------- | :------: | :------: | :--: | :--------------------------: | :---------------------------------------------: |
| `locked` & `unvested`   |    ❌    |    ❌    |  ❌  |              ❌              |                       ✅                        |
| `locked` & `vested`     |    ❌    |    ✅    |  ✅  |              ❌              |                       ✅                        |
| `unlocked` & `unvested` |    ❌    |    ❌    |  ❌  |              ❌              |                       ✅                        |
| `unlocked` & `vested`\* |    ✅    |    ✅    |  ✅  |              ✅              |                       ✅                        |

\*Staking rewards are unlocked and vested

\*\*EVM transactions only fail if they involve sending locked or unvested EVMOS tokens,
e.g. send EVMOS to EOA or Smart Contract (fails if amount > 0 ).

### Schedules

Vesting and lockup schedules specify the amount and time at which tokens are vested or unlocked.
They are defined as [`periods`](https://docs.cosmos.network/main/modules/auth/vesting#period)
where each period has its own length and amount.
A typical vesting schedule for instance would be defined starting with a one-year period to represent the vesting cliff,
followed by several monthly vesting periods until the total allocated vesting amount is vested.

Vesting or lockup schedules can be easily created
with Agoric’s [`vestcalc`](https://github.com/agoric-labs/cosmos-sdk/tree/Agoric/x/auth/vesting/cmd/vestcalc) tool.
E.g.
to calculate a four-year vesting schedule with a one year cliff, starting in January 2022, you can run vestcalc with:

```bash
vestcalc --write --start=2022-01-01 --coins=200000000000000000000000aevmos --months=48 --cliffs=2023-01-01
```

### Clawback

In case a `ClawbackVestingAccount`'s underlying commitment or contract is breached,
the clawback provides a mechanism to return unvested funds. The account authorized to perform the clawback is
defined during `ClawbackVestingAccount` account creation. It can be:

- The governance module if allowed
- The address specified as the `FunderAddress`

It should be noted that the information if an account has governance clawback enabled or not is not stored with
the account itself but it is stored directly in the vesting module.

When a clawback is initiated, or by the funder or the governance, unvested tokens are send to the destination
address specified in the clawback message. If no destination address is specified, the default is to return
tokens to the funder.

## State

### State Objects

The `x/vesting` module does not keep objects in its own store.
Instead, it uses the SDK `auth` module to store account objects in state
using the [Account Interface](https://docs.cosmos.network/main/modules/auth#account-interface).
Accounts are exposed externally as an interface and stored internally as a clawback vesting account.

### ClawbackVestingAccount

An instance that implements
the [Vesting Account](https://docs.cosmos.network/main/modules/auth/vesting#vesting-account-types) interface.
It provides an account that can hold contributions subject to lockup,
or vesting which is subject to clawback of unvested tokens,
or a combination (tokens vest, but are still locked).

```go
type ClawbackVestingAccount struct {
	// base_vesting_account implements the VestingAccount interface. It contains
	// all the necessary fields needed for any vesting account implementation
	*types.BaseVestingAccount `protobuf:"bytes,1,opt,name=base_vesting_account,json=baseVestingAccount,proto3,embedded=base_vesting_account" json:"base_vesting_account,omitempty"`
	// funder_address specifies the account which can perform clawback
	FunderAddress string `protobuf:"bytes,2,opt,name=funder_address,json=funderAddress,proto3" json:"funder_address,omitempty"`
	// start_time defines the time at which the vesting period begins
	StartTime time.Time `protobuf:"bytes,3,opt,name=start_time,json=startTime,proto3,stdtime" json:"start_time"`
	// lockup_periods defines the unlocking schedule relative to the start_time
	LockupPeriods []types.Period `protobuf:"bytes,4,rep,name=lockup_periods,json=lockupPeriods,proto3" json:"lockup_periods"`
	// vesting_periods defines the vesting schedule relative to the start_time
	VestingPeriods []types.Period `protobuf:"bytes,5,rep,name=vesting_periods,json=vestingPeriods,proto3" json:"vesting_periods"`
}
```

#### BaseVestingAccount

Implements the `VestingAccount` interface.
It contains all the necessary fields needed for any vesting account implementation.

#### FunderAddress

Specifies the account which provides the original tokens and can perform clawback.

#### StartTime

Defines the time at which the vesting and lockup schedules begin.

#### LockupPeriods

Defines the unlocking schedule relative to the start time.

#### VestingPeriods

Defines the vesting schedule relative to the start time.

### Genesis State

The `x/vesting` module allows the definition of `ClawbackVestingAccounts` at genesis.
In this case, the account balance must be logged in the SDK `bank` module balances
or automatically adjusted through the `add-genesis-account` CLI command.

## State Transitions

The `x/vesting` module allows for state transitions that create
and update a clawback vesting account with `CreateClawbackVestingAccount`
or perform a clawback of unvested funds with `Clawback`.

### Create Clawback Vesting Account

An externally owned account can be converted to a clawback vesting account by the owner.
Upon creation, the owner assigns a funder, who is able to fund the account with vesting and/or lockup schedules.
The account has also the possibility to specify if the vested tokens can be calwbacked from the governance.

1. Owner submits a `MsgCreateClawbackVestingAccount` through one of the clients.
2. Check if
    1. the vesting account address is not blocked.
    2. the account at the vesting account address is not already a vesting account.
3. Create a clawback vesting account at the target address with empty vesting and lockup schedules.

### Fund Clawback Vesting Account

 The funder of a clawback vesting account can fund it with vesting and/or lockup schedules.
 If a vesting account already has funds, the schedules are merged together.

 1. Funder submits a `MsgFundVestingAccount` through one of the clients.
 2. Check if
	1. the vesting address is not a blocked address.
	2. the vesting address is a clawback vesting account.
	3. there is at least one vesting or lockup schedule provided.
	If one of them is absent, default to instant vesting or unlock schedule.
 4. lockup and vesting total amounts are equal.
 3. Update the clawback vesting account and send coins from the funder to the vesting account,
    merging any existing schedules with the new funding.

### Clawback

The funding address is the only address that can perform the clawback.

1. Funder submits a `MsgClawback` through one of the clients.
2. Check if
    1. a destination address is given and default to funder address if not
    2. the destination address is not blocked
    3. the account exists and is a clawback vesting account
    4. account funder is same as in msg
3. Transfer unvested tokens from the clawback vesting account to the destination address,
   update the lockup schedule and remove future vesting events.

### Update Clawback Vesting Account Funder

The funding address of an existing clawback vesting account can be updated only by the current funder.

1. Funder submits a `MsgUpdateVestingFunder` through one of the clients.
2. Check if
    1. the new funder address is not blocked
    2. the vesting account exists and is a clawback vesting account
    3. account funder is same as in msg
3. Update the vesting account funder with the new funder address.

### Convert Vesting Account

Once all tokens are vested, the vesting account can be converted back to an `EthAccount`.

1. Owner of vesting account submits a `MsgConvertVestingAccount` through one of the clients.
2. Check if
    1. the vesting account exists and is a clawback vesting account
    2. the vesting account's vesting and locked schedules have concluded
3. Convert the vesting account to an `EthAccount`

## Transactions

This section defines the concrete `sdk.Msg` types, that result in the state transitions defined on the previous section.

### `CreateClawbackVestingAccount`

```go
type MsgCreateClawbackVestingAccount struct {
	// funder_address specifies the account that will be able to fund the vesting account
	FunderAddress string `protobuf:"bytes,1,opt,name=funder_address,json=funderAddress,proto3" json:"funder_address,omitempty"`
	// vesting_address specifies the address that will receive the vesting tokens
	VestingAddress string `protobuf:"bytes,2,opt,name=vesting_address,json=vestingAddress,proto3" json:"vesting_address,omitempty"`
	// enable_gov_clawback specifies whether the governance module can clawback this account
	EnableGovClawback bool `protobuf:"varint,3,opt,name=enable_gov_clawback,json=enableGovClawback,proto3" json:"enable_gov_clawback,omitempty"`
}
```

The msg content stateless validation fails if:

- `FunderAddress` or `VestingAddress` are invalid

### `FundVestingAccount`

```go
type MsgFundVestingAccount struct {
	// funder_address specifies the account that funds the vesting account
	FunderAddress string `protobuf:"bytes,1,opt,name=funder_address,json=funderAddress,proto3" json:"funder_address,omitempty"`
	// vesting_address specifies the account that receives the funds
	VestingAddress string `protobuf:"bytes,2,opt,name=vesting_address,json=vestingAddress,proto3" json:"vesting_address,omitempty"`
	// start_time defines the time at which the vesting period begins
	StartTime time.Time `protobuf:"bytes,3,opt,name=start_time,json=startTime,proto3,stdtime" json:"start_time"`
	// lockup_periods defines the unlocking schedule relative to the start_time
	LockupPeriods github_com_cosmos_cosmos_sdk_x_auth_vesting_types.Periods `protobuf:"bytes,4,rep,name=lockup_periods,json=lockupPeriods,proto3,castrepeated=github.com/cosmos/cosmos-sdk/x/auth/vesting/types.Periods" json:"lockup_periods"`
	// vesting_periods defines the vesting schedule relative to the start_time
	VestingPeriods github_com_cosmos_cosmos_sdk_x_auth_vesting_types.Periods `protobuf:"bytes,5,rep,name=vesting_periods,json=vestingPeriods,proto3,castrepeated=github.com/cosmos/cosmos-sdk/x/auth/vesting/types.Periods" json:"vesting_periods"`
}
```

The msg content stateless validation fails if:

- `FunderAddress` or `VestingAddress` are invalid
- `LockupPeriods` and `VestingPeriods`
    - include a period with a non-positive length or amount
    - do not describe the same total amount

### `Clawback`

```go
type MsgClawback struct {
	// funder_address is the address which funded the account
	FunderAddress string `protobuf:"bytes,1,opt,name=funder_address,json=funderAddress,proto3" json:"funder_address,omitempty"`
	// account_address is the address of the ClawbackVestingAccount to claw back from.
	AccountAddress string `protobuf:"bytes,2,opt,name=account_address,json=accountAddress,proto3" json:"account_address,omitempty"`
	// dest_address specifies where the clawed-back tokens should be transferred
	// to. If empty, the tokens will be transferred back to the original funder of
	// the account.
	DestAddress string `protobuf:"bytes,3,opt,name=dest_address,json=destAddress,proto3" json:"dest_address,omitempty"`
}
```

The msg content stateless validation fails if:

- `FunderAddress` or `AccountAddress` are invalid
- `DestAddress` is not empty and invalid

### `UpdateVestingFunder`

```go
type MsgUpdateVestingFunder struct {
	// funder_address is the current funder address of the ClawbackVestingAccount
	FunderAddress string `protobuf:"bytes,1,opt,name=funder_address,json=funderAddress,proto3" json:"funder_address,omitempty"`
	// new_funder_address is the new address to replace the existing funder_address
	NewFunderAddress string `protobuf:"bytes,2,opt,name=new_funder_address,json=newFunderAddress,proto3" json:"new_funder_address,omitempty"`
	// vesting_address is the address of the ClawbackVestingAccount being updated
	VestingAddress string `protobuf:"bytes,3,opt,name=vesting_address,json=vestingAddress,proto3" json:"vesting_address,omitempty"`
}
```

The msg content stateless validation fails if:

- `FunderAddress`, `NewFunderAddress` or `VestingAddress` are invalid

### `ConvertVestingAccount`

```go
type MsgConvertVestingAccount struct {
	// vesting_address is the address of the ClawbackVestingAccount being updated
	VestingAddress string `protobuf:"bytes,2,opt,name=vesting_address,json=vestingAddress,proto3" json:"vesting_address,omitempty"`
}
```

The msg content stateless validation fails if:

- `VestingAddress` is invalid

## AnteHandlers

The `x/vesting` module provides `AnteDecorator`s that are recursively chained together
into a single [`Antehandler`](https://github.com/cosmos/cosmos-sdk/blob/v0.43.0-alpha1/docs/architecture/adr-010-modular-antehandler.md).
These decorators perform basic validity checks on an Ethereum,
such that it could be thrown out of the transaction Mempool.

Note that the `AnteHandler` is called on both `CheckTx` and `DeliverTx`,
as CometBFT proposers presently have the ability to include in their proposed block transactions that fail `CheckTx`.

### Decorators

The following decorators implement the vesting logic for token delegation and performing EVM transactions.

#### `EthVestingTransactionDecorator`

Validates if a clawback vesting account is permitted to perform Ethereum transactions,
based on if it has its vesting schedule has surpassed the vesting cliff and first lockup period.
Also, validates if the account has sufficient unlocked tokens to execute the transaction.
This AnteHandler decorator will fail if:

- the message is not a `MsgEthereumTx`
- sender account cannot be found
- sender account is not a `ClawbackVestingAccount`
- block time is before surpassing vesting cliff end (with zero vested coins) AND
- block time is before surpassing all lockup periods (with non-zero locked coins)
- sender account has insufficient unlocked tokens to execute the transaction

### Custom Staking Module

Evomos introduced the concept of [EVM extensions](https://docs.evmos.org/develop/smart-contracts/evm-extensions) to
allow smart contract to interact with Cosmos SDK modules
like the bank and the staking to provide a better developer experience allowing users to interact with Cosmos native module
via the EVM. Since `ClawbackVestingAccount` are allowed to stake only unlocked & vested coins, or locked & vested,
we have to ensure that all other configurations are not permitted to perform a state transition. Instead of
having these checks implemented in both the `AnteHandler`s for Cosmos transactions and Ethereum transactions,
Evmos core wraps the Cosmos SDK `x/staking` module to introduce these checks in the `MsgServer` of this module.
 With this approach we ensure that all staking actions, through direct Cosmos message or through extensions,
 are validating the
account balance in the proper way.

The staking wrapper uses the same functionalities of the original staking module but introduces required
checks in the following methods:

- `Delegate`
- `CreateValidator`

## Events

The `x/vesting` module emits the following events:

### Create Clawback Vesting Account

| Type                              | Attibute Key   | Attibute Value         |
| --------------------------------- | -------------- | ---------------------- |
| `create_clawback_vesting_account` | `"funder"`     | `{msg.FunderAddress}`  |
| `create_clawback_vesting_account` | `"sender"`     | `{msg.VestingAddress}` |

### Fund Vesting Account

| Type                   | Attibute Key   | Attibute Value             |
| ---------------------- | -------------- | -------------------------- |
| `fund_vesting_account` | `"funder"`     | `{msg.FunderAddress}`      |
| `fund_vesting_account` | `"coins"`      | `{vestingCoins.String()}`  |
| `fund_vesting_account` | `"start_time"` | `{msg.StartTime.String()}` |
| `fund_vesting_account` | `"account"`    | `{msg.VestingAddress}`     |

### Clawback

| Type       | Attibute Key    | Attibute Value         |
| ---------- | --------------- | ---------------------- |
| `clawback` | `"funder"`      | `{msg.FromAddress}`    |
| `clawback` | `"account"`     | `{msg.AccountAddress}` |
| `clawback` | `"destination"` | `{msg.DestAddress}`    |

### Update Clawback Vesting Account Funder

| Type                    | Attibute Key   | Attibute Value           |
| ----------------------- | -------------- | ------------------------ |
| `update_vesting_funder` | `"funder"`     | `{msg.FromAddress}`      |
| `update_vesting_funder` | `"account"`    | `{msg.VestingAddress}`   |
| `update_vesting_funder` | `"new_funder"` | `{msg.NewFunderAddress}` |

## Clients

A user can query the Evmos `x/vesting` module using the CLI, gRPC, or REST.

### CLI

Find below a list of `evmosd` commands added with the `x/vesting` module.
You can obtain the full list by using the `evmosd -h` command.

#### Genesis

The genesis configuration commands allow users to configure the genesis `vesting` account state.

`add-genesis-account`

Allows users to set up clawback vesting accounts at genesis, funded with an allocation of tokens, subject to clawback.
Must provide a lockup periods file (`--lockup`), a vesting periods file (`--vesting`), or both.

If both files are given, they must describe schedules for the same total amount.
If one file is omitted, it will default to a schedule that immediately unlocks or vests the entire amount.
The described amount of coins will be transferred from the --from address to the vesting account.
Unvested coins may be "clawed back" by the funder with the clawback command.
Coins may not be transferred out of the account if they are locked or unvested.
Only vested coins may be staked.
For an example of how to set this see [this link](https://github.com/evmos/evmos/pull/303).

```go
evmosd add-genesis-account ADDRESS_OR_KEY_NAME COIN... [flags]
```

#### Queries

The `query` commands allow users to query `vesting` account state.

**`balances`**

Allows users to query the locked, unvested and vested tokens for a given vesting account

```go
evmosd query vesting balances ADDRESS [flags]
```

#### Transactions

The `tx` commands allow users to create and clawback `vesting` account state.

**`create-clawback-vesting-account`**

A new clawback vesting account is created for the sender account (`--from`),
if it is not already of such type.
Only the designated funder will be able to define lockup and vesting schedules
and has to do so using the fund-vesting-account subcommand.
Clawback via governance is enabled or disabled through the second argument.

```go
evmosd tx vesting create-clawback-vesting-account FUNDER_ADDRESS ENABLE_GOV_CLAWBACK --from=VESTING_ADDRESS [flags]
```

**`fund-vesting-account`**

Allows the funder account to update a clawback vesting account with new schedules.
Any existing schedules are merged with the newly added schedules.
Must provide a lockup periods file (--lockup), a vesting periods file (--vesting), or both.

If both files are given, they must describe schedules for the same total amount.
If one file is omitted, it will default to a schedule that immediately unlocks or vests the entire amount.
The described amount of coins will be transferred from the --from address to the vesting account.
Unvested coins may be "clawed back" by the funder with the clawback command.
Coins may not be transferred out of the account if they are locked or unvested.
Only vested coins may be staked.
For an example of how to set this see [this link](https://github.com/evmos/evmos/pull/303).

```go
evmosd tx vesting fund-vesting-account VESTING_ADDRESS --from=FUNDER_ADDRESS [flags]
```

**`clawback`**

Allows to transfer all unvested unvested tokens out of a ClawbackVestingAccount.
Must be requested by the original funder address (--from) and may provide a destination address (--dest),
otherwise the coins are returned to the funder.
Delegated or unbonding staking tokens will be transferred in the delegated or unbonding state.
The recipient is vulnerable to slashing, and must act to unbond the tokens if desired.

```go
evmosd tx vesting clawback VESTING_ADDRESS --from=FUNDER_ADDRESS [flags]
```

**`update-vesting-funder`**

Allows users to update the funder of an existent `ClawbackVestingAccount`.
Must be requested by the original funder address (`--from`).

```go
evmosd tx vesting update-vesting-funder VESTING_ADDRESS NEW_FUNDER_ADDRESS --from=FUNDER_ADDRESS [flags]
```

**`convert`**

Allows users to convert their vesting account to the chain's default account (i.e `EthAccount`).
This operation only succeeds if there are no unvested tokens left in the account.

```go
evmosd tx vesting convert VESTING_ADDRESS [flags]
```

### gRPC

#### Queries

| Verb   | Method                                 | Description                            |
|--------|----------------------------------------|----------------------------------------|
| `gRPC` | `evmos.vesting.v2.Query/Balances`      | Gets locked, unvested and vested coins |
| `GET`  | `/evmos/vesting/v2/balances/{address}` | Gets locked, unvested and vested coins |

#### Transactions

| Verb   | Method                                                 | Description                                     |
|--------|--------------------------------------------------------|-------------------------------------------------|
| `gRPC` | `evmos.vesting.v2.Msg/CreateClawbackVestingAccount`    | Creates clawback vesting account                |
| `gRPC` | `evmos.vesting.v2.Msg/FundVestingAccount`              | Funds a clawback vesting account                |
| `gRPC` | `/evmos.vesting.v2.Msg/Clawback`                       | Performs clawback                               |
| `gRPC` | `/evmos.vesting.v2.Msg/UpdateVestingFunder`            | Updates vesting account funder                  |
| `gRPC` | `/evmos.vesting.v2.Msg/ConvertVestingAccount`          | Converts vesting account back to normal account |
| `GET`  | `/evmos/vesting/v2/tx/create_clawback_vesting_account` | Creates clawback vesting account                |
| `GET`  | `/evmos/vesting/v2/tx/fund_vesting_account`            | Funds a clawback vesting account                |
| `GET`  | `/evmos/vesting/v2/tx/clawback`                        | Performs clawback                               |
| `GET`  | `/evmos/vesting/v2/tx/update_vesting_funder`           | Updates vesting account funder                  |
| `GET`  | `/evmos/vesting/v2/tx/convert_vesting_account`         | Converts vesting account back to normal account |
