"""
This file contains the tests for the logic
that is extracting the available endpoints
from the Markdown file.
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))

from endpoints import Endpoint, get_endpoint_from_line, get_endpoints


def test_get_endpoint_from_line_pass():
    assert get_endpoint_from_line(
        "| `https://evmos.lava.build`                    | `Ethereum` `JSON-RPC`  | [Lava Network](https://lavanet.xyz)             | Pruned     |"
    ) == Endpoint(
        address="https://evmos.lava.build",
        category="Ethereum JSON-RPC",
        provider="Lava Network"
    )


def test_get_endpoints_pass():
    mainnet, testnet = get_endpoints(os.path.join(os.path.dirname(__file__), "testdata/networks.mdx"))
    assert len(mainnet) > 0, "failed to get mainnet endpoints"
    assert len(testnet) > 0, "failed to get testnet endpoints"
