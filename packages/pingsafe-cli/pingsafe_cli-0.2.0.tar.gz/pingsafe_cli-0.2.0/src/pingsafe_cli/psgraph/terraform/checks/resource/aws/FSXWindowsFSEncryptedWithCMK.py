from pingsafe_cli.psgraph.common.models.consts import ANY_VALUE
from pingsafe_cli.psgraph.terraform.checks.resource.base_resource_value_check import BaseResourceValueCheck
from pingsafe_cli.psgraph.common.models.enums import CheckCategories


class FSXWindowsFSEncryptedWithCMK(BaseResourceValueCheck):
    def __init__(self):
        name = "Ensure FSX Windows filesystem is encrypted by KMS using a customer managed Key (CMK)"
        id = "CKV_AWS_179"
        supported_resources = ['aws_fsx_windows_file_system']
        categories = [CheckCategories.ENCRYPTION]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def get_inspected_key(self):
        return "kms_key_id"

    def get_expected_value(self):
        return ANY_VALUE


check = FSXWindowsFSEncryptedWithCMK()
