from pingsafe_cli.psgraph.common.models.enums import CheckCategories
from pingsafe_cli.psgraph.terraform.checks.resource.base_resource_value_check import BaseResourceValueCheck


class ACREnableImageQuarantine(BaseResourceValueCheck):
    def __init__(self) -> None:
        name = "Ensure container image quarantine, scan, and mark images verified"
        id = "CKV_AZURE_166"
        supported_resources = ("azurerm_container_registry",)
        categories = (CheckCategories.SUPPLY_CHAIN,)
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def get_inspected_key(self) -> str:
        return "quarantine_policy_enabled"


check = ACREnableImageQuarantine()
