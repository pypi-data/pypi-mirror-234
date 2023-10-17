"""
This module handles the selection of postgresql version
"""

import logging

from common_ci_utils.command_runner import exec_cmd

log = logging.getLogger(__name__)


def enable_postgresql_version(version):
    """
    Enable postgresql version

    Args:
        version (int): postgresql version to enable

    """
    log.info(f"Enable the module stream for Postgres version to {version}")
    cmd = f"sudo dnf module enable postgresql:{version}"
    exec_cmd(cmd)
