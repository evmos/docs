---
sidebar_position: 8
---

# Mainnet

Before real users begin to transact with actual funds on your dApp, it is important to take into account certain factors
when launching it on Mainnet. Although moving your dApp from Testnet to Mainnet may be a straightforward process of
deploying your contracts to the Mainnet network, ensuring success and enhancing the exposure of your dApp may require
additional business development efforts. Here is an overview of some of the key factors to consider.

:::note
An Evmos validator, Stakely.io, runs a [faucet](https://stakely.io/en/faucet/evmos-evm) for builders to request dust.
:::

## Deployment

You can deploy your contracts on Mainnet using the [JSON-RPC](../develop/smart-contracts#deploy-with-ethereum-json-rpc).
This is the same procedure as on Testnet, but instead targeting the [Mainnet network endpoints](./../develop/api/networks).
Before you do so, have a look at the following considerations.

### Security

Thoroughly test your smart contracts on the Evmos Testnet to ensure it operates as intended. Comprehensive tests should
ensure all functions, error handling, and edge cases are covered.

Whenever possible, perform a comprehensive security audit of the smart contract code to identify and eliminate any
potential vulnerabilities or weaknesses. This is especially vital for the mainnet, as the code will be accessible to
everyone and any security flaws could result in substantial losses. Learn about the common vulnerabilities and contract
security practices. External auditors can also help optimize your contract's performance.

Ensure proper management of contract ownership and consider implementing a multi-sig mechanism for increased security.
This will allow you to maintain deployment ownership within your team instead of one specific owner that might leave the
team.

Last but not least, verify that any external libraries or dependencies used by the contract are up-to-date and secure.

### Contract upgradeability

Consider the possibility of upgrading the contract in the future and implement upgrade mechanisms if needed. This will
enable you to make changes to the contract without having to redeploy it, creating a new contract.

### Costs

Evaluate the gas costs associated with deploying and executing the smart contract, including the cost of deploying the
contract and executing its functions are sufficient or efficient for end users.

### Contract documentation

Provide clear and comprehensive documentation for the contract, including its purpose, functions, and potential risks.
This will assist users in understanding how to use the contract and make it easier for other developers to review and
contribute to the code.

## Token distribution

You're dApp might issue an ERC-20 token, e.g. to give token holders additional benefits. In this case, you will need to
decide on how to distribute them and what kind of narrative you want to create.

### Airdrop

One option is to distribute tokens to users through an airdrop. For some inspiration on how to select
eligible receivers of an airdrop have a look at the [Evmos Rektdrop](https://medium.com/evmos/the-evmos-rektdrop-abbe931ba823).

### Token Registration

Evmos allows for ERC-20 tokens to be used cross-chain. Once some of your tokens have been minted, you can register a token
pair through governance, which will allow users to send your tokens across chains. Head over to our Academy to learn how
to [register your ERC-20 token](https://academy.evmos.org/articles/advanced/erc20-registration).

## Community

Make yourself heard in the Evmos community and explain what value your dApp provides.
An essential part of building a dApp is getting in touch with the community to showcase how they can take ownership or
start contributing to your project. This will not only help your dApp's visibility but might result in a new community
of users, that want to improve your dApp.

Head over to the [Evmos Discord](https://discord.gg/evmos) channel get in touch with the community and contributors and
showcase your dApp on one of the next community calls. We also have a [Telegram group](https://t.me/EvmosBuilders) for
our builders.
