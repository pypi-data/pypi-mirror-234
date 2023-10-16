from pingsafe_cli.psgraph.common.models.consts import ANY_VALUE
from pingsafe_cli.psgraph.common.models.enums import CheckCategories
from pingsafe_cli.psgraph.terraform.checks.resource.base_resource_value_check import BaseResourceValueCheck


class APIServicesUseVirtualNetwork(BaseResourceValueCheck):
    def __init__(self):
        name = "Ensure that API management services use virtual networks"
        id = "CKV_AZURE_107"
        supported_resources = ['azurerm_api_management']
        categories = [CheckCategories.NETWORKING]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def get_inspected_key(self):
        return "virtual_network_configuration/[0]/subnet_id"

    def get_expected_value(self):
        return ANY_VALUE


check = APIServicesUseVirtualNetwork()
