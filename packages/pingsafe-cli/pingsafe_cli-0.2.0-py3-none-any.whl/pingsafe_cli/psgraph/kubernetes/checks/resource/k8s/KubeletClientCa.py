from typing import Dict, Any

from pingsafe_cli.psgraph.common.models.enums import CheckResult
from pingsafe_cli.psgraph.kubernetes.checks.resource.base_container_check import BaseK8sContainerCheck


class KubeletClientCa(BaseK8sContainerCheck):
    def __init__(self) -> None:
        # CIS-1.6 4.2.3
        id = "CKV_K8S_140"
        name = "Ensure that the --client-ca-file argument is set as appropriate"
        super().__init__(name=name, id=id)

    def scan_container_conf(self, metadata: Dict[str, Any], conf: Dict[str, Any]) -> CheckResult:
        self.evaluated_container_keys = ["command"]
        if conf.get("command"):
            if "kubelet" in conf["command"]:
                for command in conf["command"]:
                    if command.startswith("--client-ca-file"):
                        if len(command.split("=")) == 2:
                            if (command.split("=")[1]).strip() != '':
                                return CheckResult.PASSED
                        return CheckResult.FAILED
                return CheckResult.FAILED


check = KubeletClientCa()
