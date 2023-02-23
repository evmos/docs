# Testnet

The Evmos Testnet is a decentralized blockchain network
that runs parallel to the Mainnet.
It allows developers to test and deploy their decentralized applications (dApps)
in a safe and secure environment without the risk of losing real funds.
It is run by Validators using the same software as on the Evmos Mainnet,
which means it is built using the Ethereum Virtual Machine (EVM)
and supports the Ethereum toolchain.
This makes it compatible with a vast ecosystem
of existing Ethereum-based applications and tools.

Using the Evmos Testnet provides several benefits for dApp developers.
Firstly, it enables them to test and refine their smart contracts
and dApps in a sandbox environment without the risk of making costly mistakes.
Developers can experiment with different use cases and scenarios,
simulate various network conditions,
and stress test their applications to ensure they are scalable and resilient.
Secondly, the Evmos Testnet provides a community-driven
and collaborative platform for developers to share knowledge, best practices, and code.
This can help developers to speed up their development process
and tap into a wealth of resources and expertise.

Find out below how to connect to Testnet
and request testnet tokens from the Faucet to start developing.
Note, that tokens on Testnet don’t have actual value,
so that you don’t need to worry about loosing funds.

## Swagger Docs

We hosted our testnet API endpoints [here](./../develop/api#clients) and it uses Swagger.

## Faucet

import ProjectValue from '@site/src/components/ProjectValue';
import Highlighter from '@site/src/components/Highlighter';

The Evmos Testnet Faucet distributes small amounts of <ProjectValue keyword="testnet_denom" />
to anyone who can provide a valid testnet address for free. Request funds from the faucet either by using the
[Keplr Wallet](./../../use/connect-your-wallet/keplr) or follow the instructions on this page.

:::tip
Follow the [Metamask](./../../use/connect-your-wallet/metamask), [Keplr](./../../use/connect-your-wallet/keplr)
or [Keyring](./../../protocol/concepts/keyring) guides for more info on how to setup your wallet account.
:::

## Request Testnet tokens

Once you are signed in to the Keplr extension, visit the [Faucet](https://faucet.evmos.dev/) to request tokens
for the testnet. Click the `Request Funds with Keplr` button. Then approve the both following pop ups `Chain Add Request`
and `Request Connection` to add the <ProjectValue keyword='name' /> testnet chain
(evmos_<ProjectValue keyword="chain_id" />-<ProjectValue keyword="testnet_version_number" />) to Keplr and approve the
connection.

![chain add request](/img/keplr_approve_chain.png)

After approval, you can see a transaction confirmation informing you that <ProjectValue keyword="testnet_denom" /> have
been successfully transferred to your [Evmos address](./../../protocol/concepts/accounts#address-formats-for-clients) on
the testnet.

:::warning
**Note**: only Ethereum compatible addresses (i.e `eth_secp256k1` keys) are supported on Evmos.
:::

![chain add request](/img/keplr_transaction.png)

Alternatively you can also fill in your address on the input field in Bech32 (`evmos1...`) or Hex (`0x...`) format.

:::warning
If you use your Bech32 address, make sure you input the [account address](./../../protocol/concepts/accounts#addresses-and-public-keys)
(`evmos1...`) and **NOT** the validator operator address (`evmosvaloper1...`)
:::

![faucet site](/img/faucet_web_page.png)

View your account balance either by clicking on the Keplr extension or by using the [Testnet Explorer](https://testnet.mintscan.io/evmos-testnet).

:::tip
**Note**: Keplr might not display the amount of <ProjectValue keyword="testnet_denom" /> transferred by the faucet, as
it might be smaller than the number of decimals displayed in the Keplr extension.
:::

## Rate limits

:::tip
All addresses **MUST** be authenticated using ReCAPTCHA before requesting tokens.
:::

To prevent the faucet account from draining the available funds, the Evmos testnet faucet imposes a maximum number of
requests for a period of time. By default, the faucet service accepts 1 request per day per address. You can request
<ProjectValue keyword="testnet_denom" /> from the faucet for each address only once every 24h. If you try to request
multiple times within the 24h cooldown phase, no transaction will be initiated. Please try again in 24 hours.

## Amount

For each request, the faucet transfers 1 <ProjectValue keyword="testnet_denom" /> to the given address.

## Faucet Addresses

The public faucet addresses for the testnet are:

- **Bech32**: [`evmos1ht560g3pp729z86s2q6gy5ws6ugnut8r4uhyth`](https://testnet.mintscan.io/evmos-testnet/account/evmos1ht560g3pp729z86s2q6gy5ws6ugnut8r4uhyth)
- **Hex**: [`0xBaE9A7A2210F94511F5050348251d0d7113E2cE3`](https://evm.evmos.dev/address/0xBaE9A7A2210F94511F5050348251d0d7113E2cE3/transactions)
