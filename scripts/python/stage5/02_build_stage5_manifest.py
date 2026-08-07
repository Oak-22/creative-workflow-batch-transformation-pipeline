"""Stage 5 step 02: build a compact manifest from serving exports."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from scripts.python.common import ensure_parent_dir, read_json


DEFAULT_ASSET_SUMMARY = "outputs/stage5/exports/stage5_asset_summary.json"
DEFAULT_FEATURE_FAMILY_SUMMARY = "outputs/stage5/exports/stage5_feature_family_summary.json"
DEFAULT_ARTIFACT_CATALOG = "outputs/stage5/exports/stage5_artifact_catalog.json"
DEFAULT_OUTPUT = "outputs/stage5/stage5_manifest.json"


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for Stage 5 manifest generation."""
    parser = argparse.ArgumentParser(
        description="Build a compact Stage 5 manifest from serving exports."
    )
    parser.add_argument("--asset-summary", default=DEFAULT_ASSET_SUMMARY)
    parser.add_argument(
        "--feature-family-summary",
        default=DEFAULT_FEATURE_FAMILY_SUMMARY,
    )
    parser.add_argument("--artifact-catalog", default=DEFAULT_ARTIFACT_CATALOG)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    """Calculate a SHA-256 digest for one local artifact."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_ref(path: str | Path) -> dict[str, object]:
    """Return a compact reference for a local artifact path."""
    artifact_path = Path(path)
    if not artifact_path.is_file():
        raise SystemExit(f"Required artifact not found: {artifact_path}")
    return {
        "path": str(artifact_path),
        "sha256": sha256_file(artifact_path),
        "size_bytes": artifact_path.stat().st_size,
    }


def export_sequence(args: argparse.Namespace) -> list[dict[str, object]]:
    """Return generated Stage 5 exports in production order."""
    return [
        {
            "order": 1,
            "role": "asset_summary_export",
            "produced_by": "scripts/python/stage5/01_build_serving_exports.py",
            "artifact": artifact_ref(args.asset_summary),
        },
        {
            "order": 2,
            "role": "feature_family_summary_export",
            "produced_by": "scripts/python/stage5/01_build_serving_exports.py",
            "artifact": artifact_ref(args.feature_family_summary),
        },
        {
            "order": 3,
            "role": "artifact_catalog_export",
            "produced_by": "scripts/python/stage5/01_build_serving_exports.py",
            "artifact": artifact_ref(args.artifact_catalog),
        },
    ]


def build_manifest(args: argparse.Namespace) -> dict[str, object]:
    """Build the stable Stage 5 manifest payload."""
    asset_summary = read_json(args.asset_summary)
    feature_family_summary = read_json(args.feature_family_summary)
    artifact_catalog = read_json(args.artifact_catalog)
    asset_summary_summary = asset_summary.get("summary", {})
    feature_family_summary_summary = feature_family_summary.get("summary", {})
    artifact_catalog_summary = artifact_catalog.get("summary", {})
    if not isinstance(asset_summary_summary, dict):
        asset_summary_summary = {}
    if not isinstance(feature_family_summary_summary, dict):
        feature_family_summary_summary = {}
    if not isinstance(artifact_catalog_summary, dict):
        artifact_catalog_summary = {}
    return {
        "stage": "stage5_operational_serving_exports",
        "status": "complete",
        "summary": {
            "asset_count": asset_summary_summary.get("asset_count"),
            "rendered_target_asset_count": asset_summary_summary.get(
                "rendered_target_asset_count"
            ),
            "feature_family_count": feature_family_summary_summary.get(
                "feature_family_count"
            ),
            "artifact_count": artifact_catalog_summary.get("artifact_count"),
            "consumer_count": asset_summary_summary.get("consumer_count"),
        },
        "pipeline_step": "02_build_stage5_manifest",
        "purpose": (
            "Compact index for Stage 5 serving exports. Stage 5 produces "
            "file-based exports; database tables and views belong to a later "
            "infrastructure layer."
        ),
        "consumers": asset_summary.get("consumers", []),
        "upstream_stage_manifests": [
            "outputs/stage1/stage1_manifest.json",
            "outputs/stage2/stage2_manifest.json",
            "outputs/stage3/stage3_manifest.json",
            "outputs/stage4/stage4_manifest.json",
        ],
        "export_sequence": export_sequence(args),
    }


def write_ordered_json(path: str | Path, payload: dict[str, object]) -> Path:
    """Write JSON while preserving insertion order."""
    target = ensure_parent_dir(path)
    with target.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    return target


def main() -> None:
    """Generate the Stage 5 manifest."""
    args = parse_args()
    manifest = build_manifest(args)
    write_ordered_json(args.output, manifest)
    print(
        f"Wrote {args.output} with "
        f"{len(manifest['export_sequence'])} serving exports."
    )


if __name__ == "__main__":
    main()
