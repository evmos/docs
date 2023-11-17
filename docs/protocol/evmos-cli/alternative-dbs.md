---
sidebar_position: 5
---
# Alternative databases

To use a different database than the default one (levelDB),
you may need to build the `evmosd` binary manually with specific flags and configurations.

Learn about the different options supported.

## Prerequisites

- Golang version `1.20+` ([installation guide](https://go.dev/doc/install))
- [Source code of the desired `evmosd`](https://github.com/evmos/evmos) version.
  For example, if want to use `v14.0.0`, execute the following command to download only the necessary code:
  
  ```bash
  git clone -b v14.0.0 --single-branch https://github.com/evmos/evmos
  ```

## Pebble DB

Currently, the supported database backends on the [cometbft-db](https://github.com/cometbft/cometbft-db) dependency
do not include pebbleDB.

### Install dependencies

If you wish to use this database, you need to replace this dependency by a fork that includes pebbleDB.
To do this and install the binary with this database, execute the following commands:

```bash
# cd into the directory where you have the Evmos protocol source code
cd evmos

# replace the cometbft-db dependency
go mod edit -replace github.com/cometbft/cometbft-db=github.com/notional-labs/cometbft-db@pebble
go mod tidy
```

### Install `evmosd` binary

```bash
# compile and install the binary
go install -ldflags "-w -s -X github.com/cosmos/cosmos-sdk/types.DBBackend=pebbledb \
 -X github.com/cosmos/cosmos-sdk/version.Version=$(git describe --tags)-pebbledb \
 -X github.com/cosmos/cosmos-sdk/version.Commit=$(git log -1 --format='%H')" -tags pebbledb ./...
```

Check the binary version has the `-pebbledb` suffix

```bash
❯ evmosd version
v14.0.0-pebbledb
```

### Update configuration

Make sure to update the `db_backend` configuration parameter in the `config.toml`:

```toml
db_backend = "pebbledb"
```

## Rocks DB

To setup a node with rocksDB, you need to install the [corresponding library](https://github.com/facebook/rocksdb)
and related dependencies.

The installation process described below applies to Ubuntu OS.
For other operating system, refer to the [rocksdb installation guide](https://github.com/facebook/rocksdb/blob/v7.9.2/INSTALL.md).

### Install dependencies

- `gflags`

  ```bash
  sudo apt-get install libgflags-dev
  ```

  If this doesn't work and you're using Ubuntu, [here's a nice tutorial](https://askubuntu.com/questions/312173/installing-gflags-12-04)
- `snappy`

  ```bash
  sudo apt-get install libsnappy-dev
  ```

- `zlib`

  ```bash
  sudo apt-get install zlib1g-dev
  ```

- `bzip2`

  ```bash
  sudo apt-get install libbz2-dev
  ```

- `lz4`

  ```bash
  sudo apt-get install liblz4-dev
  ```

- `zstandard`

  ```bash
  sudo apt-get install libzstd-dev
  ```

- `gcc` >= 7

  ```bash
  sudo apt-get install build-essential
  ```

- `clang` >= 5

  ```bash
  sudo apt-get install clang
  ```

Install all dependencies at once with this command:

```bash
sudo apt-get install libgflags-dev libsnappy-dev zlib1g-dev libbz2-dev liblz4-dev libzstd-dev build-essential clang
```

### Install `librocksdb`

To install this library, you will need to clone the
[rocksdb repository](https://github.com/facebook/rocksdb).

Clone only the required version of it.
To find out which is the required version,
check the tag of the `grocksdb` dependency in the `go.mod` file of the evmos repository.
For example, if the `go.mod` has:

```golang
github.com/linxGnu/grocksdb v1.8.4
```

You should check in the [grocksdb repo](https://github.com/linxGnu/grocksdb/releases),
which RocksDB version is supported in the `v1.8.4` tag.
In this case, `v1.8.4` supports RocksDB `v8.5.3`.

To install `librocksdb v8.5.3`, run the following commands:

```bash
# remove rocksdb repo from your machine if you have a previous version installed
rm -rf rocksdb

# download the source code of the desired version
git clone -b v8.5.3 --single-branch https://github.com/facebook/rocksdb

# cd into the directory where the source code was downloaded
cd rocksdb

# take note of the path where you have the rocksdb code
# you will need this for building the evmosd binary
PATH_TO_ROCKSDB=$(pwd)

# install librocksdb
PORTABLE=1 WITH_JNI=0 WITH_BENCHMARK_TOOLS=0 \
WITH_TESTS=1 WITH_TOOLS=0 WITH_CORE_TOOLS=1 \
WITH_BZ2=1 WITH_LZ4=1 WITH_SNAPPY=1 WITH_ZLIB=1 \
WITH_ZSTD=1 WITH_GFLAGS=0 USE_RTTI=1 \
make static_lib
```

The installation process may take several minutes.

### Install `evmosd` binary

Once this completes, install the `evmosd` binary with rocksDB support

```bash
# cd into the directory where the evmos source code is
cd evmos

# compile and install the binary
# IMPORTANT: make sure to have the PATH_TO_ROCKSDB with the path where you cloned the rocksdb repository
CGO_CFLAGS="-I"$PATH_TO_ROCKSDB"/include" \
CGO_LDFLAGS="-L"$PATH_TO_ROCKSDB" -lrocksdb -lstdc++ -lm -lz -lbz2 -lsnappy -llz4 -lzstd" \
COSMOS_BUILD_OPTIONS=rocksdb \
make install
```

If getting the errors related to dynamic loading of shared libraries:

```bash
.../rocksdb/env/env_posix.cc:108: undefined reference to `dlclose'
.../rocksdb/env/env_posix.cc:113: undefined reference to `dlsym'
...
```

Retry the command adding the dynamic linker library in your executable, the `-ldl` flag in the `CGO_LDFLAGS`:

```bash
CGO_ENABLED=1 \
CGO_CFLAGS="-I"$PATH_TO_ROCKSDB"/include" \
CGO_LDFLAGS="-L"$PATH_TO_ROCKSDB" -lrocksdb -lstdc++ -lm -lz -lbz2 -lsnappy -llz4 -lzstd -ldl" \
COSMOS_BUILD_OPTIONS=rocksdb \
make install
```

Check the binary version has the `-rocksdb` suffix

```bash
❯ evmosd version
v14.0.0-rocksdb
```

### Update database configuration

Before starting the process,
make sure to update the `db_backend` configuration parameter in the `config.toml`:

```toml
db_backend = "rocksdb"
```

## Version DB & MemIAVL

:::note
The Evmos team carried out an
[analysis to compare the performance of a 5-node network with LevelDB vs VersionDB + MemIAVL](https://www.notion.so/altiplanic/LevelDB-vs-MemIAVL-VersionDB-2034a05c7e1646369d034eb423a25279?pvs=4).
The results of the analysis show that even though MemIAVL offers
a performance boost for state-sync and fast-sync processes,
it takes a toll on the resources required for the node.
Additionally, the block processing time is higher,
which enhances the chances of missing blocks in validator nodes.
:::

### Version DB

VersionDB is a solution developed by the Cronos team to address the size of the IAVL database.
For more information about it, refer to these resources:

- [VersionDB documentation](https://github.com/crypto-org-chain/cronos/tree/main/versiondb)
- [Blog post](https://blog.cronos.org/p/optimising-cronos-node-storage-with)

#### Prerequisites

- `evmosd` binary with `librocksdb`. Refer to [the previous section](#rocks-db) for the procedure on how to build this binary.

#### Update configuration

To enable versionDB, add `versiondb` to the list of `store.streamers` in `app.toml`:

```toml
[store]
streamers = ["versiondb"]
```

When starting the node with this configuration,
you should see a `version.db` file in the `data` directory.

#### Migration

If you have an existing database and want to migrate this data to versionDB,
follow the [migration guide](https://github.com/crypto-org-chain/cronos/wiki/VersionDB-Migration).

### MemIAVL

MemIAVL is a solution developed by the Cronos team to address
performance issues of the current IAVL implementation ([benchmarks here](https://github.com/crypto-org-chain/cronos/wiki/MemIAVL-Benchmark)).
For more information about it, check [the documentation](https://github.com/crypto-org-chain/cronos/wiki/MemIAVL).

#### Prerequisites

- `evmosd` binary with `librocksdb`. Refer to [the RocksDB section](#rocks-db) for the procedure on how to build this binary.

#### Update configuration

To enable MemIAVL turn on the `memiavl.enable` config item in `app.toml`.
MemIAVL only supports pruned node, the default configuration (`memiavl.snapshot-keep-recent=0`)
is equivalent to `pruning=everything`.
To support historical grpc query services, you should enable versionDB together with it.
If you need to support very old merkle proof generations, don't use memIAVL.

The default MemIAVL section in `app.toml`:

```toml
[memiavl]

# Enable defines if the memiavl should be enabled.
enable = false

# ZeroCopy defines if the memiavl should return slices pointing to mmap-ed buffers directly (zero-copy),
# the zero-copied slices must not be retained beyond current block's execution.
zero-copy = false

# AsyncCommitBuffer defines the size of asynchronous commit queue, this greatly improve block catching-up
# performance, -1 means synchronous commit.
async-commit-buffer = 0

# SnapshotKeepRecent defines what many old snapshots (excluding the latest one) to keep after new snapshots are taken.
snapshot-keep-recent = 0

# SnapshotInterval defines the block interval the memiavl snapshot is taken, default to 1000.
snapshot-interval = 1000

# CacheSize defines the size of the cache for each memiavl store, default to 1000.
cache-size = 1000
```

When starting the node with this configuration,
you should see a `memiavl.db` file in the `data` directory.
