"""Shared filesystem and serialization helpers for workflow scripts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def ensure_parent_dir(path: str | Path) -> Path:
    """Create the parent directory for a file path if needed."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


def read_json(path: str | Path) -> Any:
    """Read JSON from disk and return the decoded object."""
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: str | Path, payload: Any) -> Path:
    """Write JSON to disk with stable formatting."""
    target = ensure_parent_dir(path)
    with target.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
    return target

