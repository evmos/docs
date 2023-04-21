---
sidebar_position: 1
---

# Authorization

The user should grant authorization to allow smart contracts (including precompiled ones)
to send messages on behalf of a user account.
This is achieved by the `Authorization.sol` and `GenericAuthorization.sol`
that provide the necessary functions to grant approvals and allowances.
The precompiled contracts use these interfaces, `AuthorizationI` and `GenericAuthorizationI`,
to allow users to approve the corresponding messages and amounts if needed.

## Solidity Interfaces

### `Authorization.sol`

Find the [Solidity interface in the evmos/extensions repo](https://github.com/evmos/extensions/blob/main/precompiles/common/Authorization.sol).

### `GenericAuthorization.sol`

Find the [Solidity interface in the evmos/extensions repo](https://github.com/evmos/extensions/blob/main/precompiles/common/GenericAuthorization.sol).

## Transactions

### `Authorization.sol`

- `approve`

    Approves a list of Cosmos or IBC transactions with a specific amount of tokens

    ```solidity
    function approve(
            address spender,
            uint256 amount,
            string[] calldata methods
        ) external returns (bool approved);
    ```

- `increaseAllowance`

    Increase the allowance of a given spender by a specific amount of tokens for IBC transfer methods or staking

    ```solidity
    function increaseAllowance(
            address spender,
            uint256 amount,
            string[] calldata methods
        ) external returns (bool approved);
    ```

- `decreaseAllowance`

    Decreases the allowance of a given spender by a specific amount of tokens for IBC transfer methods or staking

    ```solidity
    function decreaseAllowance(
            address spender,
            uint256 amount,
            string[] calldata methods
        ) external returns (bool approved);
    ```

### `GenericAuthorization.sol`

- `approve`

    Approves a list of Cosmos message

    ```solidity
    function approve(
            address spender,
            string[] calldata methods
        ) external returns (bool approved);
    ```

## Queries

### `Authorization.sol`

- `allowance`

    Returns the remaining number of tokens that the spender will be allowed to
    spend on behalf of the owner through IBC transfer methods or staking.
    This is zero by default

    ```solidity
    function allowance(
            address owner,
            address spender,
            string calldata method
    ) external view returns (uint256 remaining);
    ```

## Events

### `Authorization.sol`

- `Approval`

    This event is emitted when the allowance of a spender is set by a call to the `approve` method.
    The `value` field specifies the new allowance and the `methods`
    field holds the information for which methods the approval was set.

    ```solidity
    event Approval(
            address indexed owner,
            address indexed spender,
            string[] methods,
            uint256 value
        );
    ```

- `AllowanceChange`

    This event is emitted when the allowance of a spender is changed by a call to the decrease or increase allowance method.
    The `values` field specifies the new allowances and the `methods`
    field holds the information for which methods the approval was set.

    ```solidity
    event AllowanceChange(
            address indexed owner,
            address indexed spender,
            string[] methods,
            uint256[] values
        );
    ```

### `GenericAuthorization.sol`

- `Approval`

    This event is emitted when the allowance of a spender is set by a call to the `approve` method.
    The `methods` field holds the information for which methods the approval was set.

    ```solidity
    event Approval(
            address indexed owner,
            address indexed spender,
            string[] methods
        );
    ```
