---
sidebar_position: 6
---

# Vesting

## Solidity Interface & ABI

`Vesting.sol` is an interface through which Solidity contracts can interact with Evmos vesting module.
This is convenient for developers as they don’t need to know the implementation details behind the `x/vesting`
module in Evmos. Instead,
they can interact with vesting accounts using the Ethereum interface they are familiar with.

:::tip
To learn more about the `x/vesting` module, check out the [module's docs](../../../protocol/modules/vesting).
:::

### Interface `Vesting.sol`

Find the [Solidity interface in the evmos/extensions repo](https://github.com/evmos/extensions/blob/main/precompiles/stateful/Vesting.sol).

### ABI

Find the [ABI in the evmos/extensions repo](https://github.com/evmos/extensions/blob/main/precompiles/abi/vesting.json).

## Transactions

The Vesting solidity interface includes the following transactions

- `createClawbackVestingAccount`

    `createClawbackVestingAccount` defines a method for the creation of a `ClawbackVestingAccount`.

    ```solidity
    function createClawbackVestingAccount(
        address funderAddress,
        address vestingAddress,
        bool enableGovClawback
    ) external returns (bool success);
    ```

- `fundVestingAccount`

    `fundVestingAccount` defines a method for funding a vesting account.

    ```solidity
    function fundVestingAccount(
        address funderAddress,
        address vestingAddress,
        uint64 startTime,
        Period[] calldata lockupPeriods,
        Period[] calldata vestingPeriods
    ) external returns (bool success);
    ```

- `clawback`

    `clawback` defines a method for clawing back coins from a vesting account.

    ```solidity
    function clawback(
        address funderAddress,
        address accountAddress,
        address destAddress
    ) external returns (Coin[] memory);
    ```

- `updateVestingFunder`

    `updateVestingFunder` defines a method for updating the funder of a vesting account.

    ```solidity
    function updateVestingFunder(
        address funderAddress,
        address newFunderAddress,
        address vestingAddress
    ) external returns (bool success);
    ```

- `convertVestingAccount`

    `convertVestingAccount` defines a method for converting a clawback vesting account to an eth account.

    ```solidity
    function convertVestingAccount(
        address vestingAddress
    ) external returns (bool success);
    ```

## Queries

- `balances`

    `balances` query the balances of a vesting account

    ```solidity
    function balances(
        address vestingAddress
    ) external view returns (Coin[] memory locked, Coin[] memory unvested, Coin[] memory vested);
    ```

## Events

Each of the transactions emits its corresponding event. These are:

- `CreateClawbackVestingAccount`

    Event that is emitted when a clawback vesting account is created.

    ```solidity
    event CreateClawbackVestingAccount(
        address indexed funderAddress,
        address indexed vestingAddress
    );
    ```

- `FundVestingAccount`

    Event that is emitted when a clawback vesting account is funded.

    ```solidity
    event FundVestingAccount(
        address indexed funderAddress,
        address indexed vestingAddress,
        uint64 startTime,
        Period[] lockupPeriods,
        Period[] vestingPeriods
    );
    ```

- `Clawback`

    Event that is emitted when a vesting account is clawed back.

    ```solidity
    event Clawback(
        address indexed funderAddress,
        address indexed accountAddress,
        address destAddress
    );
    ```

- `UpdateVestingFunder`

    Event that is emitted when a vesting account's funder is updated.

    ```solidity
    event UpdateVestingFunder(
        address indexed funderAddress,
        address indexed vestingAddress,
        address  newFunderAddress
    );
    ```

- `ConvertVestingAccount`

    Event that is emitted when a vesting account is converted to a clawback vesting account.

    ```solidity
    event ConvertVestingAccount(
        address indexed vestingAddress
    );
    ```
