---
sidebar_position: 4
---

# Distribution

## Solidity Interface & ABI

`Distribution.sol` is an interface through which Solidity contracts can interact with Cosmos SDK distribution.
This is convenient for developers as they don’t need to know the implementation details behind
the `x/distribution` module in the Cosmos SDK. Instead,
they can interact with staking functions using the Ethereum interface they are familiar with.

### Interface `Distribution.sol`

```solidity
/// @author Evmos Team
/// @title Distribution Precompile Contract
/// @dev The interface through which solidity contracts will interact with Distribution
/// @custom:address 0x0000000000000000000000000000000000000801
interface DistributionI is genericAuth.GenericAuthorizationI {
    /// TRANSACTIONS
    /// @dev Change the address, that can withdraw the rewards of a delegator.
    /// Note that this address cannot be a module account.
    /// @param delegatorAddress The address of the delegator
    /// @param withdrawerAddress The address that will be capable of withdrawing rewards for
    /// the given delegator address
    function setWithdrawAddress(
        address delegatorAddress,
        string memory withdrawerAddress
    ) external returns (bool success);

    /// @dev Withdraw the rewards of a delegator from a validator
    /// @param delegatorAddress The address of the delegator
    /// @param validatorAddress The address of the validator
    /// @return amount The amount of Coin withdrawn
    function withdrawDelegatorRewards(
        address delegatorAddress,
        string memory validatorAddress
    ) external returns (Coin[] calldata amount);

    /// @dev Withdraws the rewards commission of a validator.
    /// @param validatorAddress The address of the validator
    /// @return amount The amount of Coin withdrawn
    function withdrawValidatorCommission(
        string memory validatorAddress
    ) external returns (Coin[] calldata amount);

    /// QUERIES
    /// @dev Queries validator commission and self-delegation rewards for validator.
    /// @param validatorAddress The address of the validator
    /// @return distributionInfo The validator's distribution info
    function validatorDistributionInfo(
        string memory validatorAddress
    )
        external
        view
        returns (
            ValidatorDistributionInfo[] calldata distributionInfo
        );

    /// @dev Queries the outstanding rewards of a validator address.
    /// @param validatorAddress The address of the validator
    /// @return rewards The validator's outstanding rewards
    function validatorOutstandingRewards(
        string memory validatorAddress
    ) external view returns (DecCoin[] calldata rewards);

    /// @dev Queries the accumulated commission for a validator.
    /// @param validatorAddress The address of the validator
    /// @return commission The validator's commission
    function validatorCommission(
        string memory validatorAddress
    ) external view returns (DecCoin[] calldata commission);

    /// @dev Queries the slashing events for a validator in a given height interval
    /// defined by the starting and ending height.
    /// @param validatorAddress The address of the validator
    /// @param startingHeight The starting height
    /// @param endingHeight The ending height
    /// @return slashes The validator's slash events
    /// @return pageResponse The pagination response for the query
    function validatorSlashes(
        string memory validatorAddress,
        uint64 startingHeight,
        uint64 endingHeight
    )
        external
        view
        returns (
            ValidatorSlashEvent[] calldata slashes,
            PageResponse calldata pageResponse
        );

    /// @dev Queries the total rewards accrued by a delegation from a specific address to a given validator.
    /// @param delegatorAddress The address of the delegator
    /// @param validatorAddress The address of the validator
    /// @return rewards The total rewards accrued by a delegation.
    function delegationRewards(
        address delegatorAddress,
        string memory validatorAddress
    ) external view returns (DecCoin[] calldata rewards);

    /// @dev Queries the total rewards accrued by each validator, that a given
    /// address has delegated to.
    /// @param delegatorAddress The address of the delegator
    /// @return rewards The total rewards accrued by each validator for a delegator.
    /// @return total The total rewards accrued by a delegator.
    function delegationTotalRewards(
        address delegatorAddress
    )
        external
        view
        returns (
            DelegationDelegatorReward[] calldata rewards,
            DecCoin[] calldata total
        );

    /// @dev Queries all validators, that a given address has delegated to.
    /// @param delegatorAddress The address of the delegator
    /// @return validators The addresses of all validators, that were delegated to by the given address.
    function delegatorValidators(
        address delegatorAddress
    ) external view returns (string[] calldata validators);

    /// @dev Queries the address capable of withdrawing rewards for a given delegator.
    /// @param delegatorAddress The address of the delegator
    /// @return withdrawAddress The address capable of withdrawing rewards for the delegator.
    function delegatorWithdrawAddress(
        address delegatorAddress
    ) external view returns (string memory withdrawAddress);

    /// @dev SetWithdrawerAddress defines an Event emitted when a new withdrawer address is being set
    /// @param caller the caller of the transaction
    /// @param withdrawerAddress the newly set withdrawer address
    event SetWithdrawerAddress(
        address indexed caller,
        string withdrawerAddress
    );

    /// @dev WithdrawDelegatorRewards defines an Event emitted when rewards from a delegation are withdrawn
    /// @param delegatorAddress the address of the delegator
    /// @param validatorAddress the address of the validator
    /// @param amount the amount being withdrawn from the delegation
    event WithdrawDelegatorRewards(
        address indexed delegatorAddress,
        string indexed validatorAddress,
        uint256 amount
    );

    /// @dev WithdrawValidatorCommission defines an Event emitted when validator commissions are being withdrawn
    /// @param validatorAddress is the address of the validator
    /// @param commission is the total commission earned by the validator
    event WithdrawValidatorCommission(
        string indexed validatorAddress,
        uint256 commission
    );
}
```

### ABI

The minified version of the precompiled contract `abi.json`:

```json
[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"string[]","name":"methods","type":"string[]"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"caller","type":"address"},{"indexed":false,"internalType":"string","name":"withdrawerAddress","type":"string"}],"name":"SetWithdrawerAddress","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"delegatorAddress","type":"address"},{"indexed":true,"internalType":"string","name":"validatorAddress","type":"string"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"WithdrawDelegatorRewards","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"string","name":"validatorAddress","type":"string"},{"indexed":false,"internalType":"uint256","name":"commission","type":"uint256"}],"name":"WithdrawValidatorCommission","type":"event"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"string[]","name":"methods","type":"string[]"}],"name":"approve","outputs":[{"internalType":"bool","name":"approved","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"delegatorAddress","type":"address"},{"internalType":"string","name":"validatorAddress","type":"string"}],"name":"delegationRewards","outputs":[{"components":[{"internalType":"string","name":"denom","type":"string"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint8","name":"precision","type":"uint8"}],"internalType":"struct DecCoin[]","name":"rewards","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"delegatorAddress","type":"address"}],"name":"delegationTotalRewards","outputs":[{"components":[{"internalType":"string","name":"validatorAddress","type":"string"},{"components":[{"internalType":"string","name":"denom","type":"string"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint8","name":"precision","type":"uint8"}],"internalType":"struct DecCoin[]","name":"reward","type":"tuple[]"}],"internalType":"struct DelegationDelegatorReward[]","name":"rewards","type":"tuple[]"},{"components":[{"internalType":"string","name":"denom","type":"string"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint8","name":"precision","type":"uint8"}],"internalType":"struct DecCoin[]","name":"total","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"delegatorAddress","type":"address"}],"name":"delegatorValidators","outputs":[{"internalType":"string[]","name":"validators","type":"string[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"delegatorAddress","type":"address"}],"name":"delegatorWithdrawAddress","outputs":[{"internalType":"string","name":"withdrawAddress","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"delegatorAddress","type":"address"},{"internalType":"string","name":"withdrawerAddress","type":"string"}],"name":"setWithdrawAddress","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"validatorAddress","type":"string"}],"name":"validatorCommission","outputs":[{"components":[{"internalType":"string","name":"denom","type":"string"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint8","name":"precision","type":"uint8"}],"internalType":"struct DecCoin[]","name":"commission","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"validatorAddress","type":"string"}],"name":"validatorDistributionInfo","outputs":[{"components":[{"internalType":"string","name":"operatorAddress","type":"string"},{"components":[{"internalType":"string","name":"denom","type":"string"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint8","name":"precision","type":"uint8"}],"internalType":"struct DecCoin[]","name":"selfBondRewards","type":"tuple[]"},{"components":[{"internalType":"string","name":"denom","type":"string"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint8","name":"precision","type":"uint8"}],"internalType":"struct DecCoin[]","name":"commission","type":"tuple[]"}],"internalType":"struct ValidatorDistributionInfo[]","name":"distributionInfo","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"validatorAddress","type":"string"}],"name":"validatorOutstandingRewards","outputs":[{"components":[{"internalType":"string","name":"denom","type":"string"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint8","name":"precision","type":"uint8"}],"internalType":"struct DecCoin[]","name":"rewards","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"validatorAddress","type":"string"},{"internalType":"uint64","name":"startingHeight","type":"uint64"},{"internalType":"uint64","name":"endingHeight","type":"uint64"}],"name":"validatorSlashes","outputs":[{"components":[{"internalType":"uint64","name":"validatorPeriod","type":"uint64"},{"components":[{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint8","name":"precision","type":"uint8"}],"internalType":"struct Dec","name":"fraction","type":"tuple"}],"internalType":"struct ValidatorSlashEvent[]","name":"slashes","type":"tuple[]"},{"components":[{"internalType":"bytes","name":"nextKey","type":"bytes"},{"internalType":"uint64","name":"total","type":"uint64"}],"internalType":"struct PageResponse","name":"pageResponse","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"delegatorAddress","type":"address"},{"internalType":"string","name":"validatorAddress","type":"string"}],"name":"withdrawDelegatorRewards","outputs":[{"components":[{"internalType":"string","name":"denom","type":"string"},{"internalType":"uint256","name":"amount","type":"uint256"}],"internalType":"struct Coin[]","name":"amount","type":"tuple[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"validatorAddress","type":"string"}],"name":"withdrawValidatorCommission","outputs":[{"components":[{"internalType":"string","name":"denom","type":"string"},{"internalType":"uint256","name":"amount","type":"uint256"}],"internalType":"struct Coin[]","name":"amount","type":"tuple[]"}],"stateMutability":"nonpayable","type":"function"}]
```

## Transactions

- `setWithdrawAddress`

    ```solidity
    /// @dev Change the address, that can withdraw the rewards of a delegator.
    /// Note that this address cannot be a module account.
    /// @param delegatorAddress The address of the delegator
    /// @param withdrawerAddress The address that will be capable of withdrawing rewards for
    /// the given delegator address
    function setWithdrawAddress(
        address delegatorAddress,
        string memory withdrawerAddress
    ) external returns (bool success);
    ```

- `withdrawDelegatorRewards`

    ```solidity
    /// @dev Withdraw the rewards of a delegator from a validator
    /// @param delegatorAddress The address of the delegator
    /// @param validatorAddress The address of the validator
    /// @return amount The amount of Coin withdrawn
    function withdrawDelegatorRewards(
        address delegatorAddress,
        string memory validatorAddress
    )
    external
    returns (
        Coin[] calldata amount
    );
    ```

- `withdrawValidatorCommission`

    ```solidity
    /// @dev Withdraws the rewards commission of a validator.
    /// @param validatorAddress The address of the validator
    /// @return amount The amount of Coin withdrawn
    function withdrawValidatorCommission(
        string memory validatorAddress
    )
    external
    returns (
        Coin[] calldata amount
    );
    ```

## Queries

- `validatorDistribution`

    ```solidity
    /// @dev Queries validator commission and self-delegation rewards for validator.
    /// @param validatorAddress The address of the validator
    /// @return distributionInfo The validator's distribution info
    function validatorDistributionInfo(
        string memory validatorAddress
    )
    external
    view
    returns (
        ValidatorDistributionInfo[] calldata distributionInfo
    );
    ```

- `validatorOutstandingRewards`

    ```solidity
    /// @dev Queries the outstanding rewards of a validator address.
    /// @param validatorAddress The address of the validator
    /// @return rewards The validator's outstanding rewards
    function validatorOutstandingRewards(
        string memory validatorAddress
    )
    external
    view
    returns (
        DecCoin[] calldata rewards
    );
    ```

- `validatorCommission`

    ```solidity
    /// @dev Queries the accumulated commission for a validator.
    /// @param validatorAddress The address of the validator
    /// @return commission The validator's commission
    function validatorCommission(
        string memory validatorAddress
    )
    external
    view
    returns (
        DecCoin[] calldata commission
    );
    ```

- `validatorSlashes`

    ```solidity
    /// @dev Queries the slashing events for a validator in a given height interval
    /// defined by the starting and ending height.
    /// @param validatorAddress The address of the validator
    /// @param startingHeight The starting height
    /// @param endingHeight The ending height
    /// @return slashes The validator's slash events
    /// @return pageResponse The pagination response for the query
    function validatorSlashes(
        string memory validatorAddress,
        uint64 startingHeight,
        uint64 endingHeight
    )
    external
    view
    returns (
        ValidatorSlashEvent[] calldata slashes,
        PageResponse calldata pageResponse
    );
    ```

- `delegationRewards`

    ```solidity
    /// @dev Queries the total rewards accrued by a delegation from a specific address to a given validator.
    /// @param delegatorAddress The address of the delegator
    /// @param validatorAddress The address of the validator
    /// @return rewards The total rewards accrued by a delegation.
    function delegationRewards(
        address delegatorAddress,
        string memory validatorAddress
    )
    external
    view
    returns (
        DecCoin[] calldata rewards
    );
    ```

- `delegationTotalRewards`

    ```solidity
    /// @dev Queries the total rewards accrued by each validator, that a given
    /// address has delegated to.
    /// @param delegatorAddress The address of the delegator
    /// @return rewards The total rewards accrued by each validator for a delegator.
    /// @return total The total rewards accrued by a delegator.
    function delegationTotalRewards(
        address delegatorAddress
    )
    external
    view
    returns (
        DelegationDelegatorReward[] calldata rewards,
        DecCoin[] calldata total
    );
    ```

- `delegatorValidators`

    ```solidity
    /// @dev Queries all validators, that a given address has delegated to.
    /// @param delegatorAddress The address of the delegator
    /// @return validators The addresses of all validators, that were delegated to by the given address.
    function delegatorValidators(
        address delegatorAddress
    ) external view returns (string[] calldata validators);
    ```

- `delegatorWithdrawAddress`

    `delegatorWithdrawAddress` queries withdraw address of a delegator

    ```solidity
    /// @dev Queries the address capable of withdrawing rewards for a given delegator.
    /// @param delegatorAddress The address of the delegator
    /// @return withdrawAddress The address capable of withdrawing rewards for the delegator.
    function delegatorWithdrawAddress(
        address delegatorAddress
    ) external view returns (string memory withdrawAddress);
    ```

## Events

Each of the transactions emits its corresponding event. These are:

- `SetWithdrawerAddress`

    ```solidity
    /// @dev SetWithdrawerAddress defines an Event emitted when a new withdrawer address is being set
    /// @param caller the caller of the transaction
    /// @param withdrawerAddress the newly set withdrawer address
    event SetWithdrawerAddress(
        address indexed caller,
        string withdrawerAddress
    );
    ```

- `WithdrawDelegatorRewards`

    ```solidity
    /// @dev WithdrawDelegatorRewards defines an Event emitted when rewards from a delegation are withdrawn
    /// @param delegatorAddress the address of the delegator
    /// @param validatorAddress the address of the validator
    /// @param amount the amount being withdrawn from the delegation
    event WithdrawDelegatorRewards(
        address indexed delegatorAddress,
        string indexed validatorAddress,
        uint256 amount
    );
    ```

- `WithdrawValidatorCommission`

    ```solidity
    /// @dev WithdrawValidatorCommission defines an Event emitted when validator commissions are being withdrawn
    /// @param validatorAddress is the address of the validator
    /// @param commission is the total commission earned by the validator
    event WithdrawValidatorCommission(
        string indexed validatorAddress,
        uint256 commission
    );
    ```

## Interact with the Solidity Interface

Below are some examples of how to interact with this Solidity interface from your smart contracts.

Make sure to import the precompiled interface, e.g.:

```solidity
import "https://github.com/evmos/extensions/blob/main/precompiles/stateful/Distribution.sol";
```

### Grant approval for the desired messages

See below a function that grants approval to the smart contract to send all `x/distribution` module messages
on behalf of the sender account. You can tweak this function to approve only the desired messages.

```solidity
string[] private distributionMethods = [
    MSG_SET_WITHDRAWER_ADDRESS,
    MSG_WITHDRAW_DELEGATOR_REWARD,
    MSG_WITHDRAW_VALIDATOR_COMMISSION,
];

/// @dev Approves all distribution transactions.
/// @dev This creates a Cosmos Authorization Grant for the given methods.
/// @dev This emits an Approval event from the GenericAuthorization.sol.
function approveAllDistributionMethods() public {
    bool success = DISTRIBUTION_CONTRACT.approve(
        msg.sender,
        distributionMethods
    );
    require(success, "Failed to approve distribution methods");
}
```

### Set withdraw address

The `changeWithdrawAddress` function allows a user to set a new withdraw address in the Cosmos `x/distribution` module.
For this transaction to be successful, make sure the user had already approved the `MSG_SET_WITHDRAWER_ADDRESS` message.

```solidity
function changeWithdrawAddress(
    string memory _withdrawAddr
) public returns (bool) {
    return
        distribution.DISTRIBUTION_CONTRACT.setWithdrawAddress(
            msg.sender,
            _withdrawAddr
        );
}
```

### Withdraw staking rewards

The `withdrawStakingRewards` function allows a user to withdraw his/her rewards corresponding to a specified validator.
For this transaction to be successful, make sure the user had already approved the `MSG_WITHDRAW_DELEGATOR_REWARD` message.

```solidity
	function withdrawStakingRewards(
    string memory _valAddr
) public returns (types.Coin[] memory) {
    return
        distribution.DISTRIBUTION_CONTRACT.withdrawDelegatorRewards(
            msg.sender,
            _valAddr
        );
}
```

### Withdraw validator commission

If the user is running a validator, he/she could withdraw the corresponding commission using a smart contract.
The user could use a function similar to `withdrawCommission`.
For this transaction to be successful,
make sure the user had already approved the `MSG_WITHDRAW_VALIDATOR_COMMISSION` message.

```solidity
function withdrawCommission(
    string memory _valAddr
) public returns (types.Coin[] memory) {
    return
        distribution.DISTRIBUTION_CONTRACT.withdrawValidatorCommission(
            _valAddr
        );
}
```

### Queries

Similarly to transactions, smart contracts can use query methods. To use these methods,
there is no need for authorization, as these are read-only methods.
Examples of this are the `getDelegationRewards` and `getValidatorCommision`
functions that return the information for the specified validator address.

```solidity
getDelegationRewards(
    string memory _valAddr
) public view returns (types.DecCoin[] memory) {
    return
        distribution.DISTRIBUTION_CONTRACT.delegationRewards(
            msg.sender,
            _valAddr
        );
}

function getValidatorCommission(
    string memory _valAddr
) public view returns (types.DecCoin[] memory) {
    return distribution.DISTRIBUTION_CONTRACT.validatorCommission(_valAddr);
}
```
