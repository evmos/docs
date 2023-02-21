# Frequently Asked Questions

## Concepts

<details>

<summary><b>What is the difference between "secp256k1" and "ed25519"?</b></summary>

secp256k1 and ed25519 are both popular cryptographic algorithms used for digital signatures and key generation, but they have some differences in terms of security, performance, and compatibility with different systems.

secp256k1 is an elliptic curve algorithm that is widely used in Bitcoin and many other cryptocurrencies. It provides 128-bit security, which is considered sufficient for most practical purposes. secp256k1 is relatively fast and efficient, making it a good choice for applications that require high performance. It is widely supported by most cryptographic libraries and software, which makes it a good choice for cross-platform applications.

ed25519 is a newer elliptic curve algorithm that provides 128-bit security, similar to secp256k1. However, ed25519 is generally considered to be more secure than secp256k1, due to its resistance to certain types of attacks such as [side-channel attacks](https://en.wikipedia.org/wiki/Side-channel_attack). It is also faster than many other elliptic curve algorithms, including secp256k1, making it a good choice for applications that require high performance.

In terms of compatibility, secp256k1 is more widely supported by existing systems, while ed25519 is less widely supported. However, ed25519 is gaining popularity, and is supported by many cryptographic libraries and software.

When choosing between secp256k1 and ed25519, you should consider your specific needs in terms of security, performance, and compatibility. If you are building an application that requires high performance and compatibility with existing systems, secp256k1 may be a better choice. However, if you are building an application that requires a higher level of security and performance, and you can afford to sacrifice some compatibility, ed25519 may be a better choice.

</details>
