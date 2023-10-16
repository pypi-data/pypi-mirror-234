from __future__ import annotations

from typing import Any

from pingsafe_cli.psgraph.azure_pipelines.image_referencer.provider import AzurePipelinesProvider
from pingsafe_cli.psgraph.common.images.workflow.image_referencer_manager import WorkflowImageReferencerManager


class AzurePipelinesImageReferencerManager(WorkflowImageReferencerManager):

    def __init__(self, workflow_config: dict[str, Any], file_path: str):
        provider = AzurePipelinesProvider(workflow_config=workflow_config, file_path=file_path)
        super().__init__(workflow_config, file_path, provider)
