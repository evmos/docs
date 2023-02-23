---
sidebar_position: 5
---

# IBC Relayers

Relayers read packets of data from one blockchain and communicate them
to another blockchain, acting as a sort of decentralized postal service that allows two sovereign blockchains to send
messages to each other. The process to enable this utilizes the Inter-Blockchain Communication (IBC) as a protocol.
It allows independent blockchains to communicate with each other
and exchange value, particularly tokens. IBC relayers are software programs that facilitate communication between two
distinct blockchain networks that support IBC.

![TAO-IBC](https://tutorials.cosmos.network/resized-images/600/academy/3-ibc/images/connectionstate.png)

Relayers can also open paths across chains, creating clients, connections, and channels. The
IBC protocol consists of two layers: the TAO layer and the APP layer, built on top of TAO. The TAO layer, which is
primarily responsible for the functionality of IBC, allows connected blockchains to send packets of information via
dedicated channels, using smart contract modules that include a light client for trustlessly verifying that the
state sent by the other blockchain is valid. The APP layer enables any application-layer protocol to be built to
operate on top of TAO. IBC has been enabled on [54 networks](https://mapofzones.com/)
over 60 million transactions currently executed using IBC per month. Relayers are critical to the functioning of
the IBC protocol. They can
handle large numbers of transactions at any given time, but congestion events can still occur. Relayer infrastructure
is being scaled up regularly, but in the meantime, users can support relayers by delegating their tokens to the
validators that also operate IBC relayers.

Most relayers also operate validator nodes on one or more Cosmos
ecosystem blockchains. The more support these relayers receive as validators, the more likely they will be
encouraged to continue operating at a loss on their relayer nodes. Additionally, the knowledge that relayers
are valued in such a way should encourage even more validators to set up relayer infrastructure of their own.
