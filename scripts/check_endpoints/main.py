"""
This tool checks the list of available endpoints for their functionality.
Any non-responsive endpoints are being flagged to be either discussed
with the corresponding partners or removed.
"""

import os
import shutil
from typing import Union
from endpoints import Endpoint, get_endpoints
from queries import query_endpoint
from evmosd import get_binary

ENDPOINTS_FILE = "docs/develop/api/networks.mdx"


def print_output(endpoint: Endpoint, ok: Union[bool, None]):
    ok_emoji = "❓" if ok is None else ("✅" if ok else "❌")
    print(f"  {ok_emoji} - {endpoint.address}")


def check_endpoints(file: str, evmosd_path: str) -> bool:
    """
    This function contains the main logic of the script,
    which gets the list of available endpoints on the docs
    and runs a query to all of the supported endpoint types.
    """
    failed_endpoints = []
    mainnet_endpoints, testnet_endpoints = get_endpoints(file)

    print("\n--------------\nChecking mainnet endpoints")
    for endpoint in mainnet_endpoints:
        ok = query_endpoint(endpoint, evmosd_path)
        if ok is False:
            failed_endpoints.append(endpoint.address)
            
        print_output(endpoint, ok)

    print("\n--------------\nChecking testnet endpoints")
    for endpoint in testnet_endpoints:
        ok = query_endpoint(endpoint, evmosd_path)
        if ok is False:
            failed_endpoints.append(endpoint.address)
            
        print_output(endpoint, ok)

    return failed_endpoints == []


if __name__ == "__main__":
    print("\n--------------\nDownloading latest evmosd binary")
    download_path, extract_path, binary_path = get_binary()

    all_passed = check_endpoints(ENDPOINTS_FILE, binary_path)

    print("\n--------------\nCleaning up")
    print(f"  Removing {download_path}")
    os.remove(download_path)
    print(f"  Removing {extract_path}")
    shutil.rmtree(extract_path)

    if not all_passed:
        raise ValueError("some endpoints failed to return a response; check the output")
