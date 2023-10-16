#
# No change required normally except to possibly switch it to json
# eg. from pingsafe_cli.psgraph.json_doc.base_registry import Registry
#
from pingsafe_cli.psgraph.common.pingsafe.check_type import CheckType
from pingsafe_cli.psgraph.yaml_doc.base_registry import Registry

registry = Registry(CheckType.YAML)
