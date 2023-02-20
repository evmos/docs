# Mainnet

Moving your dApp from Testnet to Mainnet can be as simple as deploying your contracts to the Mainnet network. However, to guarantee success and improve the visibility of your dApp, you might want to consider additional business development efforts. Find below an overview of some considerations when launching your dApp on Mainnet, before you have real people use real money on it.

## Deployment

You can deploy your contracts on Mainnet using the [JSON-RPC](../build-a-dApp/build-smart-contracts/build-smart-contracts.md#deploy-with-ethereum-json-rpc). This is the same procedure as on Testnet, but instead targeting the [Mainnet network endpoints](../apis/networks.md). Before you do so, have a look at the following considerations.

### Security

Thoroughly test your smart contracts on the Evmos Testnet to ensure it operates as intended. Comprehensive tests should ensure all functions, error handling, and edge cases are covered.

Whenever possible, perform a comprehensive security audit of the smart contract code to identify and eliminate any potential vulnerabilities or weaknesses. This is especially vital for the mainnet, as the code will be accessible to everyone and any security flaws could result in substantial losses. Learn about the common vulnerabilities and contract security practices. External auditors can also help optimize your contract's performance.

Ensure proper management of contract ownership and consider implementing a multi-sig mechanism for increased security. This will allow you to maintain deployment ownership within your team instead of one specific owner that might leave the team.

Last but not least, verify that any external libraries or dependencies used by the contract are up-to-date and secure.

### Contract upgradeability

Consider the possibility of upgrading the contract in the future and implement upgrade mechanisms if needed. This will enable you to make changes to the contract without having to redeploy it, creating a new contract.

### Costs

Evaluate the gas costs associated with deploying and executing the smart contract, including the cost of deploying the contract and executing its functions are sufficient or efficient for end users.

### Contract documentation

Provide clear and comprehensive documentation for the contract, including its purpose, functions, and potential risks. This will assist users in understanding how to use the contract and make it easier for other developers to review and contribute to the code.

## Token distribution

You're dApp might issue an ERC-20 token, e.g. to give token holders additional benefits. In this case, you will need to decide on how to distribute them and what kind of narrative you want to create.

### Airdrop

One option is to distribute tokens to users through an airdrop. For some inspiration on how to select
eligible receivers of an airdrop have a look at the [Evmos Rektdrop](https://medium.com/evmos/the-evmos-rektdrop-abbe931ba823).

### Token Registration

Evmos allows for ERC20 tokens to be used cross-chain. Once some of your tokens have been minted, you can register a token pair through governance, which will allow users to send your tokens across chains. Head over to our academy to learn how to register your ERC20 token.

<!-- TODO add link to register  -->

## Revenue

On Evmos, you can generate revenue, every time a user interacts with your dApp, gaining you a steady income. Developers can register their smart contracts and every time someone interacts with a registered smart contract, the contract deployer or their assigned withdrawal account receives a part of the transaction fees.

To learn about how to register your smart contracts, head over to our academy.

<!-- TODO: when the revenue module is imported, the reference can be made here -->

## Community

Make yourself heard in the Evmos community and explain what value your dApp provides.
An essential part of building a dApp is getting in touch with the community to showcase how they can take ownership or start contributing to your project. This will not only help your dApp's visibility but might result in a new community of users, that want to improve your dApp.

Head over to the Evmos Discord channel get in touch with the community and contributors and showcase your dApp on one of the next community calls.
