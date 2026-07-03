"""Stage 4 step 05: build a compact manifest from ML handoff artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from scripts.python.common import ensure_parent_dir, read_json


DEFAULT_RAW_METRICS = "outputs/stage4/features/stage4_raw_pixel_signal_metrics.json"
DEFAULT_FEATURE_INVENTORY = "outputs/stage4/features/stage4_feature_inventory.json"
DEFAULT_READINESS_REPORT = "outputs/stage4/handoff/stage4_dataset_readiness_report.json"
DEFAULT_HANDOFF_CONTRACT = "outputs/stage4/handoff/stage4_ml_handoff_contract.json"
DEFAULT_OUTPUT = "outputs/stage4/stage4_manifest.json"


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for Stage 4 manifest generation."""
    parser = argparse.ArgumentParser(
        description="Build a compact Stage 4 manifest from ML handoff artifacts."
    )
    parser.add_argument("--raw-metrics", default=DEFAULT_RAW_METRICS)
    parser.add_argument("--feature-inventory", default=DEFAULT_FEATURE_INVENTORY)
    parser.add_argument("--readiness-report", default=DEFAULT_READINESS_REPORT)
    parser.add_argument("--handoff-contract", default=DEFAULT_HANDOFF_CONTRACT)
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
    """Return generated Stage 4 artifacts in expected production order."""
    return [
        {
            "order": 1,
            "role": "raw_pixel_signal_metrics",
            "produced_by": "scripts/python/stage4/01_extract_pixel_signal_metrics.py",
            "artifact": artifact_ref(args.raw_metrics),
        },
        {
            "order": 2,
            "role": "feature_inventory",
            "produced_by": "scripts/python/stage4/02_build_feature_inventory.py",
            "artifact": artifact_ref(args.feature_inventory),
        },
        {
            "order": 3,
            "role": "dataset_readiness_report",
            "produced_by": "scripts/python/stage4/03_build_dataset_readiness_report.py",
            "artifact": artifact_ref(args.readiness_report),
        },
        {
            "order": 4,
            "role": "ml_handoff_contract",
            "produced_by": "scripts/python/stage4/04_build_ml_handoff_contract.py",
            "artifact": artifact_ref(args.handoff_contract),
        },
    ]


def validation_status(readiness_report: dict[str, object]) -> dict[str, object]:
    """Return Stage 4 validation status from the readiness report."""
    validation = readiness_report.get("validation", {})
    readiness_summary = readiness_report.get("summary", {})
    if not isinstance(validation, dict):
        validation = {}
    if not isinstance(readiness_summary, dict):
        readiness_summary = {}
    return {
        "status": "validated_for_handoff",
        "dataset_readiness_status": readiness_report.get("status"),
        "handoff_readiness": readiness_summary.get("handoff_readiness"),
        "model_training_readiness": readiness_summary.get(
            "model_training_readiness"
        ),
        "blocking_readiness_check_count": validation.get("blocking_check_count"),
        "blocking_modeling_gap_count": len(
            readiness_report.get("blocking_modeling_gaps", [])
        ),
    }


def build_manifest(args: argparse.Namespace) -> dict[str, object]:
    """Build the stable Stage 4 manifest payload."""
    inventory = read_json(args.feature_inventory)
    readiness_report = read_json(args.readiness_report)
    handoff_contract = read_json(args.handoff_contract)
    validation = validation_status(readiness_report)
    inventory_summary = inventory.get("summary", {})
    if not isinstance(inventory_summary, dict):
        inventory_summary = {}
    return {
        "stage": "stage4_ml_readiness_handoff",
        "status": validation["status"],
        "summary": {
            "asset_count": inventory_summary.get("asset_count"),
            "complete_handoff_feature_asset_count": inventory_summary.get(
                "complete_handoff_feature_asset_count"
            ),
            "feature_family_count": len(inventory.get("feature_families", [])),
            "handoff_claim_count": len(handoff_contract.get("approved_claims", [])),
            "non_claim_count": len(handoff_contract.get("non_claims", [])),
        },
        "pipeline_step": "05_build_stage4_manifest",
        "purpose": (
            "Compact index for Stage 4 generated evidence. This manifest frames "
            "Stage 4 as an ML-readiness handoff package, not as a model-training result."
        ),
        "upstream_stage_manifests": [
            "outputs/stage1/stage1_manifest.json",
            "outputs/stage2/stage2_manifest.json",
            "outputs/stage3/stage3_manifest.json",
        ],
        "validation": validation,
        "artifact_sequence": artifact_sequence(args),
    }


def write_ordered_json(path: str | Path, payload: dict[str, object]) -> Path:
    """Write JSON while preserving semantic insertion order."""
    target = ensure_parent_dir(path)
    with target.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    return target


def main() -> None:
    """Generate the Stage 4 manifest artifact."""
    args = parse_args()
    manifest = build_manifest(args)
    write_ordered_json(args.output, manifest)
    print(
        f"Wrote {args.output} with "
        f"{len(manifest['artifact_sequence'])} referenced artifacts."
    )


if __name__ == "__main__":
    main()
