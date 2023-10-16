# flake8: noqa
from termcolor import colored

from pingsafe_cli.psgraph.version import version
from pingsafe_cli.psgraph.common.version_manager import check_for_update

tool = "PingSafe"
banner = r"""
       _               _              
   ___| |__   ___  ___| | _______   __
  / __| '_ \ / _ \/ __| |/ / _ \ \ / /
 | (__| | | |  __/ (__|   < (_) \ V / 
  \___|_| |_|\___|\___|_|\_\___/ \_/  
                                      
By pingsafe.io | version: {} """.format(version)

new_version = check_for_update("pingsafe", version)
if new_version:
    banner = (
        "\n"
        + banner
        + "\nUpdate available "
        + colored(version, "grey")
        + " -> "
        + colored(new_version, "green")
        + "\nRun "
        + colored("pip3 install -U pingsafe", "magenta")
        + " to update \n"
    )
