---
sidebar_position: 3	
---

# Build with Docker

Build the `evmosd` binary deterministically using Docker.
The container system that Docker provides offers the ability
to create an instance of the Evmos binary in an isolated environment.

:::tip
All the following instructions have been tested on *Ubuntu 18.04.2 LTS* with *Docker 20.10.2* and *MacOS 13.2.1* with *Docker 20.10.22*.
:::

## Prerequisites

- [Install Docker](https://docs.docker.com/get-docker/) 

## Building the Image

In order to build the docker image that contains the Evmos binary, clone the Evmos repository:

``` bash
git clone git@github.com:evmos/evmos.git
```

Checkout the commit, branch, or release tag you want to build (eg `v11.0.2`):

```bash
cd evmos/
git checkout v11.0.2
```

The build system supports and produces binaries for the following architectures:

* **linux/amd64**

Run the following command to launch a build for all supported architectures:

```bash
make distclean build-reproducible
```

The build system generates both the binaries and deterministic build report in the `artifacts` directory.
The `artifacts/build_report` file contains the list of the build artifacts and their respective checksums,
and can be used to verify build sanity. An example of its contents follows:

```
App: evmosd
Version: 11.0.2
Commit: 8eeeac7ae42a5b2695fea7f56868f3c6e9bc2378
Files:
 6b5939adfd9a8ce964d78fcaab16091a  evmosd-11.0.2-linux-amd64
 ac503925c535ddb8ee0fbebbb96d0eb9  evmosd-11.0.2.tar.gz
Checksums-Sha256:
 0857d59c285a87b7d354aa6d566db90c56663d938a88d41d35415da490708aea  evmosd-11.0.2-linux-amd64
 5005814fc34abc02d7e30dcfbe67e363c1b593efb774e0c97ebb7ec713baf306  evmosd-11.0.2.tar.gz
```

### Builder Image

The [Tendermint rbuilder Docker image](https://github.com/tendermint/images/tree/master/rbuilder)
provides a deterministic build environment that is used to build Cosmos SDK applications.
It provides a way to be reasonably sure that the executables are really built from the git source.
It also makes sure that the same, tested dependencies are used and statically built into the executable.
