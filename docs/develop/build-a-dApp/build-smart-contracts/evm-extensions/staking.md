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

```solidity
/// @author Evmos Team
/// @title Staking Precompiled Contract
/// @dev The interface through which solidity contracts will interact with staking.
/// We follow this same interface including four-byte function selectors, in the precompile that
/// wraps the pallet.
/// @custom:address 0x0000000000000000000000000000000000000800
interface StakingI is authorization.AuthorizationI {
    /// @dev Defines a method for performing a delegation of coins from a delegator to a validator.
    /// @param delegatorAddress The address of the delegator
    /// @param validatorAddress The address of the validator
    /// @param amount The amount of the Coin to be delegated to the validator
    function delegate(
        address delegatorAddress,
        string memory validatorAddress,
        uint256 amount
    ) external returns (int64 completionTime);

    /// @dev Defines a method for performing an undelegation from a delegate and a validator.
    /// @param delegatorAddress The address of the delegator
    /// @param validatorAddress The address of the validator
    /// @param amount The amount to be undelegated from the validator
    /// @return completionTime The time when the undelegation is completed
    function undelegate(
        address delegatorAddress,
        string memory validatorAddress,
        uint256 amount
    ) external returns (int64 completionTime);

    /// @dev Defines a method for performing a redelegation
    /// of coins from a delegator and source validator to a destination validator.
    /// @param delegatorAddress The address of the delegator
    /// @param validatorSrcAddress The validator from which the redelegation is initiated
    /// @param validatorDstAddress The validator to which the redelegation is destined
    /// @param amount The amount to be redelegated to the validator
    /// @return completionTime The time when the redelegation is completed
    function redelegate(
        address delegatorAddress,
        string memory validatorSrcAddress,
        string memory validatorDstAddress,
        uint256 amount
    ) external returns (int64 completionTime);

    /// @dev Allows delegators to cancel the unbondingDelegation entry
    /// and to delegate back to a previous validator.
    /// @param delegatorAddress The address of the delegator
    /// @param validatorAddress The address of the validator
    /// @param amount The amount of the Coin
    /// @param creationHeight The height at which the unbonding took place
    /// @return completionTime The time when the cancellation of the unbonding delegation is completed
    function cancelUnbondingDelegation(
        address delegatorAddress,
        string memory validatorAddress,
        uint256 amount,
        uint256 creationHeight
    ) external returns (int64 completionTime);

    /// @dev Queries the given amount of the bond denomination to a validator.
    /// @param delegatorAddress The address of the delegator.
    /// @param validatorAddress The address of the validator.
    /// @return shares The amount of shares, that the delegator has received.
    /// @return balance The amount in Coin, that the delegator has delegated to the given validator.
    function delegation(
        address delegatorAddress,
        string memory validatorAddress
    ) external view returns (uint256 shares, Coin calldata balance);

    /// @dev Returns the delegation shares and coins, that are currently
    /// unbonding for a given delegator and validator pair.
    /// @param delegatorAddress The address of the delegator.
    /// @param validatorAddress The address of the validator.
    /// @return entries The delegations that are currently unbonding.
    function unbondingDelegation(
        address delegatorAddress,
        string memory validatorAddress
    ) external view returns (UnbondingDelegationEntry[] calldata entries);

    /// @dev Queries validator info for a given validator address.
    /// @param validatorAddress The address of the validator.
    /// @return validators The validator info for the given validator address.
    function validator(
        string memory validatorAddress
    ) external view returns (Validator[] calldata validators);

    /// @dev Queries all validators that match the given status.
    /// @param status Enables to query for validators matching a given status.
    /// @param pageRequest Defines an optional pagination for the request.
    function validators(
        string memory status,
        PageRequest calldata pageRequest
    )
        external
        view
        returns (
            Validator[] calldata validators,
            PageResponse calldata pageResponse
        );

    /// @dev Queries all redelegations from a source to a destination validator for a given delegator.
    /// @param delegatorAddress The address of the delegator.
    /// @param srcValidatorAddress Defines the validator address to redelegate from.
    /// @param dstValidatorAddress Defines the validator address to redelegate to.
    /// @return entries The active redelegations for the given delegator, source and destination validator combination.
    function redelegation(
        address delegatorAddress,
        string memory srcValidatorAddress,
        string memory dstValidatorAddress
    ) external view returns (RedelegationEntry[] calldata entries);

    /// @dev Queries all redelegations from a source to to a destination validator
    /// for a given delegator in a specified pagination manner.
    /// @param delegatorAddress The address of the delegator.
    /// @param srcValidatorAddress Defines the validator address to redelegate from.
    /// @param dstValidatorAddress Defines the validator address to redelegate to.
    /// @param pageRequest Defines an optional pagination for the request.
    /// @return response Holds the redelegations for the given delegator, source and destination validator combination.
    function redelegations(
        address delegatorAddress,
        string memory srcValidatorAddress,
        string memory dstValidatorAddress,
        PageRequest calldata pageRequest
    ) external view returns (RedelegationResponse calldata response);

    /// @dev Delegate defines an Event emitted when a given amount of tokens are delegated from the
    /// delegator address to the validator address.
    /// @param delegatorAddress The address of the delegator
    /// @param validatorAddress The address of the validator
    /// @param amount The amount of Coin being delegated
    /// @param newShares The new delegation shares being held
    event Delegate(
        address indexed delegatorAddress,
        string indexed validatorAddress,
        uint256 amount,
        uint256 newShares
    );

    /// @dev Unbond defines an Event emitted when a given amount of tokens are unbonded from the
    /// validator address to the delegator address.
    /// @param delegatorAddress The address of the delegator
    /// @param validatorAddress The address of the validator
    /// @param amount The amount of Coin being unbonded
    /// @param completionTime The time at which the unbonding is completed
    event Unbond(
        address indexed delegatorAddress,
        string indexed validatorAddress,
        uint256 amount,
        uint256 completionTime
    );

    /// @dev Redelegate defines an Event emitted when a given amount of tokens are redelegated from
    /// the source validator address to the destination validator address.
    /// @param delegatorAddress The address of the delegator
    /// @param validatorSrcAddress The address of the validator from which the delegation is retracted
    /// @param validatorDstAddress The address of the validator to which the delegation is directed
    /// @param amount The amount of Coin being redelegated
    /// @param completionTime The time at which the redelegation is completed
    event Redelegate(
        address indexed delegatorAddress,
        string indexed validatorSrcAddress,
        string indexed validatorDstAddress,
        uint256 amount,
        uint256 completionTime
    );

    /// @dev CancelUnbondingDelegation defines an Event emitted when a given amount of tokens
    /// that are in the process of unbonding from the validator address are bonded again.
    /// @param delegatorAddress The address of the delegator
    /// @param validatorAddress The address of the validator
    /// @param amount The amount of Coin that was in the unbonding process which is to be cancelled
    /// @param creationHeight The block height at which the unbonding of a delegation was initiated
    event CancelUnbondingDelegation(
        address indexed delegatorAddress,
        string indexed validatorAddress,
        uint256 amount,
        uint256 creationHeight
    );
}
```

### ABI

The minified version of the precompiled contract `abi.json` :

```json
[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"string[]","name":"methods","type":"string[]"},{"indexed":false,"internalType":"uint256[]","name":"values","type":"uint256[]"}],"name":"AllowanceChange","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"string[]","name":"methods","type":"string[]"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"delegatorAddress","type":"address"},{"indexed":true,"internalType":"string","name":"validatorAddress","type":"string"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"creationHeight","type":"uint256"}],"name":"CancelUnbondingDelegation","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"delegatorAddress","type":"address"},{"indexed":true,"internalType":"string","name":"validatorAddress","type":"string"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newShares","type":"uint256"}],"name":"Delegate","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"delegatorAddress","type":"address"},{"indexed":true,"internalType":"string","name":"validatorSrcAddress","type":"string"},{"indexed":true,"internalType":"string","name":"validatorDstAddress","type":"string"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"completionTime","type":"uint256"}],"name":"Redelegate","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"delegatorAddress","type":"address"},{"indexed":true,"internalType":"string","name":"validatorAddress","type":"string"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"completionTime","type":"uint256"}],"name":"Unbond","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"string","name":"method","type":"string"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"remaining","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"string[]","name":"methods","type":"string[]"}],"name":"approve","outputs":[{"internalType":"bool","name":"approved","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"delegatorAddress","type":"address"},{"internalType":"string","name":"validatorAddress","type":"string"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"creationHeight","type":"uint256"}],"name":"cancelUnbondingDelegation","outputs":[{"internalType":"int64","name":"completionTime","type":"int64"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"string[]","name":"methods","type":"string[]"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"approved","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"delegatorAddress","type":"address"},{"internalType":"string","name":"validatorAddress","type":"string"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"delegate","outputs":[{"internalType":"int64","name":"completionTime","type":"int64"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"delegatorAddress","type":"address"},{"internalType":"string","name":"validatorAddress","type":"string"}],"name":"delegation","outputs":[{"internalType":"uint256","name":"shares","type":"uint256"},{"components":[{"internalType":"string","name":"denom","type":"string"},{"internalType":"uint256","name":"amount","type":"uint256"}],"internalType":"struct Coin","name":"balance","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"string[]","name":"methods","type":"string[]"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"approved","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"delegatorAddress","type":"address"},{"internalType":"string","name":"validatorSrcAddress","type":"string"},{"internalType":"string","name":"validatorDstAddress","type":"string"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"redelegate","outputs":[{"internalType":"int64","name":"completionTime","type":"int64"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"delegatorAddress","type":"address"},{"internalType":"string","name":"srcValidatorAddress","type":"string"},{"internalType":"string","name":"dstValidatorAddress","type":"string"}],"name":"redelegation","outputs":[{"components":[{"internalType":"int64","name":"creationHeight","type":"int64"},{"internalType":"int64","name":"completionTime","type":"int64"},{"internalType":"uint256","name":"initialBalance","type":"uint256"},{"internalType":"uint256","name":"sharesDst","type":"uint256"}],"internalType":"struct RedelegationEntry[]","name":"entries","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"delegatorAddress","type":"address"},{"internalType":"string","name":"srcValidatorAddress","type":"string"},{"internalType":"string","name":"dstValidatorAddress","type":"string"},{"components":[{"internalType":"bytes","name":"key","type":"bytes"},{"internalType":"uint64","name":"offset","type":"uint64"},{"internalType":"uint64","name":"limit","type":"uint64"},{"internalType":"bool","name":"countTotal","type":"bool"},{"internalType":"bool","name":"reverse","type":"bool"}],"internalType":"struct PageRequest","name":"pageRequest","type":"tuple"}],"name":"redelegations","outputs":[{"components":[{"components":[{"components":[{"internalType":"int64","name":"creationHeight","type":"int64"},{"internalType":"int64","name":"completionTime","type":"int64"},{"internalType":"uint256","name":"initialBalance","type":"uint256"},{"internalType":"uint256","name":"sharesDst","type":"uint256"}],"internalType":"struct RedelegationEntry[]","name":"entries","type":"tuple[]"}],"internalType":"struct Redelegation","name":"redelegation","type":"tuple"},{"components":[{"components":[{"internalType":"int64","name":"creationHeight","type":"int64"},{"internalType":"int64","name":"completionTime","type":"int64"},{"internalType":"uint256","name":"initialBalance","type":"uint256"},{"internalType":"uint256","name":"sharesDst","type":"uint256"}],"internalType":"struct RedelegationEntry","name":"redelegationEntry","type":"tuple"},{"internalType":"uint256","name":"balance","type":"uint256"}],"internalType":"struct RedelegationEntryResponse[]","name":"entries","type":"tuple[]"}],"internalType":"struct RedelegationResponse","name":"response","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"delegatorAddress","type":"address"},{"internalType":"string","name":"validatorAddress","type":"string"}],"name":"unbondingDelegation","outputs":[{"components":[{"internalType":"int64","name":"creationHeight","type":"int64"},{"internalType":"int64","name":"completionTime","type":"int64"},{"internalType":"uint256","name":"initialBalance","type":"uint256"},{"internalType":"uint256","name":"balance","type":"uint256"}],"internalType":"struct UnbondingDelegationEntry[]","name":"entries","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"delegatorAddress","type":"address"},{"internalType":"string","name":"validatorAddress","type":"string"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"undelegate","outputs":[{"internalType":"int64","name":"completionTime","type":"int64"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"validatorAddress","type":"string"}],"name":"validator","outputs":[{"components":[{"internalType":"string","name":"operatorAddress","type":"string"},{"internalType":"string","name":"consensusPubkey","type":"string"},{"internalType":"bool","name":"jailed","type":"bool"},{"internalType":"enum BondStatus","name":"status","type":"uint8"},{"internalType":"uint256","name":"tokens","type":"uint256"},{"internalType":"uint256","name":"delegatorShares","type":"uint256"},{"internalType":"string","name":"description","type":"string"},{"internalType":"int64","name":"unbondingHeight","type":"int64"},{"internalType":"int64","name":"unbondingTime","type":"int64"},{"internalType":"uint256","name":"commission","type":"uint256"},{"internalType":"uint256","name":"minSelfDelegation","type":"uint256"}],"internalType":"struct Validator[]","name":"validators","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"status","type":"string"},{"components":[{"internalType":"bytes","name":"key","type":"bytes"},{"internalType":"uint64","name":"offset","type":"uint64"},{"internalType":"uint64","name":"limit","type":"uint64"},{"internalType":"bool","name":"countTotal","type":"bool"},{"internalType":"bool","name":"reverse","type":"bool"}],"internalType":"struct PageRequest","name":"pageRequest","type":"tuple"}],"name":"validators","outputs":[{"components":[{"internalType":"string","name":"operatorAddress","type":"string"},{"internalType":"string","name":"consensusPubkey","type":"string"},{"internalType":"bool","name":"jailed","type":"bool"},{"internalType":"enum BondStatus","name":"status","type":"uint8"},{"internalType":"uint256","name":"tokens","type":"uint256"},{"internalType":"uint256","name":"delegatorShares","type":"uint256"},{"internalType":"string","name":"description","type":"string"},{"internalType":"int64","name":"unbondingHeight","type":"int64"},{"internalType":"int64","name":"unbondingTime","type":"int64"},{"internalType":"uint256","name":"commission","type":"uint256"},{"internalType":"uint256","name":"minSelfDelegation","type":"uint256"}],"internalType":"struct Validator[]","name":"validators","type":"tuple[]"},{"components":[{"internalType":"bytes","name":"nextKey","type":"bytes"},{"internalType":"uint64","name":"total","type":"uint64"}],"internalType":"struct PageResponse","name":"pageResponse","type":"tuple"}],"stateMutability":"view","type":"function"}]
```

## Transactions

The Staking solidity interface includes the following transactions

- `delegate`

    `delegate` defines a method for performing a delegation of coins from a delegator to a validator.

    ```solidity
    function delegate(
            address delegatorAddress,
            string memory validatorAddress,
            uint256 amount
        ) external returns (int64 completionTime);
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
        ) external returns (int64 completionTime);
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
            address delegatorAddress,
            string memory srcValidatorAddress,
            string memory dstValidatorAddress,
            PageRequest calldata pageRequest
        ) external view returns (RedelegationResponse calldata response);
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
) public returns (int64 completionTime) {
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
