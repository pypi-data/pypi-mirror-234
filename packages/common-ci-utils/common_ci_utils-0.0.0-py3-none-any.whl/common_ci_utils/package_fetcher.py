"""
This module focuses on the downloading of RPM packages.
"""

import logging
import os
import requests
import tempfile

log = logging.getLogger(__name__)


def download_rpm(rpm_url):
    """
    Downloads RPM

    Args:
        rpm_url (str): RPM URL to download

    Returns:
        str: Path to RPM file

    Raise:
        requests.RequestException: In case rpm failed to download

    """
    # Path to save the RPM package
    rpm_name, rpm_ext = os.path.splitext(os.path.split(rpm_url)[1])
    rpm_file = tempfile.NamedTemporaryFile(
        mode="w+", prefix=f"{rpm_name}_", suffix=f"{rpm_ext}", delete=False
    )
    rpm_file_name = rpm_file.name

    try:
        # Send an HTTP GET request to download the RPM package
        response = requests.get(rpm_url)
        response.raise_for_status()

        # Open a local file and write the RPM content to it
        with open(rpm_file_name, "wb") as f:
            f.write(response.content)
        log.info(f"Downloaded RPM package to {rpm_file_name}")
        return rpm_file_name

    except requests.exceptions.RequestException as ex:
        raise requests.RequestException(
            f"Failed to download RPM package. Exception: {ex}"
        )
