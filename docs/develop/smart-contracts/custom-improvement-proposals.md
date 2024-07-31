# Custom Improvement Proposals

With the release [v19.0.0](https://github.com/evmos/evmos/releases/tag/v19.0.0)
a new feature called custom improvement proposals has been introduced in the
evmOS framework. Custom improvement proposals allow protocol developers to
modify the behavior of the EVM opcodes to tailor their functionalities to the
specific needs.

Improvement proposals are a way to introduce new standards, aimed to improve
protocol functionalities. Changes proposed in this way can affect any aspect
of the protocol but are mainly used to customize the behavior of
smart contract execution.

## Operations

Operations are the base components of the Ethereum Virtual Machine (EVM) which
allow the execution of the smart contract logic. When a developer builds a smart
contract, the code written in Solidity, or Vyper, is not directly interpretable
by the EVM. Before being able to execute the code in the blockchain, the
contract has to be compiled via one of the available compilers, like
[solc](https://docs.soliditylang.org/en/latest/using-the-compiler.html). The
compilation converts the human-readable contract code into a sequence of operations
that the virtual machine can interpret and execute
to perform state transitions or query the latest committed state.
These operations are called **opcodes**, and are contained
in a structure called [**jump table**](https://github.com/evmos/evmos/blob/v19.0.0/x/evm/core/vm/jump_table.go#L120-L1094).

Each opcode is defined by specifying the logic that has to be executed when it
is called inside the EVM, its relationship with the memory, and the gas cost
associated with it. More specifically, an opcode is completely defined by:

- `SetExecute`: update the execution logic for the opcode.

- `SetConstantGas`: update the value used for the constant gas cost.

- `SetDynamicGas`: update the function used to compute the dynamic gas cost.

- `SetMinStack`: update the minimum number of items in the stack required to
execute the operation.

- `SetMaxStack`: update the maximum number of items that will be in the stack
after executing the operation.

- `SetMemorySize`: the memory size required by the operation.

Within the evmOS framework, developers can modify any of the previous properties.

## Improvement Proposals

Improvement proposals are the approach used by evmOS and Ethereum to modify the
behavior of opcodes. They are composed of a function, which has access
to the jump table to apply specific changes to operation behavior, and a name.

In the context of Ethereum, these protocol changes are
named Ethereum Improvement Proposals (EIPs) and are identified by a unique ID.
For example, [EIP-1559](https://eips.ethereum.org/EIPS/eip-1559) is
used to introduce the base fee.

To allow any evmOS partner to define their own specific
improvements without overlapping with evmOS and Ethereum ones, each
proposal is identified by a string, that is composed of the chain name and a number. For
example, default evmOS improvements are associated with the string `evmos_XXXX`.
This allows each chain to define their improvements without having to worry
about existing or future ID clashes between different chains.
Additionally, the ability to start enumeration at 0 is better for chain developers
and allows having a better overview of the historical progress for each chain.

Below, you will find an example of how the Evmos chain uses this functionality to modify the
behavior of the `CREATE` and `CREATE2` opcodes. First, the modifier function has
to be defined:

```go
// Enable0000 contains the logic to modify the CREATE and CREATE2 opcodes
// constant gas value.
func Enable0000(jt *vm.JumpTable) {
    multiplier := 10

	currentValCreate := jt[vm.CREATE].GetConstantGas()
	jt[vm.CREATE].SetConstantGas(currentValCreate * multiplier)

	currentValCreate2 := jt[vm.CREATE2].GetConstantGas()
	jt[vm.CREATE2].SetConstantGas(currentValCreate2 * multiplier)
}
```

Then, the function as to be associated with a name via a custom activator:

```go
evmosActivators = map[string]func(*vm.JumpTable){
    "evmos_0": eips.Enable0000,
}
```

## Activation of Improvement Proposals

Due to continuous changes in the users' interaction with the protocol, and to
introduce a safety measure along with the freedom to customize the virtual
machine behavior, custom improvement proposals are not active by default.
The activation of selected improvement proposals is controlled by the [EVM module's parameters](https://github.com/evmos/evmos/blob/main/proto/ethermint/evm/v1/evm.proto#L17-L18).
There are two ways of introducing the required parameter changes:

1. **Upgrade**: create a protocol upgrade handler which introduces the proposal name
in the active list.

2. **Governance**: create governance proposal to add an improvement proposal to the EVM module parameters.

This approach gives developers the ability to react to security issues or market conditions,
while keeping the chain's participants in the loop.

## Additional Resources

1. [Evmos Custom EIPs](https://github.com/evmos/evmos/blob/main/app/eips/README.md):
please refer to this document for a detailed description of how opcodes and
custom improvement proposals have to be used in the evmOS framework.
