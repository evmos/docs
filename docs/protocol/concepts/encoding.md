---
sidebar_position: 3
---

# Encoding

Encoding refers to the process of converting data from one format to another to make it more secure and efficient.
In the context of blockchain, encoding is used to ensure that data is stored and transmitted in a way that is secure and
easily accessible.

The Recursive Length Prefix (RLP) is a serialization format used extensively in Ethereum's execution clients. Its purpose
is to encode arbitrarily nested arrays of binary data, and it is the main encoding method used to serialize objects in
Ethereum. RLP only encodes structure and leaves encoding specific atomic data types, such as strings, integers, and floats,
to higher-order protocols.

In Ethereum, integers must be represented in big-endian binary form with no leading zeroes,
making the integer value zero equivalent to the empty byte array. The RLP encoding function takes in an item, which is
defined as a single byte whose value is in the [0x00, 0x7f] range or a string of 0-55 bytes long. If the string is
more than 55 bytes long, the RLP encoding consists of a single byte with value 0xb7 (dec. 183) plus the length in
bytes of the length of the string in binary form, followed by the length of the string, followed by the string. RLP
is used for hash verification, where a transaction is signed by signing the RLP hash of the transaction
data, and blocks are identified by the RLP hash of their header. RLP is also used for encoding data over the wire
and for some cases where there should be support for efficient encoding of the merkle tree data structure. The
Ethereum execution layer uses RLP as the primary encoding method to serialize objects, but the newer Simple
Serialize (SSZ) replaces RLP as the encoding for the new consensus layer in Ethereum 2.0.

The Cosmos Stargate release introduces protobuf as the main encoding format for both client and state serialization.
All the EVM module types that are used for state and clients, such as transaction messages, genesis, query services,
etc., will be implemented as protocol buffer messages. The Cosmos SDK also supports the legacy Amino encoding.
Protocol Buffers (protobuf) is a language-agnostic binary serialization format that is smaller and faster than JSON.
It is used to serialize structured data, such as messages, and is designed to be highly efficient and extensible. The
encoding format is defined in a language-agnostic language called Protocol Buffers Language (proto3), and the encoded
messages can be used to generate code for a variety of programming languages. The main advantage of protobuf is its
efficiency, which results in smaller message sizes and faster serialization and deserialization times. The RLP decoding
process is as follows: according to the first byte (i.e., prefix) of input data and decoding the data type, the length
of the actual data and offset; according to the type and offset of data, decode the data correspondingly.

## Prerequisite Readings

- [Cosmos SDK Encoding](https://docs.cosmos.network/main/core/encoding.html)
- [Ethereum RLP](https://eth.wiki/en/fundamentals/rlp)

## Encoding Formats

### Protocol Buffers

The Cosmos [Stargate](https://stargate.cosmos.network/) release introduces
[protobuf](https://developers.google.com/protocol-buffers) as the main encoding format for both
client and state serialization. All the EVM module types that are used for state and clients
(transaction messages, genesis, query services, etc) will be implemented as protocol buffer messages.

### Amino

The Cosmos SDK also supports the legacy Amino encoding format for backwards compatibility with
previous versions, specially for client encoding and signing with Ledger devices. Evmos does not
support Amino in the EVM module, but it is supported for all other Cosmos SDK modules that enable it.

### RLP

Recursive Length Prefix ([RLP](https://eth.wiki/en/fundamentals/rlp)),
is an encoding/decoding algorithm that serializes a message and
allows for quick reconstruction of encoded data. Evmos uses RLP to encode/decode Ethereum
messages for JSON-RPC handling to conform messages to the proper Ethereum format. This allows
messages to be encoded and decoded in the exact format as Ethereum's.

The `x/evm` transactions (`MsgEthereumTx`) encoding is performed by casting the message to a go-ethereum's `Transaction`
and then marshaling the transaction data using RLP:

```go
// TxEncoder overwrites sdk.TxEncoder to support MsgEthereumTx
func (g txConfig) TxEncoder() sdk.TxEncoder {
return func(tx sdk.Tx) ([]byte, error) {
  msg, ok := tx.(*evmtypes.MsgEthereumTx)
  if ok {
    return msg.AsTransaction().MarshalBinary()
  }
  return g.TxConfig.TxEncoder()(tx)
}
}

// TxDecoder overwrites sdk.TxDecoder to support MsgEthereumTx
func (g txConfig) TxDecoder() sdk.TxDecoder {
return func(txBytes []byte) (sdk.Tx, error) {
  tx := &ethtypes.Transaction{}

  err := tx.UnmarshalBinary(txBytes)
  if err == nil {
    msg := &evmtypes.MsgEthereumTx{}
    msg.FromEthereumTx(tx)
    return msg, nil
  }

  return g.TxConfig.TxDecoder()(txBytes)
}
}
```
