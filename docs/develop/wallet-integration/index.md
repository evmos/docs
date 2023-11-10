# Wallet Integration

Wallet integration is an essential aspect of dApp development that allows users to securely interact with blockchain-based
applications. Here are some key points from various sources on wallet integration in dApp development:

- The integration implementation checklist for dApp developers consists of three categories: frontend features,
transactions and wallet interactions, and more. Developers enabling transactions on their dApp have to determine
the wallet type of the user, create the transaction, request signatures from the corresponding wallet, and finally broadcast.

- Leverage Keplr, Metamask, Ledger, WalletConnect and more with Evmos. The latest wallets are located [here](https://academy.evmos.org/articles/wallet).

- Head over to our [Evmos Client Integrations](./../../develop/tools/client-integrations)
  to leverage our Typescript or Python libraries.

## Gas & Estimation

When developing and running dApps on Evmos, the wallet configuration will attempt to calculate the correct gas amount
for user's to sign. [Gas and Fees](./../../../protocol/concepts/gas-and-fees) breaks down these concepts in more detail.
We have a module called [feemarket](./../../../protocol/modules/feemarket#concepts) that describes our module implementation
of transaction prioritization since prior to Cosmos SDK 0.46 it did not have such implementation.
