# EVM Extensions

Stateful EVM Extensions on the core protocol allow dApps and users to access logic outside of the EVM.
Acting as a gateway, these EVM Extensions define how smart contracts can perform cross-chain transactions
(via IBC) and interact with core functionalities on the Evmos chain (e.g. staking, voting) from the EVM.

:::tip
**Note**: Not sure what EVM extensions are?
EVM extensions behave like smart contracts that are compiled and deployed within the EVM.
If you are familiar with the EVM, you may know them as Precompiles.
These have predefined addresses and, according to their logic, can be classified as stateful or stateless.
When they change the state of the chain (transactions)
or access state data (queries), extensions are considered "stateful";
when they don't, they're "stateless".
:::

## EVM Extensions documentation

Find in this section an outline of the currently implemented EVM extensions with transactions,
queries, and examples of using them:

- [Authorization interfaces (read first if you're new to EVM extensions)](./authorization.md)
- [EVM Extensions shared types](./types.md)
- [`x/staking` module EVM extension](./staking.md)
- [`x/distribution` module EVM extension](./distribution.md)

:::tip
**Note**: Find the EVM Extensions Solidity interfaces and examples in the [Evmos Extensions repo](https://github.com/evmos/extensions).
:::

## List of EVM Extensions

### Available Extensions

The following extensions are available in Evmos' implementation of the EVM:

| Address                                      | Name                | Stateful | EIP                                               |
| -------------------------------------------- | ------------------- | -------- | ------------------------------------------------- |
| `0x0000000000000000000000000000000000000001` | ecRecover           | No       |                                                   |
| `0x0000000000000000000000000000000000000002` | SHA256 Hash         | No       |                                                   |
| `0x0000000000000000000000000000000000000003` | RIPEMD-160 Hash     | No       |                                                   |
| `0x0000000000000000000000000000000000000004` | Data Copy           | No       |                                                   |
| `0x0000000000000000000000000000000000000005` | ExpMod              | No       | [EIP-198](https://eips.ethereum.org/EIPS/eip-198) |
| `0x0000000000000000000000000000000000000006` | BN256Add            | No       | [EIP-196](https://eips.ethereum.org/EIPS/eip-196) |
| `0x0000000000000000000000000000000000000007` | BN256ScalarMul      | No       | [EIP-196](https://eips.ethereum.org/EIPS/eip-196) |
| `0x0000000000000000000000000000000000000008` | BN256Pairing        | No       | [EIP-197](https://eips.ethereum.org/EIPS/eip-197) |
| `0x0000000000000000000000000000000000000009` | Blake2F             | No       | [EIP-152](https://eips.ethereum.org/EIPS/eip-152) |
| `0x0000000000000000000000000000000000000400` | Bech32 encoding     | No       |                                                   |
| `0x0000000000000000000000000000000000000800` | Staking module      | Yes      |                                                   |
| `0x0000000000000000000000000000000000000801` | Distribution module | Yes      |                                                   |

### Further Reading

- [EVM Codes: Precompiled Contracts](https://www.evm.codes/precompiled)
