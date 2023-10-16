from __future__ import annotations

from typing import Any

from pingsafe_cli.psgraph.common.models.enums import CheckResult, CheckCategories
from pingsafe_cli.psgraph.arm.base_resource_check import BaseResourceCheck


class StorageBlobServiceContainerPrivateAccess(BaseResourceCheck):
    def __init__(self) -> None:
        # https://docs.microsoft.com/en-us/azure/templates/microsoft.storage/storageaccounts/blobservices/containers
        # publicAccess default is None
        name = "Ensure that 'Public access level' is set to Private for blob containers"
        id = "CKV_AZURE_34"
        supported_resources = (
            'Microsoft.Storage/storageAccounts/blobServices/containers',
            'containers',
            'blobServices/containers',
        )
        categories = (CheckCategories.NETWORKING,)
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf: dict[str, Any]) -> CheckResult:
        if "properties" in conf:
            if "publicAccess" in conf["properties"]:
                if str(conf["properties"]["publicAccess"]).lower() == "container" or \
                        str(conf["properties"]["publicAccess"]).lower() == "blob":
                    return CheckResult.FAILED
        return CheckResult.PASSED


check = StorageBlobServiceContainerPrivateAccess()
