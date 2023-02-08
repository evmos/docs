---
sidebar_position: 3
---

# EVM Extensions

## Overview

Precompiled smart contracts are smart contracts
that are built into the Ethereum Virtual Machine (EVM).
Each offers specific functionality, that can be used by other smart contracts.
Generally, they are used to perform operations that are either not possible
or would be too expensive to perform
with a regular smart contract implementation,
such as hashing, elliptic curve cryptography, and modular exponentiation.

By adding custom precompiled smart contracts to Ethereum's basic feature set,
Evmos allows developers to use previously unavailable functionality in smart contracts,
like staking and governance operations.
This will allow more complex smart contracts to be built on Evmos
and further improves the interoperability between Cosmos and Ethereum.
It also is a key feature to achieve Evmos' vision
of being the definitive dApp chain, where any dApp can be deployed once
and users are able to interact with a wide range of different blockchains natively.

## Available Precompiled Contracts

The following precompiled contracts are available in Evmos' implementation of the EVM:

| Address                                      | Name            | Stateful | EIP                                               |
|----------------------------------------------|-----------------|----------|---------------------------------------------------|
| `0x0000000000000000000000000000000000000001` | ecRecover       | No       |                                                   |
| `0x0000000000000000000000000000000000000002` | SHA256 Hash     | No       |                                                   |
| `0x0000000000000000000000000000000000000003` | RIPEMD-160 Hash | No       |                                                   |
| `0x0000000000000000000000000000000000000004` | Data Copy       | No       |                                                   |
| `0x0000000000000000000000000000000000000005` | ExpMod          | No       | [EIP-198](https://eips.ethereum.org/EIPS/eip-198) |
| `0x0000000000000000000000000000000000000006` | BN256Add        | No       | [EIP-196](https://eips.ethereum.org/EIPS/eip-196) |
| `0x0000000000000000000000000000000000000007` | BN256ScalarMul  | No       | [EIP-196](https://eips.ethereum.org/EIPS/eip-196) |
| `0x0000000000000000000000000000000000000008` | BN256Pairing    | No       | [EIP-197](https://eips.ethereum.org/EIPS/eip-197) |
| `0x0000000000000000000000000000000000000009` | Blake2F         | No       | [EIP-152](https://eips.ethereum.org/EIPS/eip-152) |

## Further Reading

- [EVM Codes: Precompiled](https://www.evm.codes/precompiled)
