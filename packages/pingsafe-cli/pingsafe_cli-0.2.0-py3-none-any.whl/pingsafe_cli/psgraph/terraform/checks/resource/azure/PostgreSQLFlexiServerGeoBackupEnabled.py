from pingsafe_cli.psgraph.common.models.enums import CheckCategories
from pingsafe_cli.psgraph.terraform.checks.resource.base_resource_value_check import BaseResourceValueCheck


class PostgreSQLFlexiServerGeoBackupEnabled(BaseResourceValueCheck):
    def __init__(self):
        name = "Ensure that PostgreSQL Flexible server enables geo-redundant backups"
        id = "CKV_AZURE_136"
        supported_resources = ['azurerm_postgresql_flexible_server']
        categories = [CheckCategories.BACKUP_AND_RECOVERY]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def get_inspected_key(self):
        return 'geo_redundant_backup_enabled'


check = PostgreSQLFlexiServerGeoBackupEnabled()
