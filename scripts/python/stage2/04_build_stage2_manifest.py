"""Stage 2 step 04: build a compact manifest from conditioning artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from scripts.python.common import ensure_parent_dir, read_json


DEFAULT_PRECONDITIONING_CHECKPOINT_MANIFEST = (
    "outputs/stage2/stage2_preconditioning_checkpoint_manifest.json"
)
DEFAULT_POSTCONDITIONING_CHECKPOINT_MANIFEST = (
    "outputs/stage2/stage2_postconditioning_checkpoint_manifest.json"
)
DEFAULT_PRECONDITIONING_EXTRACT = (
    "outputs/stage2/stage2_extracted_preconditioning_develop_settings.json"
)
DEFAULT_POSTCONDITIONING_EXTRACT = (
    "outputs/stage2/stage2_extracted_postconditioning_develop_settings.json"
)
DEFAULT_COMPARISON = "outputs/stage2/stage2_develop_parameter_comparison.json"
DEFAULT_OUTPUT = "outputs/stage2/stage2_manifest.json"


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for Stage 2 manifest generation."""
    parser = argparse.ArgumentParser(
        description="Build a compact Stage 2 manifest from generated artifacts."
    )
    parser.add_argument(
        "--preconditioning-checkpoint-manifest",
        default=DEFAULT_PRECONDITIONING_CHECKPOINT_MANIFEST,
        help="Hash manifest for the frozen Stage 2 preconditioning checkpoint.",
    )
    parser.add_argument(
        "--postconditioning-checkpoint-manifest",
        default=DEFAULT_POSTCONDITIONING_CHECKPOINT_MANIFEST,
        help="Hash manifest for the frozen Stage 2 postconditioning checkpoint.",
    )
    parser.add_argument(
        "--preconditioning-extract",
        default=DEFAULT_PRECONDITIONING_EXTRACT,
        help="Develop-setting extract for the frozen preconditioning checkpoint.",
    )
    parser.add_argument(
        "--postconditioning-extract",
        default=DEFAULT_POSTCONDITIONING_EXTRACT,
        help="Develop-setting extract for the frozen postconditioning checkpoint.",
    )
    parser.add_argument(
        "--comparison",
        default=DEFAULT_COMPARISON,
        help="Stage 2 pre/post Develop-setting comparison artifact.",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help="Destination Stage 2 manifest JSON.",
    )
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    """Calculate a SHA-256 digest for one local artifact."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_ref(path: str | Path) -> dict[str, object]:
    """Return a compact, verifiable reference to a generated artifact."""
    artifact_path = Path(path)
    if not artifact_path.is_file():
        raise SystemExit(f"Required artifact not found: {artifact_path}")
    return {
        "path": str(artifact_path),
        "sha256": sha256_file(artifact_path),
        "size_bytes": artifact_path.stat().st_size,
    }


def artifact_sequence(args: argparse.Namespace) -> list[dict[str, object]]:
    """Return generated Stage 2 artifacts in expected production order."""
    return [
        {
            "order": 1,
            "role": "preconditioning_checkpoint_manifest",
            "produced_by": "scripts/python/stage2/01_build_checkpoint_manifest.py",
            "artifact": artifact_ref(args.preconditioning_checkpoint_manifest),
        },
        {
            "order": 2,
            "role": "preconditioning_develop_settings_extract",
            "produced_by": "scripts/python/stage2/02_extract_develop_settings.py",
            "artifact": artifact_ref(args.preconditioning_extract),
        },
        {
            "order": 3,
            "role": "postconditioning_checkpoint_manifest",
            "produced_by": "scripts/python/stage2/01_build_checkpoint_manifest.py",
            "artifact": artifact_ref(args.postconditioning_checkpoint_manifest),
        },
        {
            "order": 4,
            "role": "postconditioning_develop_settings_extract",
            "produced_by": "scripts/python/stage2/02_extract_develop_settings.py",
            "artifact": artifact_ref(args.postconditioning_extract),
        },
        {
            "order": 5,
            "role": "develop_parameter_comparison",
            "produced_by": "scripts/python/stage2/03_audit_stage2_parameters.py",
            "artifact": artifact_ref(args.comparison),
        },
    ]


def build_summary(
    pre_manifest: dict[str, object],
    post_manifest: dict[str, object],
    comparison: dict[str, object],
) -> dict[str, object]:
    """Build the compact Stage 2 summary from upstream artifact summaries."""
    comparison_summary = comparison.get("summary", {})
    pre_summary = pre_manifest.get("summary", {})
    post_summary = post_manifest.get("summary", {})
    if not isinstance(comparison_summary, dict):
        comparison_summary = {}
    if not isinstance(pre_summary, dict):
        pre_summary = {}
    if not isinstance(post_summary, dict):
        post_summary = {}

    return {
        "asset_count": comparison_summary.get("asset_count"),
        "changed_asset_count": comparison_summary.get("changed_asset_count"),
        "unchanged_asset_count": comparison_summary.get("unchanged_asset_count"),
        "changed_develop_setting_count": comparison_summary.get(
            "changed_develop_setting_count"
        ),
        "changed_develop_settings": comparison_summary.get(
            "changed_develop_settings", []
        ),
        "preconditioning_checkpoint_artifact_count": pre_summary.get(
            "artifact_count"
        ),
        "postconditioning_checkpoint_artifact_count": post_summary.get(
            "artifact_count"
        ),
        "preconditioning_checkpoint_matches_live_count": pre_summary.get(
            "matching_mutable_origin_count_at_manifest_time"
        ),
        "postconditioning_checkpoint_matches_live_count": post_summary.get(
            "matching_mutable_origin_count_at_manifest_time"
        ),
    }


def validation_status(
    pre_manifest: dict[str, object],
    post_manifest: dict[str, object],
    comparison: dict[str, object],
) -> dict[str, object]:
    """Return manifest validation status derived from upstream summaries."""
    comparison_summary = comparison.get("summary", {})
    pre_summary = pre_manifest.get("summary", {})
    post_summary = post_manifest.get("summary", {})
    if not isinstance(comparison_summary, dict):
        comparison_summary = {}
    if not isinstance(pre_summary, dict):
        pre_summary = {}
    if not isinstance(post_summary, dict):
        post_summary = {}

    asset_count = comparison_summary.get("asset_count")
    pre_count = pre_summary.get("artifact_count")
    post_count = post_summary.get("artifact_count")
    missing_count = int(comparison_summary.get("missing_preconditioning_asset_count") or 0)
    missing_count += int(comparison_summary.get("missing_postconditioning_asset_count") or 0)
    checkpoint_counts_match = pre_count == asset_count and post_count == asset_count
    comparison_complete = comparison.get("status") == "complete"
    status = (
        "validated"
        if comparison_complete and checkpoint_counts_match and missing_count == 0
        else "review_required"
    )
    return {
        "status": status,
        "comparison_status": comparison.get("status"),
        "checkpoint_counts_match_comparison_asset_count": checkpoint_counts_match,
        "missing_compared_asset_count": missing_count,
    }


def build_manifest(args: argparse.Namespace) -> dict[str, object]:
    """Build the stable Stage 2 manifest payload."""
    pre_manifest = read_json(args.preconditioning_checkpoint_manifest)
    post_manifest = read_json(args.postconditioning_checkpoint_manifest)
    comparison = read_json(args.comparison)
    validation = validation_status(pre_manifest, post_manifest, comparison)
    return {
        "stage": "stage2_baseline_conditioning",
        "status": validation["status"],
        "pipeline_step": "04_build_stage2_manifest",
        "purpose": (
            "Compact index for Stage 2 generated evidence. This manifest "
            "references checkpoint manifests, Develop-setting extracts, and "
            "the final pre/post Develop comparison without duplicating their "
            "verbose records."
        ),
        "artifact_sequence": artifact_sequence(args),
        "validation": validation,
        "summary": build_summary(pre_manifest, post_manifest, comparison),
    }


def write_ordered_json(path: str | Path, payload: dict[str, object]) -> Path:
    """Write JSON while preserving semantic insertion order."""
    target = ensure_parent_dir(path)
    with target.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    return target


def main() -> None:
    """Generate the Stage 2 manifest artifact."""
    args = parse_args()
    manifest = build_manifest(args)
    write_ordered_json(args.output, manifest)
    print(
        f"Wrote {args.output} with "
        f"{len(manifest['artifact_sequence'])} referenced artifacts."
    )


if __name__ == "__main__":
    main()
