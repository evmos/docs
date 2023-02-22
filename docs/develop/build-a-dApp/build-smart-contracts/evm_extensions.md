---
sidebar_position: 3
---

# List of EVM Extensions

## Available Extensions

The following extensions are available in Evmos' implementation of the EVM:

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

- [EVM Codes: Precompiled Contracts](https://www.evm.codes/precompiled)
