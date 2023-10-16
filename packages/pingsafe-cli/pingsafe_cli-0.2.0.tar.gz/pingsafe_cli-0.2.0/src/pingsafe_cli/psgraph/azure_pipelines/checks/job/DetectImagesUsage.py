from __future__ import annotations

from typing import Any

from pingsafe_cli.psgraph.azure_pipelines.checks.base_azure_pipelines_check import BaseAzurePipelinesCheck
from pingsafe_cli.psgraph.common.models.enums import CheckResult, CheckCategories
from pingsafe_cli.psgraph.yaml_doc.enums import BlockType


class DetectImageUsage(BaseAzurePipelinesCheck):
    def __init__(self) -> None:
        name = "Detecting image usages in azure pipelines workflows"
        id = "CKV_AZUREPIPELINES_5"
        super().__init__(
            name=name,
            id=id,
            categories=(CheckCategories.SUPPLY_CHAIN,),
            supported_entities=("jobs[]", "stages[].jobs[]", "*.container[]"),
            block_type=BlockType.ARRAY,
        )

    def scan_conf(self, conf: dict[str, Any]) -> tuple[CheckResult, dict[str, Any]]:
        return CheckResult.PASSED, conf


check = DetectImageUsage()
