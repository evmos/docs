# `recovery`

Recover tokens that are stuck on unsupported Evmos accounts.

## Abstract

This document specifies the  `x/recovery` module of the Evmos Hub.

The `x/recovery` module enables users on Evmos to recover locked funds
that were transferred to accounts whose keys are not supported on Evmos.
This happened in particular after the initial Evmos launch (`v1.1.2`),
where users transferred tokens to a `secp256k1` Evmos address via IBC
in order to [claim their airdrop](https://docs.evmos.org/modules/claims/).
To be EVM compatible,
[keys on Evmos](https://docs.evmos.org/users/technical_concepts/accounts.html#evmos-accounts) are generated
using the `eth_secp256k1` key type which results in a different address derivation
than e.g. the `secp256k1` key type used by other Cosmos chains.

At the time of Evmos’ relaunch,
the value of locked tokens on unsupported accounts sits at $36,291.28 worth of OSMO and $268.86 worth of ATOM tokens
according to the [Mintscan](https://www.mintscan.io/evmos/assets) block explorer.
With the `x/recovery` module, users can recover these tokens back to their own addresses
in the originating chains by performing IBC transfers from authorized IBC channels
(i.e. Osmosis for OSMO, Cosmos Hub for ATOM).

## Contents

1. **[Concepts](#concepts)**
2. **[Hooks](#hooks)**
3. **[Events](#events)**
4. **[Parameters](#parameters)**
5. **[Clients](#clients)**

## Concepts

### Key generation

`secp256k1` refers to the parameters of the elliptic curve used in generating cryptographic public keys.
Like Bitcoin, IBC compatible chains like the Cosmos chain use `secp256k1` for public key generation.

Some chains use different elliptic curves for generating public keys.
An example is the`eth_secp256k1`used by Ethereum and Evmos chain for generating public keys.

```go
// Generate new random ethsecp256k1 private key and address

ethPrivKey, err := ethsecp256k1.GenerateKey()
ethsecpAddr := sdk.AccAddress(ethPrivKey.PubKey().Address())

// Bech32 "evmos" address
ethsecpAddrEvmos := sdk.AccAddress(ethPk.PubKey().Address()).String()

// We can also change the HRP to use "cosmos"
ethsecpAddrCosmos := sdk.MustBech32ifyAddressBytes(sdk.Bech32MainPrefix, ethsecpAddr)
```

The above example code demonstrates a simple user account creation on Evmos.
On the second line, a private key is generated using the `eth_secp256k1` curve,
which is used to create a human readable `PubKey` string.
For more detailed info on accounts,
please check the [accounts section](https://docs.evmos.org/users/technical_concepts/accounts.html#evmos-accounts)
in the official Evmos documentation.

### Stuck funds

The primary use case of the `x/recovery` module is to enable the recovery of tokens,
that were sent to unsupported Evmos addresses.
These tokens are termed “stuck”, as the account’s owner cannot sign transactions
that transfer the tokens to other accounts.
The owner only holds the private key to sign transactions for its `eth_secp256k1` public keys on Evmos,
not other unsupported keys (i.e. `secp256k1` keys).
They are unable to transfer the tokens using the keys of the accounts through which they were sent
due to the incompatibility of their elliptic curves.

### Recovery

After the initial Evmos launch (`v1.1.2`), tokens got stuck from accounts with
and without claims records (airdrop allocation):

1. Osmosis/Cosmos Hub account without claims record sent IBC transfer to Evmos `secp256k1` receiver address

   **Consequences**

    - IBC vouchers from IBC transfer got stuck in the receiver’s balance

   **Recovery procedure**

    - The receiver can send an IBC transfer from their Osmosis / Cosmos Hub account (i.e `osmo1...` or `cosmos1...`)
      to its same Evmos account (`evmos1...`) to recover the tokens
      by forwarding them to the corresponding sending chain (Osmosis or Cosmos Hub)

2. Osmosis/Cosmos Hub account with claims record sent IBC transfer to Evmos `secp256k1` receiver address

   **Consequences**

    - IBC vouchers  from IBC transfer got stuck in the receiver’s balance
    - IBC Transfer Action was claimed
      and the EVMOS rewards were transferred to the receiver’s Evmos `secp256k1` account,
      resulting in stuck EVMOS tokens.
    - Claims record of the sender was migrated to the receiver’s Evmos `secp256k1` account

   **Recovery procedure**

    - The receiver can send an IBC transfer from their Osmosis / Cosmos Hub  account (i.e `osmo1...` or `cosmos1...`)
      to its same Evmos account (`evmos1...`) to recover the tokens
      by forwarding them to the corresponding sending chain (Osmosis or Cosmos Hub)
    - Migrate once again the claims record to a valid account so that the remaining 3 actions can be claimed
    - Chain is restarted with restored Claims records

### IBC Middleware Stack

#### Middleware ordering

The IBC middleware adds custom logic between the core IBC and the underlying application.
Middlewares are implemented as stacks so that applications can define multiple layers of custom behavior.

The order of middleware matters.
Function calls from IBC core to the application travel from top-level middleware to the bottom middleware
and then to the application,
whereas function calls from the application to IBC core go through the bottom middleware first
and then in order to the top middleware and then to core IBC handlers.
Thus, the same set of middleware put in different orders may produce different effects.

During packet execution each middleware in the stack will be executed in the order defined on creation
(from top to bottom).

For Evmos the middleware stack ordering is defined as follows (from top to bottom):

1. IBC Transfer
2. Claims Middleware
3. Recovery Middleware

This means that the IBC transfer will be executed first, then the claim will be attempted
and lastly the recovery will be executed.
By performing the actions in this order we allow the users to receive back the coins used to trigger the recover.

**Example execution order**

1. User attempts to recover `1000aevmos` that are stuck on the Evmos chain.
2. User sends `100uosmo` from Osmosis to Evmos through an IBC transaction.
3. Evmos receives the transaction, and goes through the IBC stack:
    1. **IBC transfer**: the `100uosmo` IBC vouchers are added to the user balance on evmos.
    2. **Claims Middleware**: since `sender=receiver` -> perform no-op
    3. **Recovery Middleware**: since `sender=receiver` -> recover user balance (`1000aevmos` and `100uosmo`)
       by sending an IBC transfer from `receiver` to the `sender` on the Osmosis chain.
4. User receives `100uosmo` and `1000aevmos` (IBC voucher) on Osmosis.

#### Execution errors

It is possible that the IBC transaction fails in any point of the stack execution
and in that case the recovery will not be triggered by the transaction, as it will rollback to the previous state.

So if at any point either the IBC transfer or the claims middleware return an error,
then the recovery middleware will not be executed.


## Hooks

The `x/recovery` module allows for state transitions that return IBC tokens
that were previously transferred to EVMOS back to the source chains into the source accounts
with the `Keeper.OnRecvPacket` callback.
The source chain must be authorized.

### Withdraw

A user performs an IBC transfer to return the tokens that they previously transferred
to their Cosmos `secp256k1` address instead of the Ethereum `ethsecp256k1` address.
The behavior is implemented using an IBC`OnRecvPacket` callback.

1. A user performs an IBC transfer to their own account by sending tokens from their address on an authorized chain
   (e.g. `cosmos1...`) to their evmos `secp2561` address (i.e. `evmos1`)  which holds the stuck tokens.
   This is done using a
   [`FungibleTokenPacket`](https://github.com/cosmos/ibc/blob/master/spec/app/ics-020-fungible-token-transfer/README.md)
   IBC packet.

2. Check that the withdrawal conditions are met and skip to the next middleware if any condition is not satisfied:

    1. recovery is enabled globally
    2. channel is authorized
    3. channel is not an EVM channel (as an EVM supports `eth_secp256k1` keys and tokens are not stuck)
    4. sender and receiver address belong to the same account as recovery
       is only possible for transfers to a sender's own account on Evmos.
       Both sender and recipient addresses are therefore converted from `bech32` to `sdk.AccAddress`.
    5. the sender/recipient account is a not vesting or module account
    6. recipient pubkey is not a supported key (`eth_secp256k1`, `amino multisig`, `ed25519`),
       as in this case tokens are not stuck and don’t require recovery

3. Check if sender/recipient address is blocked by the `x/bank` module
   and throw an acknowledgment error to prevent further execution along with the IBC middleware stack
4. Perform recovery to transfer the recipient’s balance back to the sender address with the IBC `OnRecvPacket` callback.
   There are two cases:

    1. First transfer from authorized source chain:
        1. sends back IBC tokens that originated from the source chain
        2. sends over all Evmos native tokens
    2. Second and further transfers from a different authorized source chain
        1. only sends back IBC tokens that originated from the source chain

5. If the recipient does not have any balance, return without recovering tokens


## Events

The `x/recovery` module emits the following event:

### Recovery

| Type       |    Attribute Key     |             Attribute Value |
| :--------- | :------------------- | :-------------------------- |
| `recovery` |       `sender`       |              `senderBech32` |
| `recovery` |      `receiver`      |           `recipientBech32` |
| `recovery` |       `amount`       |                    `amtStr` |
| `recovery` | `packet_src_channel` |      `packet.SourceChannel` |
| `recovery` |  `packet_src_port`   |         `packet.SourcePort` |
| `recovery` | `packet_dst_channel` |    `packet.DestinationPort` |
| `recovery` |  `packet_dst_port`   | `packet.DestinationChannel` |


## Parameters

The `x/recovery` module contains the following parameters:

| Key                     |      Type       |             Default Value |
| :---------------------- | :-------------- | :------------------------ |
| `EnableRecovery`        |     `bool`      |                    `true` |
| `PacketTimeoutDuration` | `time.Duration` | `14400000000000`  // 4hrs |

### Enable Recovery

The `EnableRecovery` parameter toggles Recovery IBC middleware.
When the parameter is disabled, it will disable the recovery of stuck tokens to users.

### Packet Timeout Duration

The `PacketTimeoutDuration` parameter is the duration before the IBC packet timeouts
and the transaction is reverted on the counter party chain.


## Clients

A user can query the `x/recovery` module using the CLI, gRPC or REST.

### CLI

Find below a list of `evmosd` commands added with the `x/recovery` module.
You can obtain the full list by using the `evmosd` -h command.

#### Queries

The query commands allow users to query Recovery state.

**`params`**
Allows users to query the module parameters.

```bash
evmosd query recovery params [flags]
```

### gRPC

#### Queries

| Verb   |              Method              |           Description |
| :----- | :------------------------------- | :-------------------- |
| `gRPC` | `evmos.recovery.v1.Query/Params` | `Get Recovery params` |
| `GET`  |   `/evmos/recovery/v1/params`    | `Get Recovery params` |

