# Key Management

All of these wallets will issue a mnemonic seed or private key and it is critical to handle this information carefully. It is vital to secure this phrase or key and backup this phrase. There are no `Forget Your Password`. Many wallets will require a password to secure the account. Using a strong and unique password will ensure better likelihood of wallet safety.

## Mnemonics from the Evmos CLI

:::note
Before proceeding with the CLI, please insure you have `evmosd` installed. Installation instruction are located [here](../../develop/build-a-dApp/run-a-node/installation).
:::

When you create a new key, you'll receive a mnemonic phrase that can be used to restore that key. Backup the mnemonic phrase:

```bash
evmosd keys add dev0
{
  "name": "dev0",
  "type": "local",
  "address": "evmos1n253dl2tgyhxjm592p580c38r4dn8023ctv28d",
  "pubkey": '{"@type":"/ethermint.crypto.v1.ethsecp256k1.PubKey","key":"ArJhve4v5HkLm+F7ViASU/rAGx7YrwU4+XKV2MNJt+Cq"}',
  "mnemonic": ""
}

**Important** write this mnemonic phrase in a safe place.
It is the only way to recover your account if you ever forget your password.

# <24 word mnemonic phrase>
```

To restore the key:

```bash
$ evmosd keys add dev0-restored --recover
> Enter your bip39 mnemonic
banner genuine height east ghost oak toward reflect asset marble else explain foster car nest make van divide twice culture announce shuffle net peanut
{
  "name": "dev0-restored",
  "type": "local",
  "address": "evmos1n253dl2tgyhxjm592p580c38r4dn8023ctv28d",
  "pubkey": '{"@type":"/ethermint.crypto.v1.ethsecp256k1.PubKey","key":"ArJhve4v5HkLm+F7ViASU/rAGx7YrwU4+XKV2MNJt+Cq"}'
}
```

## Export Key

### Tendermint-Formatted Private Keys

To backup this type of key without the mnemonic phrase, do the following:

```bash
evmosd keys export dev0
Enter passphrase to decrypt your key:
Enter passphrase to encrypt the exported key:
-----BEGIN TENDERMINT PRIVATE KEY-----
kdf: bcrypt
salt: 14559BB13D881A86E0F4D3872B8B2C82
type: secp256k1

# <Tendermint private key>
-----END TENDERMINT PRIVATE KEY-----

$ echo "\
-----BEGIN TENDERMINT PRIVATE KEY-----
kdf: bcrypt
salt: 14559BB13D881A86E0F4D3872B8B2C82
type: secp256k1

# <Tendermint private key>
-----END TENDERMINT PRIVATE KEY-----" > dev0.export
```

### Ethereum-Formatted Private Keys

:::tip
**Note**: These types of keys are MetaMask-compatible.
:::

To backup this type of key without the mnemonic phrase, do the following:

```bash
evmosd keys unsafe-export-eth-key dev0 > dev0.export
**WARNING** this is an unsafe way to export your unencrypted private key, are you sure? [y/N]: y
Enter keyring passphrase:
```

## Import Key

### Tendermint-Formatted Private Keys

```bash
$ evmosd keys import dev0-imported ./dev0.export
Enter passphrase to decrypt your key:
```

### Ethereum-Formatted Private Keys

```
$ evmosd keys unsafe-import-eth-key dev0-imported ./dev0.export
Enter passphrase to encrypt your key:
```

### Verification

Verify that your key has been restored using the following command:

```bash
$ evmosd keys list
[
  {
    "name": "dev0-imported",
    "type": "local",
    "address": "evmos1n253dl2tgyhxjm592p580c38r4dn8023ctv28d",
    "pubkey": '{"@type":"/ethermint.crypto.v1.ethsecp256k1.PubKey","key":"ArJhve4v5HkLm+F7ViASU/rAGx7YrwU4+XKV2MNJt+Cq"}'
  },
  {
    "name": "dev0-restored",
    "type": "local",
    "address": "evmos1n253dl2tgyhxjm592p580c38r4dn8023ctv28d",
    "pubkey": '{"@type":"/ethermint.crypto.v1.ethsecp256k1.PubKey","key":"ArJhve4v5HkLm+F7ViASU/rAGx7YrwU4+XKV2MNJt+Cq"}'
  },
  {
    "name": "dev0",
    "type": "local",
    "address": "evmos1n253dl2tgyhxjm592p580c38r4dn8023ctv28d",
    "pubkey": '{"@type":"/ethermint.crypto.v1.ethsecp256k1.PubKey","key":"ArJhve4v5HkLm+F7ViASU/rAGx7YrwU4+XKV2MNJt+Cq"}'
  }
]
```
