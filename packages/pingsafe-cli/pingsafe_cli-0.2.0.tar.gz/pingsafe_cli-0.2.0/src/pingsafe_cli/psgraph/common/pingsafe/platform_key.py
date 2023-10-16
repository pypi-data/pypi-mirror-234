from __future__ import annotations

import os

from pathlib import Path

home = str(Path.home())
pingsafe_dir = f"{home}/.pingsafe"
pingsafe_file = f"{pingsafe_dir}/credentials"


def persist_key(key: str) -> None:
    if not os.path.exists(pingsafe_dir):
        os.makedirs(pingsafe_dir)
    with open(pingsafe_file, "w") as f:
        f.write(key)


def read_key() -> str | None:
    key = None
    if os.path.exists(pingsafe_file):
        with open(pingsafe_file, "r") as f:
            key = f.readline()
    return key
