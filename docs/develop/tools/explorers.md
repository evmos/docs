---
sidebar_position: 1
---

# Block Explorers

Blockchain explorers allow users to query the blockchain for data. Explorers are often compared to search engines for the blockchain. By using an explorer, users can search and track balances, transactions, contracts, and other broadcast data to the blockchain.

Evmos offers two types block explorers: an EVM explorer and a Cosmos explorer. Each explorer queries data respective to their environment with the EVM explorers querying Ethereum-formatted data (blocks, transactions, accounts, smart contracts, etc) and the Cosmos explorers querying Cosmos-formatted data (Cosmos and IBC transactions, blocks, accounts, module data, etc).

## List of Block Explorers

Below is a list of public block explorers that support Evmos Mainnet and Testnet:

### Mainnet

|  Service   | Support       | URL                                                    | Contract Verification  |
|------------| -------------- |--------------------------------------------------------|-----------------------|
| Mintscan   | `cosmos` `evm` | [mintscan.io/evmos](https://www.mintscan.io/evmos)     | Yes but requires form submission  |
| Escan      | `cosmos` `evm` | [escan.live](https://escan.live)                       | Permissionless  |
| BigDipper  | `cosmos`       | [evmos.bigdipper.live/](https://evmos.bigdipper.live/) | No  |
| ATOMScan   | `cosmos`       | [atomscan.com/evmos](https://atomscan.com/evmos)       | No  |
| NGExplorer | `cosmos`       | [evmos.explorers.guru](https://evmos.explorers.guru)   | No  |

### Testnet

| Service    | Support        | URL                                                                            |
| ---------- | -------------- | ------------------------------------------------------------------------------ |
| Escan      | `cosmos` `evm` | [testnet.escan.live](https://testnet.escan.live)                               |
| Mintscan   | `cosmos` `evm` | [testnet.mintscan.io/evmos-testnet](https://testnet.mintscan.io/evmos-testnet) |
| BigDipper  | `cosmos`       | [testnet.bigdipper.live](https://testnet.evmos.bigdipper.live/)                |
| Blockscout | `evm`          | [evm.evmos.dev](https://evm.evmos.dev/)                                        |
| NGExplorer | `cosmos`       | [testnet.evmos.explorers.guru](https://testnet.evmos.explorers.guru)           |
