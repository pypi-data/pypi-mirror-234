from __future__ import annotations

from typing import TYPE_CHECKING

from pingsafe_cli.psgraph.bicep.image_referencer.provider.azure import AzureBicepProvider
from pingsafe_cli.psgraph.common.images.graph.image_referencer_manager import GraphImageReferencerManager

if TYPE_CHECKING:
    from pingsafe_cli.psgraph.common.images.image_referencer import Image


class BicepImageReferencerManager(GraphImageReferencerManager):

    def extract_images_from_resources(self) -> list[Image]:
        bicep_provider = AzureBicepProvider(graph_connector=self.graph_connector)

        images = bicep_provider.extract_images_from_resources()

        return images
