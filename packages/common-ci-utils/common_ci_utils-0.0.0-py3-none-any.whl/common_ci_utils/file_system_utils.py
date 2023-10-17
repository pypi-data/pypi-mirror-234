"""
This module contains utility functions which interact with the file system like directory-related functions,
setting permissions on directory/file etc ...
"""

import logging
import os

from common_ci_utils.command_runner import exec_cmd
from common_ci_utils.exceptions import PermissionsFailedToChange

log = logging.getLogger(__name__)


def create_directory(name):
    """
    Creates directory

    Args:
        name (str): Name of directory to create

    """
    # Check if the directory already exists
    if not os.path.exists(name):
        # Create the directory with permissions
        os.makedirs(name, mode=0o777)
        log.info(f"Directory '{name}' created successfully.")
    else:
        log.info(f"Directory '{name}' already exists.")


def set_permissions(directory_path, permissions, use_sudo=False):
    """
    Sets permissions to directory

    Args:
        directory_path (str): Name of the directory to give required permissions.
        permissions (int): permissions to set on directory. permissions must be in
            octal notation. For example, 755 grants read, write, and execute
            permissions to the owner and read and execute permissions to the group and others
        use_sudo (bool): If True cmd will be executed with sudo

    """
    cmd = f"chmod {permissions} {directory_path}"
    result = exec_cmd(cmd=cmd, use_sudo=use_sudo)
    if result.returncode == 0:
        log.info(f"Permissions for '{directory_path}' have been set to {permissions}")
    else:
        raise PermissionsFailedToChange(
            f"Error setting permissions for '{directory_path}': {result.stderr}"
        )
