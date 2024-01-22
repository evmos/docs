---
sidebar_position: 3
---

# List of EVM Extensions

## Available Extensions

The following extensions are available in Evmos' implementation of the EVM:

| Address                                      | Name                | Stateful | EIP                                               | Testnet                  | Mainnet                  |
| -------------------------------------------- | ------------------- | -------- | ------------------------------------------------- | ------------------------ | ------------------------ |
| `0x0000000000000000000000000000000000000001` | ecRecover           | No       |                                                   | :heavy_check_mark:       | :heavy_check_mark:       |
| `0x0000000000000000000000000000000000000002` | SHA256 Hash         | No       |                                                   | :heavy_check_mark:       | :heavy_check_mark:       |
| `0x0000000000000000000000000000000000000003` | RIPEMD-160 Hash     | No       |                                                   | :heavy_check_mark:       | :heavy_check_mark:       |
| `0x0000000000000000000000000000000000000004` | Data Copy           | No       |                                                   | :heavy_check_mark:       | :heavy_check_mark:       |
| `0x0000000000000000000000000000000000000005` | ExpMod              | No       | [EIP-198](https://eips.ethereum.org/EIPS/eip-198) | :heavy_check_mark:       | :heavy_check_mark:       |
| `0x0000000000000000000000000000000000000006` | BN256Add            | No       | [EIP-196](https://eips.ethereum.org/EIPS/eip-196) | :heavy_check_mark:       | :heavy_check_mark:       |
| `0x0000000000000000000000000000000000000007` | BN256ScalarMul      | No       | [EIP-196](https://eips.ethereum.org/EIPS/eip-196) | :heavy_check_mark:       | :heavy_check_mark:       |
| `0x0000000000000000000000000000000000000008` | BN256Pairing        | No       | [EIP-197](https://eips.ethereum.org/EIPS/eip-197) | :heavy_check_mark:       | :heavy_check_mark:       |
| `0x0000000000000000000000000000000000000009` | Blake2F             | No       | [EIP-152](https://eips.ethereum.org/EIPS/eip-152) | :heavy_check_mark:       | :heavy_check_mark:       |
| `0x0000000000000000000000000000000000000400` | Bech32 encoding     | No       |                                                   | :heavy_multiplication_x: | :heavy_multiplication_x: |
| `0x0000000000000000000000000000000000000800` | Staking module      | Yes      |                                                   | :heavy_check_mark:       | :heavy_check_mark:       |
| `0x0000000000000000000000000000000000000801` | Distribution module | Yes      |                                                   | :heavy_check_mark:       | :heavy_check_mark:       |
| `0x0000000000000000000000000000000000000802` | IBC Transfer        | Yes      |                                                   | :heavy_check_mark:       | :heavy_check_mark:       |
| `0x0000000000000000000000000000000000000803` | Vesting module      | Yes      |                                                   | :heavy_check_mark:       | :heavy_check_mark:       |

## Further Reading

- [EVM Codes: Precompiled Contracts](https://www.evm.codes/precompiled)
