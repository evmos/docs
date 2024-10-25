"""
This file contains the tests for the endpoint queries.
"""

from .endpoints import Endpoint
from .queries import query_endpoint


def test_query_json_rpc():
	assert query_endpoint(Endpoint(
		address="https://evmos.lava.build",
		category="Ethereum JSON-RPC",
		provider="Lava Network"
	)) is True, "expected successful JSON-RPC call"


def test_query_cosmos_rest():
	assert query_endpoint(Endpoint(
		address="https://evmos.rest.lava.build",
		category="Cosmos REST",
		provider="Lava Network"
	)) is True, "expected successful Cosmos REST call"


def test_query_tendermint_rpc():
	assert query_endpoint(Endpoint(
		address="https://evmos.tendermintrpc.lava.build",
		category="Tendermint RPC",
		provider="Lava Network"
	)) is True, "expected successful Tendermint RPC call"
