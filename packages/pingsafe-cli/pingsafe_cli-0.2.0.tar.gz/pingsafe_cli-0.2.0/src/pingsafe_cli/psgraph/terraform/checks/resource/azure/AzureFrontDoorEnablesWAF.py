from pingsafe_cli.psgraph.common.models.consts import ANY_VALUE
from pingsafe_cli.psgraph.common.models.enums import CheckCategories
from pingsafe_cli.psgraph.terraform.checks.resource.base_resource_value_check import BaseResourceValueCheck


class AzureFrontDoorEnablesWAF(BaseResourceValueCheck):
    def __init__(self):
        name = "Ensure that Azure Front Door enables WAF"
        id = "CKV_AZURE_121"
        supported_resources = ['azurerm_frontdoor']
        categories = [CheckCategories.NETWORKING]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def get_inspected_key(self):
        return "frontend_endpoint/[0]/web_application_firewall_policy_link_id"

    def get_expected_value(self):
        return ANY_VALUE


check = AzureFrontDoorEnablesWAF()
