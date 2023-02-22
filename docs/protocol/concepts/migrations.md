---
sidebar_position: 6
---

# State Export/Import

Evmos can dump the entire application state to a JSON file.
This, besides [upgrades](../../validate/upgrades),
can be useful for manual analysis of the state at a given height.

## Export State

Export state with:

```bash
evmosd export > new_genesis.json
```

You can also export state from a particular height
(at the end of processing the block of that height):

```bash
evmosd export --height [height] > new_genesis.json
```

If you plan to start a new network for 0 height (i.e genesis) from the exported state,
export with the `--for-zero-height` flag:

```bash
evmosd export --height [height] --for-zero-height > new_genesis.json
```

## Manually Migrate State

If you want to migrate state manually, e.g. for local testing purpose.
Note that for regular chain upgrades, a manual state migration is not required.

After exporting your state into a json file,
you can replace the old `genesis.json` with `new_genesis.json`.

```bash
cp -f genesis.json new_genesis.json
mv new_genesis.json genesis.json
```

At this point, you might want to run a script
to update the exported genesis into a genesis state
that is compatible with your new version.

You can use the `migrate` command to
migrate from a given version to the next one (eg: `v0.X.X` to `v1.X.X`):

```bash
evmosd migrate TARGET_VERSION GENESIS_FILE --chain-id=<new_chain_id> --genesis-time=<yyyy-mm-ddThh:mm:ssZ>
```
