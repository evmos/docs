"""
This file contains the logic to download the latest evmosd binary
from the GitHub releases.
"""

import requests
import os
import subprocess
import tarfile
import platform
from typing import Tuple


def get_target_binary() -> dict:
    """
    This method returns the target binary name and path.
    """
    # Step 1: Determine the system architecture
    system = platform.system().lower()
    architecture = platform.machine().lower()

    target_binary = {}

    # Map the architecture to the GitHub release asset name
    if system == 'darwin':
        if architecture == 'arm64':
            target_binary['asset_name'] = 'Darwin_arm64'
        elif architecture == 'x86_64':
            target_binary['asset_name'] = 'Darwin_amd64'
        else:
            raise Exception("Unsupported architecture for macOS.")
    
    elif system == 'linux':
        if architecture == 'x86_64':
            target_binary['asset_name'] = 'Linux_amd64'
        elif architecture == 'aarch64':
            target_binary['asset_name'] = 'Linux_arm64'
        else:
            raise Exception("Unsupported architecture for Linux.")

    else:
        raise Exception("Unsupported operating system.")

    return target_binary


def get_download_url(target_binary: dict) -> str:
    """
    This method returns the download URL for the latest evmosd binary.
    """
    # Step 2: Fetch the latest release information
    api_url = f"https://api.github.com/repos/evmos/evmos/releases/latest"

    response = requests.get(api_url)
    release_info = response.json()

    # Step 3: Download the binary
    binary_url = None
    for asset in release_info['assets']:
        if target_binary['asset_name'] in asset['name']:
            binary_url = asset['browser_download_url']
            break

    if not binary_url:
        raise Exception(f"Binary for {target_binary['asset_name']} not found in the latest release.")

    return binary_url


def download_binary(download_url: str) -> Tuple[str, str, str]:
    """
    This method downloads the binary from the given URL
    and extracts it from the tar.gz file.
    """
    # Download the binary
    binary_response = requests.get(download_url)
    download_path = download_url.split('/')[-1]
    with open(download_path, 'wb') as file:
        file.write(binary_response.content)

    # Extract the binary if it's a tar.gz file
    if not download_path.endswith('.tar.gz'):
        raise ValueError("expected downloaded file to be a tar.gz file")

    extract_path = download_path.rstrip('.tar.gz')
    with tarfile.open(download_path, 'r:gz') as tar:
        tar.extractall(extract_path)

    binary_path = os.path.join(extract_path, 'bin', 'evmosd')

    return download_path, extract_path, binary_path


def get_binary() -> Tuple[str, str, str]:
    """
    This method downloads and returns the path to the downloaded file,
    the path to the extracted file and the path to the binary itself.
    """
    target_binary = get_target_binary()
    binary_url = get_download_url(target_binary)
    download_path, extract_path, binary_path = download_binary(binary_url)

    return download_path, extract_path, binary_path


def run_binary(binary_path: str, command: str) -> str:
    """
    This method runs the binary with the given command.
    """
    result = subprocess.run(
        [binary_path, command],
        capture_output=True,
        text=True
    )

    return result.stdout
