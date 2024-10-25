"""
This file contains the logic to extract the available endpoints
from the Markdown file of the docs.
"""

import os
import re
from dataclasses import dataclass
from typing import List, Union


@dataclass
class Endpoint:
    address: str
    category: str
    provider: str


ENDPOINT_PATTERN = re.compile(r'\|\s*`(?P<endpoint>[^`]+)`\s*\|\s*`(?P<type1>[^`]+)`\s*`(?P<type2>[^`]+)`\s*\|\s*\[(?P<provider>[^\]]+)\]'"")


def get_endpoint_from_line(line: str) -> Union[Endpoint, None]:
    """
    This method extracts the information of a given endpoint
    from one line of the Markdown table.
    """
    match = ENDPOINT_PATTERN.search(line)
    if not match:
        return None

    return Endpoint(
        address=match.group("endpoint"),
        category=f'{match.group("type1")} {match.group("type2")}',
        provider=match.group("provider")
    )


def extract_endpoints(contents: List[str]) -> List[List[str]]:
    """
    This function extracts the available endpoints
    for testnet and mainnet from the given file contents.
    """
    testnet_endpoints = []
    mainnet_endpoints = []

    extract_mainnet = False
    extract_testnet = False

    for line in contents:
        if line[0] not in ["#", "|"]:
            continue
        
        if "### Mainnet" in line:
            extract_mainnet = True
            extract_testnet = False
            continue
        elif "### Testnet" in line:
            extract_mainnet = False
            extract_testnet = True
            continue
        elif line[0] != "|":
            continue

        endpoint = get_endpoint_from_line(line)
        if endpoint is None:
            continue

        if extract_mainnet:
            mainnet_endpoints.append(endpoint)
            continue

        if extract_testnet:
            testnet_endpoints.append(endpoint)
            continue

        raise ValueError(f"unexpected condition: got endpoint {endpoint.address} but neither testnet nor mainnet is active to be extracted")

    return mainnet_endpoints, testnet_endpoints


def get_endpoints(file: str) -> List[str]:
    """
    This method tries to extract the list of available endpoints from
    from the given docs file. 
    """
    if not os.path.exists(file):
        raise FileNotFoundError(f"{file} does not exist")

    with open(file, "r", encoding="utf-8") as f:
        contents = f.readlines()

    return extract_endpoints(contents)

