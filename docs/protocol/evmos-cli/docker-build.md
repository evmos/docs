---
sidebar_position: 3
---

# Working with Docker

There are multiple ways to use Evmos with Docker.
If you want to run Evmos inside a Docker setup and possibly connect the Docker container
to other containerized compatible blockchain binaries, check out the guide on
[building a Docker image containing the Evmos binary](#building-a-docker-image-containing-the-binary).
If you instead want to generate a binary for use outside of Docker,
but want to ensure the correct dependencies are used by building the binary inside a Docker container,
then go ahead to the section on [building the Evmos binary with Docker](#building-the-binary-with-docker).

:::note
The given instructions have been tested on *Ubuntu 18.04.2 LTS* with *Docker 20.10.2* and *macOS 13.2.1* with *Docker 20.10.22*.
:::

## Prerequisites

- [Install Docker](https://docs.docker.com/get-docker/)

## General Setup

In order to build Evmos binaries with Docker, it is necessary to

- clone the Evmos repository to your local machine (e.g. `git clone git@github.com/evmos/evmos.git`)
- checkout the commit, branch, or release tag you want to build (e.g. `git checkout v11.0.2`)

## Building A Docker Image Containing The Binary

To build a Docker image, that contains the Evmos binary,
step into the cloned repository and run the following command in a terminal session:

```bash
make build-docker
```

This will create an image with the name `tharsishq/evmos` and the version tag `latest`.
Now it is possible to run the `evmosd` binary in the container, e.g. evaluating its version:

```bash
docker run -it --rm tharsishq/evmos:latest evmosd version
```

## Building The Binary With Docker

It is possible to build the `evmosd` binary deterministically using Docker.
The container system that Docker provides offers the ability
to create an instance of the Evmos binary in an isolated environment.

### Building the Image

Run the following command to launch a build for all supported architectures (currently **linux/amd64**):

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

The [Tendermint builder Docker image](https://github.com/tendermint/images/tree/master/rbuilder)
provides a deterministic build environment that is used to build Cosmos SDK applications.
It provides a way to be reasonably sure that the executables are really built from the git source.
It also makes sure that the same, tested dependencies are used and statically built into the executable.

----

Now that you have built the Evmos binary, either for local use or in a Docker container,
you'll find information to run a node instance in the following section
on [setting up a local network](./single-node).
