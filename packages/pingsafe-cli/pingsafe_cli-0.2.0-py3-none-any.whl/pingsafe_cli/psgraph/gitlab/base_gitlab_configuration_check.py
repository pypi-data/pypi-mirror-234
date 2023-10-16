from __future__ import annotations

from typing import Iterable

from pingsafe_cli.psgraph.common.checks.base_check import BaseCheck
from pingsafe_cli.psgraph.common.models.enums import CheckCategories

from pingsafe_cli.psgraph.gitlab.registry import registry


class BaseGitlabCheck(BaseCheck):
    def __init__(self, name: str, id: str, categories: Iterable[CheckCategories], supported_entities: list[str],
                 block_type: str, path: str | None = None, guideline: str | None = None) -> None:
        super().__init__(
            name=name,
            id=id,
            categories=categories,
            supported_entities=supported_entities,
            block_type=block_type,
            guideline=guideline,
        )
        self.path = path
        registry.register(self)
