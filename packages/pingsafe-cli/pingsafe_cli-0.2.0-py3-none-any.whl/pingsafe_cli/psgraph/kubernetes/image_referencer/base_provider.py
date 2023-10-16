from __future__ import annotations

import os
from typing import Any

from pingsafe_cli.psgraph.common.graph.graph_builder import CustomAttributes
from pingsafe_cli.psgraph.common.images.graph.image_referencer_provider import GraphImageReferencerProvider
from pingsafe_cli.psgraph.common.images.image_referencer import Image
from pingsafe_cli.psgraph.common.util.consts import START_LINE, END_LINE
from pingsafe_cli.psgraph.common.util.str_utils import removeprefix


class BaseKubernetesProvider(GraphImageReferencerProvider):

    def extract_images_from_resources(self) -> list[Image]:
        images = []

        supported_resources_graph = self.extract_nodes()

        for resource in self.extract_resource(supported_resources_graph):
            resource_type = resource[CustomAttributes.RESOURCE_TYPE]
            resource_path = self._get_resource_path(resource)

            extract_images_func = self.supported_resource_types.get(resource_type)
            if extract_images_func:
                for name in extract_images_func(resource):
                    images.append(
                        Image(
                            file_path=resource_path,
                            name=name,
                            start_line=resource[START_LINE],
                            end_line=resource[END_LINE],
                            related_resource_id=f'{removeprefix(resource_path, os.getenv("BC_ROOT_DIR", ""))}:{resource.get("id_")}',
                        )
                    )

        return images

    def _get_resource_path(self, resource: dict[str, Any]) -> str:
        return resource.get(CustomAttributes.FILE_PATH, "")
