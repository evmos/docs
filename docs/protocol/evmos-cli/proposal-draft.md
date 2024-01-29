---
sidebar_position: 7
---

# Drafting a proposal

The `draft-proposal` command in the Evmos CLI is part of the Cosmos-SDK
governance module and is used to generate a draft proposal JSON file.
This generated proposal JSON file contains a skeleton structure for a governance proposal.

## Command Syntax

```bash
evmosd tx gov draft-proposal [flags]
```

## Usage

To create a draft proposal using the `evmosd tx gov draft-proposal` command, follow these steps:

1. Run the command

   ```bash
   evmosd tx gov draft-proposal
   ```

2. The command will present a list of proposal types for selection.
   The available options typically include:

   ```bash
   Use the arrow keys to navigate: ↓ ↑ → ← 
    ? Select proposal type: 
        text
        community-pool-spend
        software-upgrade
        cancel-software-upgrade
      ▸ other
   ```

   In case you don't find the required proposal (e.g. update params),
   choose the `other` option. It will show an extensive list of the supported messages:

    ```bash
    ✔ other
    Use the arrow keys to navigate: ↓ ↑ → ← 
    ? Select proposal message type:: 
    ↑   /evmos.erc20.v1.MsgUpdateParams
      ▸ /evmos.inflation.v1.MsgUpdateParams
        /evmos.recovery.v1.MsgUpdateParams
    ↓   /evmos.revenue.v1.MsgCancelRevenue
    ```

3. Follow the on-screen instructions to complete the process.
   The command will generate a JSON file that you can use for your proposal.

4. Once the JSON file is generated,
   you can make any necessary changes to the proposal information within the file.

5. Finally, use the generated JSON file as input when submitting
   your proposal using the `evmosd tx gov submit-proposal` command.

    ```bash
    evmosd tx gov submit-proposal draft_proposal.json [flags]
    ```
