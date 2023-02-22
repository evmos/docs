---
sidebar_position: 4
slug: '/create-backend'
---

# Create A Backend

When building a DApp, having a backend can provide several benefits, including:

- Resiliency: A DApp's backend is fully distributed and managed on a blockchain platform, so there is no downtime and
the application will continue to be available as long as the platform is still operating.
- Transparency: The on-chain nature of a DApp allows everyone to inspect the code and be more sure about its function.
Any interaction with the DApp will be stored forever in the blockchain.
- Censorship resistance: As long as a user has access to an Ethereum node, the user will always be able to interact with
a DApp without interference from any centralized control. No service provider, or even the owner of the smart contract,
can alter the code once it is deployed on the network.
- Enhanced security: Smart contracts used in DApps are highly secure and tamper-proof, and the decentralized nature of
the platform makes it difficult for hackers to breach the system.
- Decentralization: DApps operate on Ethereum, an open public decentralized platform where no one person or group has control.
- Determinism: DApps perform the same function irrespective of the environment in which they get executed.
- Turing completeness: DApps can perform any action given the required resources.
- Isolation: DApps are executed in a virtual environment known as Ethereum Virtual Machine so that if the smart contract
has a bug, it won’t hamper the normal functioning of the blockchain network.

However, it is important to note that not all DApps require a backend. For example, if the DApp is designed solely for
transactions, a backend may not be necessary. Additionally, the frontend of a DApp can use standard web technologies
and interact with the smart contract using a library like ethers.js. If a DApp does require a backend, it is important
to consider the following:

- Smart contract architecture design: It is important to identify which aspects of the application need a trusted and
decentralized execution platform, and to keep computations in the smart contract minimal to avoid high costs.
- Off-chain or metadata: Data that won't be stored in the smart contract, such as user data, may need to be stored in a
backend system aggregating analytics and allowing you to run reports and manage some aspects of the DApp.
- User authentication: If the DApp requires a username and password, a backend may be necessary to generate a wallet for
the user and allow them to fund their account.
- Data verification: If the DApp is a website running on a webserver and displaying content from the blockchain, there
may be an element of trust involved because the code is pre-compiled on the server and the client doesn't have access
to the code. A mobile or desktop app may be a better solution in this case, as the source code can be open source
and the client can build the app from that code, thus having full trust in the code being executed.

Ultimately, whether or not a DApp requires a backend depends on the specific requirements of the application.  A
competent app development team skilled in building DApps can help determine the technical intricacies and tradeoffs
involved in building a fully decentralized application.
