from pingsafe_cli.psgraph.common.models.enums import CheckCategories
from pingsafe_cli.psgraph.terraform.checks.resource.base_resource_value_check import BaseResourceValueCheck


class ACREnableRetentionPolicy(BaseResourceValueCheck):
    def __init__(self) -> None:
        name = "Ensure a retention policy is set to cleanup untagged manifests."
        id = "CKV_AZURE_167"
        supported_resources = ("azurerm_container_registry",)
        categories = (CheckCategories.GENERAL_SECURITY,)
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def get_inspected_key(self) -> str:
        return "retention_policy/enabled"


check = ACREnableRetentionPolicy()
