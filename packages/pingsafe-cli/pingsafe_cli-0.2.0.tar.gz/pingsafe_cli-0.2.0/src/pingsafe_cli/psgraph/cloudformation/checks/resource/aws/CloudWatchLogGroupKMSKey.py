from pingsafe_cli.psgraph.common.models.enums import CheckCategories
from pingsafe_cli.psgraph.cloudformation.checks.resource.base_resource_value_check import BaseResourceValueCheck
from pingsafe_cli.psgraph.common.models.consts import ANY_VALUE


class CloudWatchLogGroupKMSKey(BaseResourceValueCheck):
    def __init__(self):
        name = "Ensure that CloudWatch Log Group is encrypted by KMS"
        id = "CKV_AWS_158"
        supported_resource = ['AWS::Logs::LogGroup']
        categories = [CheckCategories.ENCRYPTION]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resource)

    def get_inspected_key(self):
        return 'Properties/KmsKeyId'

    def get_expected_value(self):
        return ANY_VALUE


check = CloudWatchLogGroupKMSKey()
