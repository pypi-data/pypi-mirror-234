from typing import Dict, Any

from pingsafe_cli.psgraph.common.models.enums import CheckResult
from pingsafe_cli.psgraph.kubernetes.checks.resource.base_container_check import BaseK8sContainerCheck


class KubletRotateCertificates(BaseK8sContainerCheck):
    def __init__(self) -> None:
        # CIS-1.6 4.2.11
        id = "CKV_K8S_149"
        name = "Ensure that the --rotate-certificates argument is not set to false"
        super().__init__(name=name, id=id)

    def scan_container_conf(self, metadata: Dict[str, Any], conf: Dict[str, Any]) -> CheckResult:
        self.evaluated_container_keys = ["command"]
        if conf.get("command"):
            if "kubelet" in conf["command"]:
                if "--rotate-certificates=false" in conf["command"]:
                    return CheckResult.FAILED

        return CheckResult.PASSED


check = KubletRotateCertificates()
