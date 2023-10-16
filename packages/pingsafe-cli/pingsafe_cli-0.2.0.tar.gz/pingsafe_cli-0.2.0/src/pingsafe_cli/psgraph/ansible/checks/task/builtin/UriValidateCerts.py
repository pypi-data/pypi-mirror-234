from __future__ import annotations

from pingsafe_cli.psgraph.ansible.checks.base_ansible_task_value_check import BaseAnsibleTaskValueCheck
from pingsafe_cli.psgraph.common.models.enums import CheckResult, CheckCategories


class UriValidateCerts(BaseAnsibleTaskValueCheck):
    def __init__(self) -> None:
        name = "Ensure that certificate validation isn't disabled with uri"
        id = "CKV_ANSIBLE_1"
        super().__init__(
            name=name,
            id=id,
            categories=(CheckCategories.GENERAL_SECURITY,),
            supported_modules=("ansible.builtin.uri", "uri"),
            missing_block_result=CheckResult.PASSED,
        )

    def get_inspected_key(self) -> str:
        return "validate_certs"


check = UriValidateCerts()
