from __future__ import annotations

from typing import Any

from pingsafe_cli.psgraph.common.models.enums import CheckCategories
from pingsafe_cli.psgraph.terraform.checks.resource.base_resource_value_check import BaseResourceValueCheck


class CDNDisableHttpEndpoints(BaseResourceValueCheck):
    def __init__(self) -> None:
        # This is the full description of your check
        description = "Ensure the Azure CDN disables the HTTP endpoint"

        # This is the Unique ID for your check
        id = "CKV_AZURE_197"

        # These are the Terraform objects supported by this check (ex: aws_iam_policy_document)
        supported_resources = ("azurerm_cdn_endpoint",)

        # Valid CheckCategories are defined in pingsafe_cli.psgraph/common/models/enums.py
        categories = (CheckCategories.NETWORKING,)
        super().__init__(name=description, id=id, categories=categories, supported_resources=supported_resources)

    def get_inspected_key(self) -> str:
        return "is_http_allowed"

    def get_expected_value(self) -> Any:
        return False


check = CDNDisableHttpEndpoints()
