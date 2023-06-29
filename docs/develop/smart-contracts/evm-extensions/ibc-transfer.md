---
sidebar_position: 5
---

# IBC Transfer

## Solidity Interface & ABI

`IBCTransfer.sol` is an interface through which Solidity contracts can interact with the IBC protocol on Evmos chain.
This is convenient for developers as they don’t need to know the implementation details behind
the `transfer` module in [IBC-go](https://ibc.cosmos.network/). Instead,
they can perform IBC transfers using the Ethereum interface they are familiar with.

### Interface `IBCTransfer.sol`

Find the [Solidity interface in the evmos/extensions repo](https://github.com/evmos/extensions/blob/main/precompiles/stateful/IBCTransfer.sol).

### ABI

Find the [ABI in the evmos/extensions repo](https://github.com/evmos/extensions/blob/main/precompiles/abi/ibctransfer.json).

## Transactions

- `approve`

    ```solidity
    /// @dev Approves IBC transfer with a specific amount of tokens.
    /// @param spender spender The address which will spend the funds.
    /// @param allocations The allocations for the authorization.
    function approve(
        address spender,
        Allocation[] calldata allocations
    ) external returns (bool approved);
    ```

- `revoke`

    ```solidity
    /// @dev Revokes IBC transfer authorization for a specific spender
    /// @param spender The address which will spend the funds.
    function revoke(address spender) external returns (bool revoked);
    ```

- `increaseAllowance`
  
    ```solidity
    /// @dev Increase the allowance of a given spender by a specific amount of tokens and IBC connection for IBC transfer methods.
    /// @param spender The address which will spend the funds.
    /// @param sourcePort The source port of the IBC transaction.
    /// @param sourceChannel The source channel of the IBC transaction.
    /// @param denom The denomination of the tokens transferred.
    /// @param amount The amount of tokens to be spent.
    function increaseAllowance(
        address spender,
        string calldata sourcePort,
        string calldata sourceChannel,
        string calldata denom,
        uint256 amount
    ) external returns (bool approved);
    ```

- `decreaseAllowance`
  
    ```solidity
    /// @dev Decreases the allowance of a given spender by a specific amount of tokens for for IBC transfer methods.
    /// @param spender The address which will spend the funds.
    /// @param sourcePort The source port of the IBC transaction.
    /// @param sourceChannel The source channel of the IBC transaction.
    /// @param denom The denomination of the tokens transferred.
    /// @param amount The amount of tokens to be spent.
    function decreaseAllowance(
        address spender,
        string calldata sourcePort,
        string calldata sourceChannel,
        string calldata denom,
        uint256 amount
    ) external returns (bool approved);
    ```

- `transfer`
  
    ```solidity
    /// @dev Transfer defines a method for performing an IBC transfer.
    /// @param sourcePort the address of the validator
    /// @param sourceChannel the address of the validator
    /// @param denom the denomination of the Coin to be transferred to the receiver
    /// @param amount the amount of the Coin to be transferred to the receiver
    /// @param sender the hex address of the sender
    /// @param receiver the bech32 address of the receiver
    /// @param timeoutHeight the bech32 address of the receiver
    /// @param timeoutTimestamp the bech32 address of the receiver
    /// @param memo the bech32 address of the receiver
    function transfer(
        string memory sourcePort,
        string memory sourceChannel,
        string memory denom,
        uint256 amount,
        address sender,
        string memory receiver,
        Height memory timeoutHeight,
        uint64 timeoutTimestamp,
        string memory memo
    ) external returns (uint64 nextSequence);
    ```

## Queries

- `denomTrace`
  
    ```solidity
    /// @dev DenomTrace defines a method for returning a denom trace.
    function denomTrace(
        string memory hash
    ) external returns (DenomTrace[] memory denomTrace);
    ```

- `denomTraces`
  
    ```solidity
    /// @dev DenomTraces defines a method for returning all denom traces.
    function denomTraces(
        PageRequest memory pageRequest
    )
        external
        returns (
            DenomTrace[] memory denomTraces,
            PageResponse memory pageResponse
        );
    ```

- `denomHash`
  
    ```solidity
    /// @dev DenomHash defines a method for returning a hash of the denomination trace info.
    function denomHash(
        string memory trace
    ) external returns (string memory hash);
    ```

- `allowance`
  
    ```solidity
    /// @dev Returns the remaining number of tokens that spender will be allowed to spend on behalf of owner through
    /// IBC transfers. This is zero by default.
    /// @param owner The address of the account owning tokens.
    /// @param spender The address of the account able to transfer the tokens.
    function allowance(
        address owner,
        address spender
    ) external view returns (uint256 remaining);
    ```

## Events

Each of the transactions emits its corresponding event. These are:

- `IBCTransfer`

    ```solidity
    /// @dev Emitted when an ICS-20 transfer is executed.
    /// @param sender The address of the sender.
    /// @param receiver The address of the receiver.
    /// @param sourcePort The source port of the IBC transaction.
    /// @param sourceChannel The source channel of the IBC transaction.
    /// @param denom The denomination of the tokens transferred.
    /// @param amount The amount of tokens transferred.
    /// @param memo The IBC transaction memo.
    event IBCTransfer(
        address indexed sender,
        string indexed receiver,
        string sourcePort,
        string sourceChannel,
        string denom,
        uint256 amount,
        string memo
    );
    ```

- `IBCTransferAuthorization`

    ```solidity
    /// @dev Emitted when an ICS-20 transfer authorization is granted.
    /// @param grantee The address of the grantee.
    /// @param granter The address of the granter.
    /// @param sourcePort The source port of the IBC transaction.
    /// @param sourceChannel The source channel of the IBC transaction.
    /// @param spendLimit The coins approved in the allocation
    event IBCTransferAuthorization(
        address indexed grantee,
        address indexed granter,
        string sourcePort,
        string sourceChannel,
        Coin[] spendLimit
    );
    ```

- `RevokeIBCTransferAuthorization`

    ```solidity
    /// @dev This event is emitted when an owner revokes a spender's allowance.
    /// @param owner The owner of the tokens.
    /// @param spender The address which will spend the funds.
    event RevokeIBCTransferAuthorization(
        address indexed owner,
        address indexed spender
    );
    ```

- `AllowanceChange`

    ```solidity
    /// @dev This event is emitted when the allowance of a spender is changed by a call to the decrease or increase
    /// allowance method. The values field specifies the new allowances and the methods field holds the
    /// information for which methods the approval was set.
    /// @param owner The owner of the tokens.
    /// @param spender The address which will spend the funds.
    /// @param methods The message type URLs of the methods for which the approval is set.
    /// @param values The amounts of tokens approved to be spent.
    event AllowanceChange(
        address indexed owner,
        address indexed spender,
        string[] methods,
        uint256[] values
    );
    ```
