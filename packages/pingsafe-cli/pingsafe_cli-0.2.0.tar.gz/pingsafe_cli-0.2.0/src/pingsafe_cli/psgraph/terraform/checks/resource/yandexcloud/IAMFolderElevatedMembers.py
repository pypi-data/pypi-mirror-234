from typing import List, Any
from pingsafe_cli.psgraph.common.models.enums import CheckCategories
from pingsafe_cli.psgraph.terraform.checks.resource.base_resource_negative_value_check import BaseResourceNegativeValueCheck


class IAMFolderElevatedMembers(BaseResourceNegativeValueCheck):
    def __init__(self) -> None:
        name = "Ensure folder member does not have elevated access."
        id = "CKV_YC_23"
        categories = (CheckCategories.IAM,)
        supported_resources = ("yandex_resourcemanager_folder_iam_binding", "yandex_resourcemanager_folder_iam_member")
        super().__init__(
            name=name,
            id=id,
            categories=categories,
            supported_resources=supported_resources,
        )

    def get_inspected_key(self) -> str:
        return "role"

    def get_forbidden_values(self) -> List[Any]:
        return ["admin", "editor"]


check = IAMFolderElevatedMembers()
