from pingsafe_cli.psgraph.common.models.enums import CheckCategories
from pingsafe_cli.psgraph.terraform.checks.resource.gcp.AbsGoogleIAMMemberDefaultServiceAccount import AbsGoogleIAMMemberDefaultServiceAccount


class GoogleOrgMemberDefaultServiceAccount(AbsGoogleIAMMemberDefaultServiceAccount):
    def __init__(self) -> None:
        name = "Ensure default service account is not used at an organization level"
        id = "CKV_GCP_47"
        supported_resources = ('google_organization_iam_member', 'google_organization_iam_binding')
        categories = (CheckCategories.IAM,)
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)


check = GoogleOrgMemberDefaultServiceAccount()
