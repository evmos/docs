---
sidebar_position: 1
---

# Accounts

Crypto Wallets (or Accounts) can be created
and represented in unique ways on different blockchains.
For developers who interface with account types on Evmos,
e.g. during wallet integration on their dApp frontend,
it is therefore important to understand that accounts on Evmos are implemented
to be compatible with Ethereum type addresses.

## Prerequisite Readings

- [Cosmos SDK Accounts](https://docs.cosmos.network/main/basics/accounts.html)
- [Ethereum Accounts](https://ethereum.org/en/whitepaper/#ethereum-accounts)

## Creating Accounts

To create one account you can either
create a private key, a keystore file (a private key protected by a password),
or a mnemonic phrase (a string of words that can access multiple private keys).

Aside from having different security features,
the biggest difference between each of these is
that a private key or keystore file only creates one account.
Creating a mnemonic phrase gives you control of many accounts,
all accessible with that same phrase.

Cosmos blockchains, like Evmos, support creating accounts with mnemonic phrases,
otherwise known as [hierarchical deterministic key generation](https://github.com/confio/cosmos-hd-key-derivation-spec) (HD keys).
This allows the user to create accounts on multiple blockchains
without having to manage multiple secrets.

HD keys generate addresses by taking the mnemonic phrase
and combining it with a piece of information called a [derivation path](https://learnmeabitcoin.com/technical/derivation-paths).
Blockchains can differ in which derivation path they support.
To access all accounts from an mnemonic phrase on a blockchain,
it is therefore important to use that blockchain's specific derivation path.

## Representing Accounts

The terms "account" and "address" are often used interchangeably to describe crypto wallets.
In the Cosmos SDK, an account designates a pair of public key (PubKey) and private key (PrivKey).
The derivation path defines what the private key, public key, and address would be.

The PubKey can be derived to generate various addresses in different formats,
which are used to identify users (among other parties) in the application.
A common address form for Cosmos chains is the bech32 format (e.g. `evmos1...`).
Addresses are also associated with messages to identify the sender of the message.

The PrivKey is used to generate digital signatures to prove
that an address associated with the PrivKey approved of a given message.
The proof is performed by applying a cryptographic scheme to the PrivKey,
known as Elliptic Curve Digital Signature Algorithm (ECDSA),
to generate a PubKey that is compared with the address in the message.

## Evmos Accounts

Evmos defines its own custom `Account` type
to implement a HD wallet that is compatible with Ethereum type addresses.
It uses Ethereum's ECDSA secp256k1 curve for keys (`eth_secp265k1`)
and satisfies the [EIP84](https://github.com/ethereum/EIPs/issues/84)
for full [BIP44](https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki) paths.
This cryptographic curve is not to be confused with [Bitcoin's ECDSA secp256k1](https://en.bitcoin.it/wiki/Secp256k1) curve.

The root HD path for Evmos-based accounts is `m/44'/60'/0'/0`.
Evmos uses the Coin type `60` to support Ethereum type accounts,
unlike many other Cosmos chains that use Coin type `118` ([list of coin types](https://github.com/satoshilabs/slips/blob/master/slip-0044.md)

The custom Evmos [EthAccount](https://github.com/evmos/evmos/blob/main/types/account.go#L28-L33)
satisfies the `AccountI` interface from the Cosmos SDK auth module
and includes additional fields that are required for Ethereum type addresses:

```go
// EthAccountI represents the interface of an EVM compatible account
type EthAccountI interface {
	authtypes.AccountI
	// EthAddress returns the ethereum Address representation of the AccAddress
	EthAddress() common.Address
	// CodeHash is the keccak256 hash of the contract code (if any)
	GetCodeHash() common.Hash
	// SetCodeHash sets the code hash to the account fields
	SetCodeHash(code common.Hash) error
	// Type returns the type of Ethereum Account (EOA or Contract)
	Type() int8
}
```

For more information on Ethereum accounts head over to the [x/evm module](../modules/evm.md#concepts).

### Addresses and Public Keys

[BIP-0173](https://github.com/satoshilabs/slips/blob/master/slip-0173.md) defines a new format for segregated witness
output addresses that contains a human-readable part that identifies the Bech32 usage. Evmos uses the following
HRP (human readable prefix) as the base HRP:

| Network   | Mainnet | Testnet |
|-----------|---------|---------|
| Evmos     | `evmos` | `evmos` |

There are 3 main types of HRP for the `Addresses`/`PubKeys` available by default on Evmos:

- Addresses and Keys for **accounts**, which identify users (e.g. the sender of a `message`). They are derived using
 the **`eth_secp256k1`** curve.
- Addresses and Keys for **validator operators**, which identify the operators of validators. They are derived using
 the **`eth_secp256k1`** curve.
- Addresses and Keys for **consensus nodes**, which identify the validator nodes participating in consensus. They are
 derived using the **`ed25519`** curve.

|                    | Address bech32 Prefix | Pubkey bech32 Prefix | Curve           | Address byte length | Pubkey byte length |
|--------------------|-----------------------|----------------------|-----------------|---------------------|--------------------|
| Accounts           | `evmos`               | `evmospub`           | `eth_secp256k1` | `20`                | `33` (compressed)  |
| Validator Operator | `evmosvaloper`        | `evmosvaloperpub`    | `eth_secp256k1` | `20`                | `33` (compressed)  |
| Consensus Nodes    | `evmosvalcons`        | `evmosvalconspub`    | `ed25519`       | `20`                | `32`               |

### Address formats for clients

`EthAccount` can be represented in both [Bech32](https://en.bitcoin.it/wiki/Bech32) (`evmos1...`) and hex (`0x...`) formats for Ethereum's Web3 tooling compatibility.

The Bech32 format is the default format for Cosmos-SDK queries and transactions through CLI and REST
clients. The hex format on the other hand, is the Ethereum `common.Address` representation of a
Cosmos `sdk.AccAddress`.

- **Address (Bech32)**: `evmos1z3t55m0l9h0eupuz3dp5t5cypyv674jj7mz2jw`
- **Address ([EIP55](https://eips.ethereum.org/EIPS/eip-55) Hex)**: `0x91defC7fE5603DFA8CC9B655cF5772459BF10c6f`
- **Compressed Public Key**: `{"@type":"/ethermint.crypto.v1.ethsecp256k1.PubKey","key":"AsV5oddeB+hkByIJo/4lZiVUgXTzNfBPKC73cZ4K1YD2"}`

### Address conversion

The `evmosd debug addr <address>` can be used to convert an address between hex and bech32 formats. For example:

```bash title="Bech32"
 $ evmosd debug addr evmos1z3t55m0l9h0eupuz3dp5t5cypyv674jj7mz2jw
  Address: [20 87 74 109 255 45 223 158 7 130 139 67 69 211 4 9 25 175 86 82]
  Address (hex): 14574A6DFF2DDF9E07828B4345D3040919AF5652
  Bech32 Acc: evmos1z3t55m0l9h0eupuz3dp5t5cypyv674jj7mz2jw
  Bech32 Val: evmosvaloper1z3t55m0l9h0eupuz3dp5t5cypyv674jjn4d6nn
```

```bash title="Hex"
 $ evmosd debug addr 14574A6DFF2DDF9E07828B4345D3040919AF5652
  Address: [20 87 74 109 255 45 223 158 7 130 139 67 69 211 4 9 25 175 86 82]
  Address (hex): 14574A6DFF2DDF9E07828B4345D3040919AF5652
  Bech32 Acc: evmos1z3t55m0l9h0eupuz3dp5t5cypyv674jj7mz2jw
  Bech32 Val: evmosvaloper1z3t55m0l9h0eupuz3dp5t5cypyv674jjn4d6nn
```

### Key output

:::tip
The Cosmos SDK Keyring output (i.e `evmosd keys`) only supports addresses and public keys in Bech32 format.
:::

We can use the `keys show` command of `evmosd` with the flag `--bech <type> (acc|val|cons)` to
obtain the addresses and keys as mentioned above,

```bash title="Accounts"
 $ evmosd keys show dev0 --bech acc
- name: dev0
  type: local
  address: evmos1z3t55m0l9h0eupuz3dp5t5cypyv674jj7mz2jw
  pubkey: '{"@type":"/ethermint.crypto.v1.ethsecp256k1.PubKey","key":"AsV5oddeB+hkByIJo/4lZiVUgXTzNfBPKC73cZ4K1YD2"}'
  mnemonic: ""
```

```bash title="Validator"
 $ evmosd keys show dev0 --bech val
- name: dev0
  type: local
  address: evmosvaloper1z3t55m0l9h0eupuz3dp5t5cypyv674jjn4d6nn
  pubkey: '{"@type":"/ethermint.crypto.v1.ethsecp256k1.PubKey","key":"AsV5oddeB+hkByIJo/4lZiVUgXTzNfBPKC73cZ4K1YD2"}'
  mnemonic: ""
```

```bash title="Consensus"
 $ evmosd keys show dev0 --bech cons
- name: dev0
  type: local
  address: evmosvalcons1rllqa5d97n6zyjhy6cnscc7zu30zjn3f7wyj2n
  pubkey: '{"@type":"/ethermint.crypto.v1.ethsecp256k1.PubKey","key":"A/fVLgIqiLykFQxum96JkSOoTemrXD0tFaFQ1B0cpB2c"}'
  mnemonic: ""
```

## Querying an Account

You can query an account address using the CLI, gRPC or

### Command Line Interface

```bash
# NOTE: the --output (-o) flag will define the output format in JSON or YAML (text)
evmosd q auth account $(evmosd keys show dev0 -a) -o text

'@type': /ethermint.types.v1.EthAccount
base_account:
account_number: "0"
address: evmos1z3t55m0l9h0eupuz3dp5t5cypyv674jj7mz2jw
pub_key:
  '@type': /ethermint.crypto.v1.ethsecp256k1.PubKey
  key: AsV5oddeB+hkByIJo/4lZiVUgXTzNfBPKC73cZ4K1YD2
sequence: "1"
code_hash: 0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470
```

### Cosmos gRPC and REST

``` bash
# GET /cosmos/auth/v1beta1/accounts/{address}
curl -X GET "http://localhost:10337/cosmos/auth/v1beta1/accounts/evmos14au322k9munkmx5wrchz9q30juf5wjgz2cfqku" -H "accept: application/json"
```

### JSON-RPC

To retrieve the Ethereum hex address using Web3, use the JSON-RPC [`eth_accounts`](./../../develop/api/ethereum-json-rpc/methods#eth-accounts) or [`personal_listAccounts`](./../../develop/api/ethereum-json-rpc/methods#personal-listAccounts) endpoints:

```bash
# query against a local node
curl -X POST --data '{"jsonrpc":"2.0","method":"eth_accounts","params":[],"id":1}' -H "Content-Type: application/json" http://localhost:8545

curl -X POST --data '{"jsonrpc":"2.0","method":"personal_listAccounts","params":[],"id":1}' -H "Content-Type: application/json" http://localhost:8545
```
