---
sidebar_position: 3
---

# Staking

## Solidity Interface & ABI

`Staking.sol` is an interface through which Solidity contracts can interact with Cosmos SDK staking.
This is convenient for developers as they don’t need to know the implementation details behind the `x/staking`
module in the Cosmos SDK. Instead,
they can interact with staking functions using the Ethereum interface they are familiar with.

### Interface `Staking.sol`

Find the [Solidity interface in the evmos/extensions repo](https://github.com/evmos/extensions/blob/main/precompiles/stateful/Staking.sol).

### ABI

Find the [ABI in the evmos/extensions repo](https://github.com/evmos/extensions/blob/main/precompiles/abi/staking.json).

## Transactions

The Staking solidity interface includes the following transactions

- `delegate`

    `delegate` defines a method for performing a delegation of coins from a delegator to a validator.

    ```solidity
    function delegate(
        address delegatorAddress,
        string memory validatorAddress,
        uint256 amount
    ) external returns (bool success);
    ```

- `undelegate`

    `undelegate` defines a method for performing an undelegation from a delegate and a validator.

    ```solidity
    function undelegate(
        address delegatorAddress,
        string memory validatorAddress,
        uint256 amount
    ) external returns (int64 completionTime);
    ```

- `redelegate`

    Redelegate defines a method for performing a redelegation
    of coins from a delegator and source validator to a destination validator

    ```solidity
    function redelegate(
        address delegatorAddress,
        string memory validatorSrcAddress,
        string memory validatorDstAddress,
        uint256 amount
    ) external returns (int64 completionTime);
    ```

- `cancelUnbondingDelegation`

    `cancelUnbondingDelegation` allows delegators to cancel the unbondingDelegation entry
    and to delegate back to a previous validator.

    ```solidity
    function cancelUnbondingDelegation(
        address delegatorAddress,
        string memory validatorAddress,
        uint256 amount,
        uint256 creationHeight
    ) external returns (bool success);
    ```

## Queries

- `delegation`

    get the given amount of the bond denomination to a validator.

    ```solidity
    function delegation(
            address delegatorAddress,
            string memory validatorAddress
        ) external view returns (uint256 shares, Coin calldata balance);
    ```

- `unbondingDelegation`

    `unbondingDelegation` returns the unbonding delegation

    ```solidity
    function unbondingDelegation(
            address delegatorAddress,
            string memory validatorAddress
        ) external view returns (UnbondingDelegationEntry[] calldata entries);
    ```

- `validator`

    `validator` queries validator info for given validator address

    ```solidity
    function validator(
            string memory validatorAddress
        )
        external view returns (
            Validator[] calldata validators
        );
    ```

- `validators`

    `validators` queries all validators that match the given status

    ```solidity
    function validators(
            string memory status,
            PageRequest calldata pageRequest
        ) external view returns (
            Validator[] calldata validators,
            PageResponse calldata pageResponse
        );
    ```

- `redelegation`

    `redelegation` queries all redelegations from a source to a destination validator for a given delegator

    ```solidity
    function redelegation(
            address delegatorAddress,
            string memory srcValidatorAddress,
            string memory dstValidatorAddress
        ) external view returns (RedelegationEntry[] calldata entries);
    ```

- `redelegations`

    `redelegations` queries redelegations of given address for a given delegator in a specified pagination manner

    ```solidity
    function redelegations(
        string memory delegatorAddress,
        string memory srcValidatorAddress,
        string memory dstValidatorAddress,
        PageRequest calldata pageRequest
    )
        external
        view
        returns (
            RedelegationResponse[] calldata response,
            PageResponse calldata pageResponse
        );
    ```

## Events

Each of the transactions emits its corresponding event. These are:

- `Delegate`

    Delegate defines an Event emitted when a given amount
    of tokens are delegated from the delegator address to the validator address

    ```solidity
    event Delegate(
            address indexed delegatorAddress,
            string indexed validatorAddress,
            uint256 amount,
            uint256 newShares
        );
    ```

- `Unbond`

    Unbond defines an Event emitted when a given amount
    of tokens are unbonded from the validator address to the delegator address

    ```solidity
    event Unbond(
            address indexed delegatorAddress,
            string indexed validatorAddress,
            uint256 amount,
            uint256 completionTime
        );
    ```

- `Redelegate`

    Redelegate defines an Event emitted when a given amount
    of tokens are redelegated from the source validator address to the destination validator address

    ```solidity
    event Redelegate(
            address indexed delegatorAddress,
            string indexed validatorSrcAddress,
            string indexed validatorDstAddress,
            uint256 amount,
            uint256 completionTime
        );
    ```

- `CancelUnbondingDelegation`

    CancelUnbondingDelegation defines an Event emitted when
    a given amount of tokens that are in the process of unbonding
    from the validator address are bonded again

    ```solidity
    event CancelUnbondingDelegation(
            address indexed delegatorAddress,
            string indexed validatorAddress,
            uint256 amount,
            uint256 creationHeight
        );
    ```

## Interact with the Solidity Interface

Below are some examples of how to interact with this Solidity interface from your smart contracts.

Make sure to import the precompiled interface, e.g.:

```solidity
import "https://github.com/evmos/extensions/blob/main/precompiles/stateful/Staking.sol";
```

### Grant approval for the desired messages

See below a function that grants approval to the smart contract to send all `x/staking` module messages
on behalf of the sender account. In this case,
the allowance amount is the maximum amount possible.
You can tweak this function to approve only the desired messages and amounts.

```solidity
string[] private stakingMethods = [
    MSG_DELEGATE,
    MSG_UNDELEGATE,
    MSG_REDELEGATE,
    MSG_CANCEL_UNDELEGATION
];

/// @dev Approves all staking transactions with the maximum amount of tokens.
/// @dev This creates a Cosmos Authorization Grant for the given methods.
/// @dev This emits an Approval event.
function approveAllStakingMethodsWithMaxAmount() public {
    bool success = STAKING_CONTRACT.approve(
        msg.sender,
        type(uint256).max,
        stakingMethods
    );
    require(success, "Failed to approve staking methods");
}
```

### Delegate to a validator

The `stakeTokens` function allows the transaction sender to delegate the specified amount to his/her favorite validator.
Keep in mind that, for this transaction to be successful, the user should have approved the `MSG_DELEGATE` previously
(see the `approveAllStakingMethodsWithMaxAmount` defined in the code snippet above as an example).
This function returns the completion time of the staking transaction and emits a `Delegate` event.

```solidity
/// @dev stake a given amount of tokens. Returns the completion time of the staking transaction.
/// @dev This emits an Delegate event.
/// @param _validatorAddr The address of the validator.
/// @param _amount The amount of tokens to stake in aevmos.
/// @return completionTime The completion time of the staking transaction.
function stakeTokens(
    string memory _validatorAddr,
    uint256 _amount
) public returns (int64 completionTime) {
    return STAKING_CONTRACT.delegate(msg.sender, _validatorAddr, _amount);
}
```

### Undelegate from a validator

The `unstakeTokens` function allows a user to unstake a given amount of tokens.
It returns the completion time of the unstaking transaction and emits an `Undelegate` event.

```solidity
/// @dev unstake a given amount of tokens. Returns the completion time of the unstaking transaction.
/// @dev This emits an Undelegate event.
/// @param _validatorAddr The address of the validator.
/// @param _amount The amount of tokens to unstake in aevmos.
/// @return completionTime The completion time of the unstaking transaction.
function unstakeTokens(
    string memory _validatorAddr,
    uint256 _amount
) public returns (int64 completionTime) {
    return STAKING_CONTRACT.undelegate(msg.sender, _validatorAddr, _amount);
}
```

### Redelegate to another validator

With the `redelegateTokens` function, a user can redelegate a given amount of tokens.
It returns the completion time of the redelegate transaction and emits a `Redelegate` event.

```solidity
/// @dev redelegate a given amount of tokens. Returns the completion time of the redelegate transaction.
/// @dev This emits a Redelegate event.
/// @param _validatorSrcAddr The address of the source validator.
/// @param _validatorDstAddr The address of the destination validator.
/// @param _amount The amount of tokens to redelegate in aevmos.
/// @return completionTime The completion time of the redelegate transaction.
function redelegateTokens(
    string memory _validatorSrcAddr,
    string memory _validatorDstAddr,
    uint256 _amount
) public returns (int64 completionTime) {
    return
        STAKING_CONTRACT.redelegate(
            msg.sender,
            _validatorSrcAddr,
            _validatorDstAddr,
            _amount
        );
}
```

### Cancel unbonding from a validator

With the `cancelUnbondingDelegation` function, a user can cancel an unbonding delegation.
This function returns the completion time of the unbonding delegation cancellation transaction
and emits a `CancelUnbondingDelegation` event.

```solidity
/// @dev cancel an unbonding delegation. Returns the completion time of the unbonding delegation cancellation transaction.
/// @dev This emits an CancelUnbondingDelegation event.
/// @param _validatorAddr The address of the validator.
/// @param _amount The amount of tokens to cancel the unbonding delegation in aevmos.
/// @param _creationHeight The creation height of the unbonding delegation.
function cancelUnbondingDelegation(
    string memory _validatorAddr,
    uint256 _amount,
    uint256 _creationHeight
) public returns (bool success) {
    return
        STAKING_CONTRACT.cancelUnbondingDelegation(
            msg.sender,
            _validatorAddr,
            _amount,
            _creationHeight
        );
}
```

### Queries

Similarly to transactions, smart contracts can use query methods.
To use these methods, there is no need for authorization, as these are read-only methods.
Examples of this are these `getDelegation` and `getUnbondingDelegation`
functions that return the information for the specified validator address.

```solidity
/// @dev Returns the delegation information for a given validator for the msg sender.
/// @param _validatorAddr The address of the validator.
/// @return shares and balance. The delegation information for a given validator for the msg sender.
function getDelegation(
    string memory _validatorAddr
) public view returns (uint256 shares, Coin memory balance) {
    return STAKING_CONTRACT.delegation(msg.sender, _validatorAddr);
}

/// @dev Returns the unbonding delegation information for a given validator for the msg sender.
/// @param _validatorAddr The address of the validator.
/// @return entries The unbonding delegation entries for a given validator for the msg sender.
function getUnbondingDelegation(
    string memory _validatorAddr
) public view returns (UnbondingDelegationEntry[] memory entries) {
    return STAKING_CONTRACT.unbondingDelegation(msg.sender, _validatorAddr);
}
```
