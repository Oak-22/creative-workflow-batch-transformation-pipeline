"""Stage 5 step 01: build operational serving exports from stage evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from scripts.python.common import ensure_parent_dir, read_json


DEFAULT_STAGE1_MANIFEST = "outputs/stage1/stage1_manifest.json"
DEFAULT_STAGE2_MANIFEST = "outputs/stage2/stage2_manifest.json"
DEFAULT_STAGE3_MANIFEST = "outputs/stage3/stage3_manifest.json"
DEFAULT_STAGE4_MANIFEST = "outputs/stage4/stage4_manifest.json"
DEFAULT_FEATURE_INVENTORY = "outputs/stage4/features/stage4_feature_inventory.json"
DEFAULT_READINESS_REPORT = "outputs/stage4/handoff/stage4_dataset_readiness_report.json"
DEFAULT_HANDOFF_CONTRACT = "outputs/stage4/handoff/stage4_ml_handoff_contract.json"
DEFAULT_RENDERED_TARGET_ROOT = "data/stage4/rendered_targets/lightroom_jpeg_exports"
DEFAULT_EXPORT_DIR = "outputs/stage5/exports"


CONSUMERS = [
    {
        "consumer": "ml_data_science_team",
        "decision_surface": "feature sufficiency, target definition, and modeling feasibility",
    },
    {
        "consumer": "business_operations_stakeholder",
        "decision_surface": "readiness, workflow leverage, and operational impact",
    },
    {
        "consumer": "audit_compliance_governance_stakeholder",
        "decision_surface": "provenance, claims, non-claims, and reproducibility",
    },
]


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for Stage 5 serving export generation."""
    parser = argparse.ArgumentParser(
        description="Build compact Stage 5 serving exports from Stage 1-4 artifacts."
    )
    parser.add_argument("--stage1-manifest", default=DEFAULT_STAGE1_MANIFEST)
    parser.add_argument("--stage2-manifest", default=DEFAULT_STAGE2_MANIFEST)
    parser.add_argument("--stage3-manifest", default=DEFAULT_STAGE3_MANIFEST)
    parser.add_argument("--stage4-manifest", default=DEFAULT_STAGE4_MANIFEST)
    parser.add_argument("--feature-inventory", default=DEFAULT_FEATURE_INVENTORY)
    parser.add_argument("--readiness-report", default=DEFAULT_READINESS_REPORT)
    parser.add_argument("--handoff-contract", default=DEFAULT_HANDOFF_CONTRACT)
    parser.add_argument("--rendered-target-root", default=DEFAULT_RENDERED_TARGET_ROOT)
    parser.add_argument("--export-dir", default=DEFAULT_EXPORT_DIR)
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


def optional_artifact_ref(path: str | Path) -> dict[str, object] | None:
    """Return an artifact reference when the artifact exists."""
    artifact_path = Path(path)
    if not artifact_path.is_file():
        return None
    return artifact_ref(artifact_path)


def write_ordered_json(path: str | Path, payload: dict[str, object]) -> Path:
    """Write JSON while preserving insertion order."""
    target = ensure_parent_dir(path)
    with target.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    return target


def asset_summary_records(
    feature_inventory: dict[str, object],
    rendered_target_root: Path,
) -> list[dict[str, object]]:
    """Build one compact operational summary row per asset."""
    records = []
    for asset in feature_inventory.get("asset_feature_matrix", []):
        if not isinstance(asset, dict) or not asset.get("asset_key"):
            continue
        asset_key = str(asset["asset_key"])
        rendered_target = optional_artifact_ref(rendered_target_root / f"{asset_key}.jpg")
        feature_presence = asset.get("feature_family_presence", {})
        if not isinstance(feature_presence, dict):
            feature_presence = {}
        asset_context = asset.get("asset_context", {})
        if not isinstance(asset_context, dict):
            asset_context = {}
        raw_metric_summary = asset.get("stage4_raw_metric_summary", {})
        if not isinstance(raw_metric_summary, dict):
            raw_metric_summary = {}
        records.append(
            {
                "asset_key": asset_key,
                "summary": {
                    "complete_handoff_feature_set": asset.get(
                        "complete_handoff_feature_set"
                    ),
                    "rendered_target_present": rendered_target is not None,
                },
                "asset_context": {
                    "present": bool(asset_context.get("present")),
                    "metadata_state": asset_context.get("metadata_state"),
                    "source_summary": asset_context.get("source_summary", {}),
                },
                "feature_family_presence": {
                    "develop_parameter_deltas": bool(
                        feature_presence.get("develop_parameter_deltas")
                    ),
                    "semantic_local_mask_state": bool(
                        feature_presence.get("semantic_local_mask_state")
                    ),
                    "raw_pixel_signal_metrics": bool(
                        feature_presence.get("raw_pixel_signal_metrics")
                    ),
                },
                "supporting_evidence": {
                    "stage2_changed_setting_count": asset.get(
                        "stage2_changed_setting_count"
                    ),
                    "stage3_mask_counts": asset.get("stage3_mask_counts"),
                    "stage4_raw_metric_summary": {
                        "coverage_status": raw_metric_summary.get("coverage_status"),
                        "raw_visible_pixel_count": raw_metric_summary.get(
                            "raw_visible_pixel_count"
                        ),
                        "raw_visible_shape": raw_metric_summary.get(
                            "raw_visible_shape"
                        ),
                        "raw_full_sha256": raw_metric_summary.get("raw_full_sha256"),
                        "raw_visible_sha256": raw_metric_summary.get(
                            "raw_visible_sha256"
                        ),
                    },
                    "rendered_target_artifact": rendered_target,
                },
            }
        )
    return records


def build_asset_summary(args: argparse.Namespace, feature_inventory: dict[str, object]) -> dict[str, object]:
    """Build the Stage 5 asset serving export."""
    records = asset_summary_records(feature_inventory, Path(args.rendered_target_root))
    rendered_count = sum(
        1
        for record in records
        if record["summary"].get("rendered_target_present")
    )
    complete_count = sum(
        1
        for record in records
        if record["summary"].get("complete_handoff_feature_set")
    )
    return {
        "stage": "stage5_operational_serving_exports",
        "status": "complete",
        "summary": {
            "asset_count": len(records),
            "complete_handoff_feature_asset_count": complete_count,
            "rendered_target_asset_count": rendered_count,
            "consumer_count": len(CONSUMERS),
        },
        "pipeline_step": "01_build_serving_exports",
        "purpose": "Asset-level serving export for operational consumers.",
        "consumers": CONSUMERS,
        "inputs": {
            "feature_inventory": args.feature_inventory,
            "rendered_target_root": args.rendered_target_root,
        },
        "records": records,
    }


def feature_family_records(feature_inventory: dict[str, object]) -> list[dict[str, object]]:
    """Build one serving row per feature family."""
    records = []
    for family in feature_inventory.get("feature_families", []):
        if not isinstance(family, dict):
            continue
        artifact_refs = []
        for key in ("artifact", "mask_definition_artifact", "mask_edit_artifact"):
            path = family.get(key)
            if path:
                artifact_refs.append({"role": key, "path": path})
        records.append(
            {
                "feature_family": family.get("feature_family"),
                "source_stage": family.get("source_stage"),
                "summary": {
                    "asset_count": family.get("asset_count"),
                    "status": family.get("status"),
                    "modeling_role": family.get("modeling_role"),
                },
                "artifact_refs": artifact_refs,
            }
        )
    return records


def build_feature_family_summary(
    args: argparse.Namespace,
    feature_inventory: dict[str, object],
) -> dict[str, object]:
    """Build the Stage 5 feature-family serving export."""
    records = feature_family_records(feature_inventory)
    return {
        "stage": "stage5_operational_serving_exports",
        "status": "complete",
        "summary": {
            "feature_family_count": len(records),
            "consumer_count": len(CONSUMERS),
        },
        "pipeline_step": "01_build_serving_exports",
        "purpose": "Feature-family serving export for operational consumers.",
        "consumers": CONSUMERS,
        "inputs": {
            "feature_inventory": args.feature_inventory,
        },
        "records": records,
    }


def manifest_artifact_records(stage: str, manifest_path: str, manifest: dict[str, object]) -> list[dict[str, object]]:
    """Extract artifact references from one stage manifest."""
    records = [
        {
            "stage": stage,
            "role": "stage_manifest",
            "artifact": artifact_ref(manifest_path),
            "produced_by": None,
            "catalog_source": manifest_path,
        }
    ]
    sequence_keys = (
        "artifact_sequence",
        "core_pipeline_artifact_sequence",
        "exploratory_probe_artifact_sequence",
    )
    for sequence_key in sequence_keys:
        sequence = manifest.get(sequence_key, [])
        if not isinstance(sequence, list):
            continue
        for item in sequence:
            if not isinstance(item, dict):
                continue
            artifact = item.get("artifact")
            if not isinstance(artifact, dict):
                continue
            records.append(
                {
                    "stage": stage,
                    "role": item.get("role"),
                    "artifact": artifact,
                    "produced_by": item.get("produced_by"),
                    "catalog_source": manifest_path,
                }
            )
    return records


def build_artifact_catalog(
    args: argparse.Namespace,
    stage_manifests: dict[str, dict[str, object]],
) -> dict[str, object]:
    """Build the Stage 5 artifact catalog serving export."""
    manifest_paths = {
        "stage1": args.stage1_manifest,
        "stage2": args.stage2_manifest,
        "stage3": args.stage3_manifest,
        "stage4": args.stage4_manifest,
    }
    records = []
    for stage, manifest in stage_manifests.items():
        records.extend(manifest_artifact_records(stage, manifest_paths[stage], manifest))
    return {
        "stage": "stage5_operational_serving_exports",
        "status": "complete",
        "summary": {
            "artifact_count": len(records),
            "stage_count": len(stage_manifests),
            "consumer_count": len(CONSUMERS),
        },
        "pipeline_step": "01_build_serving_exports",
        "purpose": "Artifact catalog export for provenance and loading workflows.",
        "consumers": CONSUMERS,
        "inputs": manifest_paths,
        "records": records,
    }


def main() -> None:
    """Generate Stage 5 serving exports."""
    args = parse_args()
    export_dir = Path(args.export_dir)
    feature_inventory = read_json(args.feature_inventory)
    stage_manifests = {
        "stage1": read_json(args.stage1_manifest),
        "stage2": read_json(args.stage2_manifest),
        "stage3": read_json(args.stage3_manifest),
        "stage4": read_json(args.stage4_manifest),
    }

    exports = {
        "stage5_asset_summary.json": build_asset_summary(args, feature_inventory),
        "stage5_feature_family_summary.json": build_feature_family_summary(
            args,
            feature_inventory,
        ),
        "stage5_artifact_catalog.json": build_artifact_catalog(args, stage_manifests),
    }
    for filename, payload in exports.items():
        write_ordered_json(export_dir / filename, payload)
    print(f"Wrote {len(exports)} Stage 5 serving exports to {export_dir}.")


if __name__ == "__main__":
    main()
