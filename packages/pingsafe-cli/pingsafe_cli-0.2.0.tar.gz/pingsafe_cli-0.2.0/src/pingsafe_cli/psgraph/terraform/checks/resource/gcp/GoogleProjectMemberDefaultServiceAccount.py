from pingsafe_cli.psgraph.common.models.enums import CheckCategories
from pingsafe_cli.psgraph.terraform.checks.resource.gcp.AbsGoogleIAMMemberDefaultServiceAccount import AbsGoogleIAMMemberDefaultServiceAccount


class GoogleProjectMemberDefaultServiceAccount(AbsGoogleIAMMemberDefaultServiceAccount):
    def __init__(self) -> None:
        name = "Ensure Default Service account is not used at a project level"
        id = "CKV_GCP_46"
        supported_resources = ('google_project_iam_member', 'google_project_iam_binding')
        categories = (CheckCategories.IAM,)
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)


check = GoogleProjectMemberDefaultServiceAccount()
