import os
from typing import List
from pingsafe_cli.psgraph.common.runners.base_runner import strtobool

PATH_SEPARATOR = "->"


def unify_dependency_path(dependency_path: List[str]) -> str:
    if not dependency_path:
        return ''
    if strtobool(os.getenv('PINGSAFE_ENABLE_NESTED_MODULES', 'True')):
        return dependency_path[-1]
    return PATH_SEPARATOR.join(dependency_path)
