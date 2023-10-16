from pingsafe_cli.psgraph.terraform.checks.resource.base_resource_value_check import BaseResourceValueCheck
from pingsafe_cli.psgraph.common.models.enums import CheckCategories


class NeptuneClusterSnapshotEncrypted(BaseResourceValueCheck):
    def __init__(self) -> None:
        name = "Ensure Neptune snapshot is securely encrypted"
        id = "CKV_AWS_279"
        supported_resources = ("aws_neptune_cluster_snapshot",)
        categories = (CheckCategories.ENCRYPTION,)
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def get_inspected_key(self) -> str:
        return "storage_encrypted"


check = NeptuneClusterSnapshotEncrypted()
