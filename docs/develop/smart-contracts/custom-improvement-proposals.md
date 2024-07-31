# Custom Improvement Proposals

With the release [v19.0.0](https://github.com/evmos/evmos/releases/tag/v19.0.0)
a new feature called custom improvement proposal has been introduced in the
evmOS framework. Custom improvement proposals allow protocol developers to
modify the behavior of the EVM opcodes to tailor their functionalities to the
specific needs.

Improvement proposals are a way to introduce new standards, aimed to improve
protocol functionalities. Changes proposed in this way can affect any aspect
of protocol functionalities but are mainly used to customize the behavior of
smart contract execution.

## Operations

Operations are the base components of the Ethereum Virtual Machine (EVM) which
allows the execution of the smart contract logic. When a developer build a smart
contract, the code written in Solidity, or Viper, is not directly interpretable
by the EVM. Before being able to execute the code in the blockchain, the
contract has to be compiled via one of the available compilers, like `solc`. The
step of the compilation convert the contract, written in a human readable
language, into a sequence of operations that the virtual machine can interpret
and execute to perform state transition or query the latest committed state.
These operations are called, in the EVM context, **opcodes** and are contained
in a structure called **jump table**.

Some example of operations are the addition, defined by the opcode `ADD`, and
the subtraction, defined by the opcode `SUB`.

Each opcode is defined by specifying the logic that has to be executed when it
is called inside the EVM, its relationship with the memory, and the gas cost
associated with it. More specifically, an opcodes is completely defined by:

- `SetExecute`: update the execution logic for the opcode.

- `SetConstantGas`: update the value used for the constant gas cost.

- `SetDynamicGas`: update the function used to compute the dynamic gas cost.

- `SetMinStack`: update the minimum number of items in the stack required to
execute the `operation`.

- `SetMaxStack`: update the maximum number of items that will be in the stack
after executing the `operation`.

- `SetMemorySize`: the memory size required by the `operation`.

Within evmOS framework, developer can modify any of the previous properties.

## Improvement Proposals

Improvement proposal are the approach used by evmOS and Ethereum to modify the
the behavior of opcodes. They are composed by a function, which have the access
to the jump table to apply specific changes to operations behavior, and a name.

In the context of Ethereum, these protocol changes are
named Ethereum Improvement Proposals (EIPs) and are associated to a numerical
name. For example, the [EIP-1559](https://eips.ethereum.org/EIPS/eip-1559) is
used to introduce the base fee.

To allow any evmOS user to define their specific
improvements without overlapping with evmOS and Ethereum default ones, each
proposal is identified by a string composed by the chain name and a number. For
example, default evmOS improvements are associated with the string `evmos_XXXX`.
In this way, every chain can define their improvement without the risk of
overwriting already present functions and is free to start the numeration from
0.

Below an example of how Evmos chain uses this functionalities to modify the
behavior of the `CREATE` and `CREATE2` opcodes. First the modifier function has
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

then, the function as to be associated with a name via a custom activator:

```go
evmosActivators = map[int]func(*vm.JumpTable){
    "evmos_0": eips.Enable0000,
}
```

## Activation of Improvement Proposals

Due to continuous changes in the interaction of users with the protocol, and to
introduce a safety measure along with the freedom to customize the virtual
machine behavior, custom improvement proposals are not active by default. The
two just defined structures are used to define a modifier, and associate it with
a namespace. The activation of selected improvement proposals is made via
`x/evm` parameters. It is possible to activate specific improvement proposals in
two ways:

1. Upgrade: create a protocol upgrade handler that introduce the proposal name
in the active list.

2. Governance: create governance proposal to activate a improvement that is
registered in the custom activator.

With this approach, it is given to developers the possibility to quickly react
to security issues or market conditions, still keeping chain's participants in
the loop.

## Additional Resources

1. [Evmos Custom EIPs](https://github.com/evmos/evmos/blob/main/app/eips/README.md):
please refer to this document for a detailed description of how opcodes and
custom improvement proposals has to be used in the evmOS framework.
