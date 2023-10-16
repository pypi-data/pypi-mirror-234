from typing import Dict, Any

from pingsafe_cli.psgraph.common.models.enums import CheckResult
from pingsafe_cli.psgraph.kubernetes.checks.resource.base_container_check import BaseK8sContainerCheck


class KubeletMakeIptablesUtilChains(BaseK8sContainerCheck):
    def __init__(self) -> None:
        # CIS-1.6 4.2.7
        id = "CKV_K8S_145"
        name = "Ensure that the --make-iptables-util-chains argument is set to true"
        super().__init__(name=name, id=id)

    def scan_container_conf(self, metadata: Dict[str, Any], conf: Dict[str, Any]) -> CheckResult:
        self.evaluated_container_keys = ["command"]
        if conf.get("command"):
            if "kubelet" in conf["command"]:
                if "--make-iptables-util-chains=true" not in conf["command"]:
                    return CheckResult.FAILED

        return CheckResult.PASSED


check = KubeletMakeIptablesUtilChains()
