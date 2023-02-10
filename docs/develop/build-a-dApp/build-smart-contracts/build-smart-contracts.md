# EVM Smart Contracts

<!--
Add an image of a dApp with several smart contracts that use
- are built with solitidy
- oracles
- evm extensions
-->

Since the introduction of Ethereum in 2015, the ability to control digital assets through [smart contracts](https://www.fon.hum.uva.nl/rob/Courses/InformationInSpeech/CDROM/Literature/LOTwinterschool2006/szabo.best.vwh.net/idea.html) has attracted a large community of developers to build decentralized applications on the Ethereum Virtual Machine (EVM). This community is continuously creating extensive tooling and introducing standards, which are further increasing the adoption rate of EVM compatible technology.

Whether you are building new use cases on Evmos or porting an existing dApp from another EVM-based chain (e.g. Ethereum), you can easily build and deploy EVM smart contracts on Evmos to implement the core business logic of your dApp. Evmos is fully compatible with the EVM, so it allows you to use the same tools (Solidity, Remix, Oracles, etc.) and APIs (i.e. Ethereum JSON-RPC) that are available on the EVM.

Leveraging the interoperability of Cosmos chains, Evmos enables you to build scalable cross-chain applications within a familiar EVM environment. Learn about the essential components when building and deploying EVM smart contracts on Evmos below.

## Build with Solidity

You can develop EVM smart contracts on Evmos using [Solidity](https://github.com/ethereum/solidity). Solidity is also used to build smart contracts on Ethereum. So if you have deployed smart contracts on Ethereum (or any other EVM-compatible chain) you can use the same contracts on Evmos.

Since it is the most widely used smart contract programming language in Blockchain, Solidity comes with well-documented and rich language support. Head over to our list of Tools and IDE Plugins to help you get started.

### EVM Extensions

<!-- TODO: included in another open PR -->

### Oracles

Blockchain oracles provide a way for smart contracts to access external information, such as price feeds from financial exchanges or carbon emission measurements. They serve as bridges between blockchains and the outside world.

Head over to our Oracles section to find out how smart contracts can make use of oracles on Evmos for real-life activities such as insurance, borrowing, lending, or gaming.

<!-- TODO: Add when Oracle section is added to develop/tools -->

## Deploy with Ethereum JSON-RPC

Evmos is fully compatible with the Ethereum JSON-RPC APIs, allowing you to deploy and interact with smart contracts on Evmos and connect with existing Ethereum-compatible web3 tooling. This gives you direct access to reading Ethereum-formatted transactions or sending them to the network which otherwise wouldn't be possible on a Cosmos chain, such as Evmos.

You can connect to the Evmos Testnet to deploy and test your smart contracts before moving to Mainnet.

<!-- TODO: Add link to JSON-RPC and Testnet once those sections are ready -->

### Block Explorers

You can use block explorers to view and debug interactions with your smart contracts deployed on Evmos. Block explorers index blocks and their transactions so that you can search for real-time and historical information about the blockchain, including data related to blocks, transactions, addresses, and more.

<!-- TODO: Add link to Block explorer section is added to develop/tools -->

### Contract Verification

Once deployed, smart contract data is deployed as non-human readable EVM bytecode. You can use contract verification tools that publish and verify your original Solidity code to prove to users that they are interacting with the correct smart contract.
