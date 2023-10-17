"""
This module manages various aspects of RPM packages, with a focus on installation, upgrade
and removing rpms.
"""

import logging

from common_ci_utils.command_runner import exec_cmd
from common_ci_utils.exceptions import RPMInstallationFailed

log = logging.getLogger(__name__)


def install_rpm(rpm_path=None, packages=None):
    """
    Install RPMs/packages

    Args:
        rpm_path (str): RPM path to install
        packages (list): List of packages to install

    """
    target_to_install = rpm_path if rpm_path else " ".join(map(str, packages))
    log.info(f"Installing {target_to_install}")
    cmd = f"yum install {target_to_install} -y"
    result = exec_cmd(cmd, use_sudo=True)
    if result.returncode == 0:
        log.info(f"Successfully installed {rpm_path}")
    else:
        raise RPMInstallationFailed(f"Error installing {rpm_path}:\n{result.stderr}")
