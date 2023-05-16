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
- [`ibc/transfer` module EVM extension](./ibc-transfer.md)

:::tip
**Note**: Find the EVM Extensions Solidity interfaces and examples in the [Evmos Extensions repo](https://github.com/evmos/extensions).
:::

## More learning resources

- [EVM Extensions - Staking & Distribution](https://academy.evmos.org/articles/advanced/evm-extensions-stk-distr)
  academy article
- [Diving into EVM Extensions Workshop (DoraHacks Hackathon)](https://www.youtube.com/live/pJhOfZ0ScAE?feature=share)
