"""
This file contains the required logic to
call a simple query on a given endpoint
based on the type of endpoint.
"""

from endpoints import Endpoint
import requests
from typing import Union


def query_endpoint(ep: Endpoint) -> Union[bool, None]:
    """
    This function queries an endpoint based on its type.
    """
    if ep.category == "Ethereum JSON-RPC":
        return query_json_rpc(ep.address)
    elif ep.category == "Cosmos REST":
        return query_cosmos_rest(ep.address)
    elif ep.category == "Tendermint RPC":
        return query_tendermint_rpc(ep.address)
    else:
        return None


def query_json_rpc(address: str) -> bool:
    """
    This method queries the latest block on the Ethereum JSON-RPC.
    """
    try:
        response = requests.post(
            address,
        json={
            "jsonrpc":"2.0",
            "method":"eth_blockNumber",
            "params":[],
            "id":83
        }
    )
        return response.status_code == requests.codes.OK
    except Exception as e:
        print(f"failed to query JSON-RPC endpoint {address}: {e}")
        return False


def query_cosmos_rest(address: str) -> bool:
    """
    This method queries the latest block on the Cosmos REST.
    """
    try:
        full_address = f"{address}/cosmos/base/tendermint/v1beta1/blocks/latest"
        response = requests.get(full_address)
        return response.status_code == requests.codes.OK
    except Exception as e:
        print(f"failed to query Cosmos REST endpoint {address}: {e}")
        return False


def query_tendermint_rpc(address: str) -> bool:
    """
    This method queries the latest block on the Tendermint RPC.
    """
    try:
        response = requests.get(f"{address}/block")
        return response.status_code == requests.codes.OK
    except Exception as e:
        print(f"failed to query Tendermint RPC endpoint {address}: {e}")
        return False
