# Build A Frontend

The importance of having a frontend for dapp development is significant because it allows users to interact with the
blockchain and smart contracts in a more user-friendly way. Here are some reasons why:

- The frontend of a dapp is built similarly to a traditional web application using HTML, CSS, and JavaScript, but
instead of interacting with a database via an API, the dapp interacts directly with the blockchain via a smart contract.
This enables users to access and use decentralized applications in a way that is familiar and easy to use.

- DApps need to be fully decentralized, and the frontend is typically hosted on peer-to-peer networks instead of
centralized hosting servers. This ensures that the dapp is not controlled by any single entity and is resistant to
censorship or shutdown.

- Blockchain application development requires front-end developers to have a good understanding of blockchain technology,
including the blockchain's nodes, smart contracts, and providers. Front-end developers need to be able to interact with
the smart contract by using its address and ABI. They also need to be able to read data from a smart contract with a
provider and write data to it with a signer. They need to choose the right network for the smart contract and ensure
that the wallet is on the same network.

 To develop dApps, it is essential to know how to interact with blockchain programmatically and understand the software
development aspect of it. Some applications build to leverage the Evmos Network involves
[Orbital Apes](https://www.orbitalapes.com), [SpaceFi](https://app.spacefi.io/#/home), and [more](https://evmos.org/ecosystem).

## Indexers

Indexers are programs that simplify querying and searching through blockchain data. They transform a large amount of
information into a database with convenient and fast search. Indexers are essential in building decentralized applications
(DApps) as they provide an efficient way to access blockchain data. Users can leverage our available [indexers](./../../develop/tools/indexers).

## Gas & Estimation

When developing and running dApps on Evmos, the wallet configuration will attempt to calculate the correct gas amount
for user's to sign. [Gas and Fees](./../../../protocol/concepts/gas-and-fees) breaks down these concepts in more detail.
We have a module called [feemarket](./../../../protocol/modules/feemarket#concepts) that describe our module implementation
of transaction prioritization since prior to Cosmos SDK 0.46 it did not have such implementation.

## Wallet Integration

Wallet integration is an essential aspect of dApp development that allows users to securely interact with blockchain-based
applications. Here are some key points from various sources on wallet integration in dApp development:

- The integration implementation checklist for dApp developers consists of three categories: frontend features,
transactions and wallet interactions, and more. Developers enabling transactions on their dApp have to determine
the wallet type of the user, create the transaction, request signatures from the corresponding wallet, and finally broadcast.

- Leverage Keplr, Metamask, Ledger, WalletConnect and more with Evmos. The latest wallets are located [here](./../../../use/wallet).

- Head over to our [Evmos Client Integrations](./../../develop/tools/client-integrations) to leverage our Typescript or Python libraries.
