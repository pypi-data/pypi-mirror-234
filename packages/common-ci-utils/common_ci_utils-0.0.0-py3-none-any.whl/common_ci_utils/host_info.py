"""
This module handles various host-related information.
"""

import logging
import socket

log = logging.getLogger(__name__)


def get_hostname():
    """
    Fetches hostname

    Returns:
        str: Hostname

    """
    return socket.gethostname()


def get_ip_address():
    """
    Fetches IP address

    Returns:
        str: IP address

    """
    hostname = get_hostname()
    return socket.gethostbyname(hostname)
