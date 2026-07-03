"""Stage 4 step 03: build a dataset readiness report for ML handoff."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from scripts.python.common import ensure_parent_dir, read_json


DEFAULT_FEATURE_INVENTORY = "outputs/stage4/features/stage4_feature_inventory.json"
DEFAULT_OUTPUT = "outputs/stage4/handoff/stage4_dataset_readiness_report.json"


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for the Stage 4 readiness report."""
    parser = argparse.ArgumentParser(
        description="Build an ML-readiness report from the Stage 4 feature inventory."
    )
    parser.add_argument("--feature-inventory", default=DEFAULT_FEATURE_INVENTORY)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    return parser.parse_args()


def readiness_checks(inventory: dict[str, object]) -> list[dict[str, object]]:
    """Return explicit readiness checks from the feature inventory."""
    summary = inventory.get("summary", {})
    if not isinstance(summary, dict):
        summary = {}
    asset_count = int(summary.get("asset_count") or 0)
    complete_count = int(summary.get("complete_handoff_feature_asset_count") or 0)
    raw_count = int(summary.get("raw_pixel_signal_metric_asset_count") or 0)
    return [
        {
            "check": "cross_stage_feature_inventory_exists",
            "status": "pass" if inventory.get("status") == "complete" else "fail",
            "evidence": "Stage 4 feature inventory was generated.",
        },
        {
            "check": "asset_identity_contract_exists",
            "status": "pass"
            if int(summary.get("asset_identity_metadata_asset_count") or 0) > 0
            else "fail",
            "evidence": "Stage 1 assets provide the shared asset_key identity surface.",
        },
        {
            "check": "raw_signal_metrics_exist",
            "status": "pass" if raw_count == asset_count and asset_count > 0 else "review",
            "evidence": (
                f"{raw_count} of {asset_count} inventory assets have RAW pixel-signal metrics."
            ),
        },
        {
            "check": "complete_cross_stage_training_rows_exist",
            "status": "review" if complete_count > 0 else "fail",
            "evidence": (
                f"{complete_count} assets currently have all implemented feature families."
            ),
        },
        {
            "check": "sample_size_supports_model_training",
            "status": "fail",
            "evidence": (
                "Current asset counts are enough for schema validation and handoff design, "
                "not for credible model training."
            ),
        },
        {
            "check": "supervised_targets_exist",
            "status": "fail",
            "evidence": (
                "No accepted/rejected suggestions, editing-time records, final human ratings, "
                "or rendered before/after target dataset is materialized yet."
            ),
        },
    ]


def build_report(args: argparse.Namespace) -> dict[str, object]:
    """Build the dataset readiness report."""
    inventory = read_json(args.feature_inventory)
    summary = inventory.get("summary", {})
    if not isinstance(summary, dict):
        summary = {}
    checks = readiness_checks(inventory)
    blocking_checks = [check for check in checks if check["status"] == "fail"]
    review_checks = [check for check in checks if check["status"] == "review"]

    return {
        "stage": "stage4_ml_readiness_handoff",
        "status": "handoff_ready_model_training_not_ready",
        "pipeline_step": "03_build_dataset_readiness_report",
        "purpose": (
            "State honestly what the current artifacts can support: a structured "
            "handoff to an ML team, not a model-training claim."
        ),
        "inputs": {
            "feature_inventory": args.feature_inventory,
        },
        "readiness_summary": {
            "handoff_readiness": "ready_for_ml_team_discovery",
            "model_training_readiness": "not_ready",
            "reason": (
                "The repository has structured lineage, feature-family evidence, and "
                "RAW signal metrics, but it does not yet have enough labeled examples "
                "or target definitions for credible training."
            ),
            "asset_count": summary.get("asset_count"),
            "complete_handoff_feature_asset_count": summary.get(
                "complete_handoff_feature_asset_count"
            ),
        },
        "readiness_checks": checks,
        "blocking_modeling_gaps": [
            "small sample size",
            "missing accepted/rejected suggestion labels",
            "missing edit-time and intervention telemetry",
            "missing rendered before/after targets for visual-output learning",
            "limited cross-shoot and cross-lighting diversity",
            "no model-evaluation protocol or holdout split",
        ],
        "recommended_next_artifacts": [
            "stage4_rendered_before_after_manifest.json",
            "stage4_manual_review_labels.json",
            "stage4_edit_session_telemetry.json",
            "stage4_train_validation_split_manifest.json",
        ],
        "validation": {
            "status": "review_required" if blocking_checks else "validated",
            "blocking_check_count": len(blocking_checks),
            "review_check_count": len(review_checks),
        },
    }


def write_ordered_json(path: str | Path, payload: dict[str, object]) -> Path:
    """Write JSON while preserving semantic insertion order."""
    target = ensure_parent_dir(path)
    with target.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    return target


def main() -> None:
    """Generate the Stage 4 dataset readiness report."""
    args = parse_args()
    report = build_report(args)
    write_ordered_json(args.output, report)
    print(
        f"Wrote {args.output} with "
        f"{report['validation']['blocking_check_count']} blocking readiness checks."
    )


if __name__ == "__main__":
    main()
