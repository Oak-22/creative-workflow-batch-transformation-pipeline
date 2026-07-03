"""Stage 4 step 02: build a feature inventory across stage evidence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from scripts.python.common import ensure_parent_dir, read_json


DEFAULT_STAGE1_MANIFEST = "outputs/stage1/stage1_manifest.json"
DEFAULT_STAGE2_MANIFEST = "outputs/stage2/stage2_manifest.json"
DEFAULT_STAGE2_COMPARISON = (
    "outputs/stage2/comparisons/stage2_develop_parameter_comparison.json"
)
DEFAULT_STAGE3_MANIFEST = "outputs/stage3/stage3_manifest.json"
DEFAULT_STAGE3_CORE_COMPARISON = (
    "outputs/stage3/pipeline/stage3_mask_state_postmasking_no_local_adjustment_comparison.json"
)
DEFAULT_RAW_METRICS = "outputs/stage4/features/stage4_raw_pixel_signal_metrics.json"
DEFAULT_OUTPUT = "outputs/stage4/features/stage4_feature_inventory.json"


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for Stage 4 feature inventory generation."""
    parser = argparse.ArgumentParser(
        description="Build a cross-stage feature inventory for ML handoff review."
    )
    parser.add_argument("--stage1-manifest", default=DEFAULT_STAGE1_MANIFEST)
    parser.add_argument("--stage2-manifest", default=DEFAULT_STAGE2_MANIFEST)
    parser.add_argument("--stage2-comparison", default=DEFAULT_STAGE2_COMPARISON)
    parser.add_argument("--stage3-manifest", default=DEFAULT_STAGE3_MANIFEST)
    parser.add_argument(
        "--stage3-core-comparison", default=DEFAULT_STAGE3_CORE_COMPARISON
    )
    parser.add_argument("--raw-metrics", default=DEFAULT_RAW_METRICS)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    return parser.parse_args()


def asset_keys_from_records(payload: dict[str, object]) -> set[str]:
    """Return asset keys from a payload with top-level records."""
    records = payload.get("records", [])
    if not isinstance(records, list):
        return set()
    return {
        str(record.get("asset_key"))
        for record in records
        if isinstance(record, dict) and record.get("asset_key")
    }


def stage1_assets(stage1_manifest: dict[str, object]) -> dict[str, dict[str, object]]:
    """Return Stage 1 assets indexed by asset key."""
    assets = stage1_manifest.get("assets", [])
    if not isinstance(assets, list):
        return {}
    indexed = {}
    for asset in assets:
        if not isinstance(asset, dict) or not asset.get("asset_key"):
            continue
        indexed[str(asset["asset_key"])] = asset
    return indexed


def stage2_changed_settings(stage2_comparison: dict[str, object]) -> dict[str, int]:
    """Return changed setting counts by Stage 2 asset key."""
    records = stage2_comparison.get("records", [])
    if not isinstance(records, list):
        return {}
    return {
        str(record["asset_key"]): int(record.get("changed_setting_count") or 0)
        for record in records
        if isinstance(record, dict) and record.get("asset_key")
    }


def stage3_mask_counts(stage3_comparison: dict[str, object]) -> dict[str, dict[str, int]]:
    """Return postmasking mask counts by Stage 3 asset key."""
    records = stage3_comparison.get("records", [])
    if not isinstance(records, list):
        return {}
    counts = {}
    for record in records:
        if not isinstance(record, dict) or not record.get("asset_key"):
            continue
        postmasking = record.get("postmasking", {})
        if not isinstance(postmasking, dict):
            postmasking = {}
        counts[str(record["asset_key"])] = {
            "mask_group_count": int(postmasking.get("mask_group_count") or 0),
            "mask_entry_count": int(postmasking.get("mask_entry_count") or 0),
        }
    return counts


def raw_metric_summaries(raw_metrics: dict[str, object]) -> dict[str, dict[str, object]]:
    """Return compact RAW metric summaries by asset key."""
    records = raw_metrics.get("records", [])
    if not isinstance(records, list):
        return {}
    summaries = {}
    for record in records:
        if not isinstance(record, dict) or not record.get("asset_key"):
            continue
        read_coverage = record.get("read_coverage", {})
        rendered = record.get("rendered_preview_metrics", {})
        raw_mosaic = record.get("raw_mosaic_metrics", {})
        if not isinstance(read_coverage, dict):
            read_coverage = {}
        if not isinstance(rendered, dict):
            rendered = {}
        if not isinstance(raw_mosaic, dict):
            raw_mosaic = {}
        summaries[str(record["asset_key"])] = {
            "coverage_status": read_coverage.get("coverage_status"),
            "raw_visible_pixel_count": read_coverage.get("raw_visible_pixel_count"),
            "raw_visible_shape": read_coverage.get("raw_visible_shape"),
            "raw_full_sha256": read_coverage.get("raw_full_sha256"),
            "raw_visible_sha256": read_coverage.get("raw_visible_sha256"),
            "normalized_value_summary": raw_mosaic.get("normalized_value_summary", {}),
            "rendered_preview_luminance_summary": rendered.get(
                "luminance_summary", {}
            ),
            "rendered_preview_channel_cast_proxy_summaries": rendered.get(
                "channel_cast_proxy_summaries", {}
            ),
        }
    return summaries


def coverage_count(matrix: list[dict[str, object]], family_key: str) -> int:
    """Count assets where a feature family is present."""
    return sum(
        1
        for asset in matrix
        if isinstance(asset.get("feature_family_presence"), dict)
        and asset["feature_family_presence"].get(family_key)
    )


def build_feature_families(
    stage1_manifest: dict[str, object],
    stage2_manifest: dict[str, object],
    stage2_comparison: dict[str, object],
    stage3_manifest: dict[str, object],
    raw_metrics: dict[str, object],
    args: argparse.Namespace,
) -> list[dict[str, object]]:
    """Return stage-aware feature family descriptors."""
    stage2_summary = stage2_comparison.get("summary", {})
    raw_summary = raw_metrics.get("summary", {})
    stage3_summary = stage3_manifest.get("summary", {})
    if not isinstance(stage2_summary, dict):
        stage2_summary = {}
    if not isinstance(raw_summary, dict):
        raw_summary = {}
    if not isinstance(stage3_summary, dict):
        stage3_summary = {}
    return [
        {
            "feature_family": "asset_identity_metadata",
            "source_stage": "stage1",
            "artifact": args.stage1_manifest,
            "asset_count": stage1_manifest.get("summary", {}).get("asset_count"),
            "status": stage1_manifest.get("status"),
            "modeling_role": "asset identity, metadata state, and cohort context",
        },
        {
            "feature_family": "develop_parameter_deltas",
            "source_stage": "stage2",
            "artifact": args.stage2_comparison,
            "asset_count": stage2_summary.get("asset_count"),
            "changed_feature_count": stage2_summary.get("changed_develop_setting_count"),
            "status": stage2_manifest.get("status"),
            "modeling_role": "global edit transformation labels and parameter deltas",
        },
        {
            "feature_family": "semantic_local_mask_state",
            "source_stage": "stage3",
            "artifact": args.stage3_core_comparison,
            "asset_count": stage3_summary.get("core_asset_count"),
            "mask_group_count": stage3_summary.get("core_mask_group_count"),
            "mask_entry_count": stage3_summary.get("core_mask_entry_count"),
            "status": stage3_manifest.get("status"),
            "modeling_role": "semantic region availability and local-edit structure",
        },
        {
            "feature_family": "raw_pixel_signal_metrics",
            "source_stage": "stage4",
            "artifact": args.raw_metrics,
            "asset_count": raw_summary.get("asset_count"),
            "complete_coverage_asset_count": raw_summary.get(
                "complete_coverage_asset_count"
            ),
            "status": raw_metrics.get("status"),
            "modeling_role": "source-image signal summaries and decoded-read provenance",
        },
    ]


def build_inventory(args: argparse.Namespace) -> dict[str, object]:
    """Build the Stage 4 feature inventory payload."""
    stage1_manifest = read_json(args.stage1_manifest)
    stage2_manifest = read_json(args.stage2_manifest)
    stage2_comparison = read_json(args.stage2_comparison)
    stage3_manifest = read_json(args.stage3_manifest)
    stage3_comparison = read_json(args.stage3_core_comparison)
    raw_metrics = read_json(args.raw_metrics)

    stage1_by_asset = stage1_assets(stage1_manifest)
    stage2_by_asset = stage2_changed_settings(stage2_comparison)
    stage3_by_asset = stage3_mask_counts(stage3_comparison)
    raw_by_asset = raw_metric_summaries(raw_metrics)
    asset_keys = sorted(
        set(stage1_by_asset) | set(stage2_by_asset) | set(stage3_by_asset) | set(raw_by_asset)
    )

    asset_matrix = []
    for asset_key in asset_keys:
        stage1_asset = stage1_by_asset.get(asset_key, {})
        raw_summary = raw_by_asset.get(asset_key, {})
        presence = {
            "asset_identity_metadata": asset_key in stage1_by_asset,
            "develop_parameter_deltas": asset_key in stage2_by_asset,
            "semantic_local_mask_state": asset_key in stage3_by_asset,
            "raw_pixel_signal_metrics": asset_key in raw_by_asset,
        }
        asset_matrix.append(
            {
                "asset_key": asset_key,
                "feature_family_presence": presence,
                "complete_handoff_feature_set": all(presence.values()),
                "stage1_metadata_state": stage1_asset.get("metadata_state"),
                "stage1_source_summary": stage1_asset.get("source_summary", {}),
                "stage2_changed_setting_count": stage2_by_asset.get(asset_key),
                "stage3_mask_counts": stage3_by_asset.get(asset_key),
                "stage4_raw_metric_summary": raw_summary,
            }
        )

    return {
        "stage": "stage4_ml_readiness_handoff",
        "status": "complete",
        "pipeline_step": "02_build_feature_inventory",
        "purpose": (
            "Inventory the feature families currently materialized by Stages 1-4 "
            "so a downstream ML team can see what evidence exists before model "
            "training is proposed."
        ),
        "inputs": {
            "stage1_manifest": args.stage1_manifest,
            "stage2_manifest": args.stage2_manifest,
            "stage2_comparison": args.stage2_comparison,
            "stage3_manifest": args.stage3_manifest,
            "stage3_core_comparison": args.stage3_core_comparison,
            "raw_pixel_signal_metrics": args.raw_metrics,
        },
        "feature_families": build_feature_families(
            stage1_manifest,
            stage2_manifest,
            stage2_comparison,
            stage3_manifest,
            raw_metrics,
            args,
        ),
        "summary": {
            "asset_count": len(asset_matrix),
            "complete_handoff_feature_asset_count": sum(
                1 for asset in asset_matrix if asset["complete_handoff_feature_set"]
            ),
            "asset_identity_metadata_asset_count": coverage_count(
                asset_matrix, "asset_identity_metadata"
            ),
            "develop_parameter_delta_asset_count": coverage_count(
                asset_matrix, "develop_parameter_deltas"
            ),
            "semantic_local_mask_state_asset_count": coverage_count(
                asset_matrix, "semantic_local_mask_state"
            ),
            "raw_pixel_signal_metric_asset_count": coverage_count(
                asset_matrix, "raw_pixel_signal_metrics"
            ),
        },
        "asset_feature_matrix": asset_matrix,
    }


def write_ordered_json(path: str | Path, payload: dict[str, object]) -> Path:
    """Write JSON while preserving semantic insertion order."""
    target = ensure_parent_dir(path)
    with target.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    return target


def main() -> None:
    """Generate the Stage 4 feature inventory artifact."""
    args = parse_args()
    inventory = build_inventory(args)
    write_ordered_json(args.output, inventory)
    print(
        f"Wrote {args.output} with "
        f"{inventory['summary']['asset_count']} assets and "
        f"{inventory['summary']['complete_handoff_feature_asset_count']} complete handoff feature sets."
    )


if __name__ == "__main__":
    main()
