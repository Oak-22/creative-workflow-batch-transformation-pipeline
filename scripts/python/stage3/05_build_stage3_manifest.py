"""Stage 3 step 05: build a compact manifest from mask-state artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from scripts.python.common import ensure_parent_dir, read_json


DEFAULT_PRESEGMENTATION_EXTRACT = "outputs/stage3/pipeline/stage3_premasking_mask_state.json"
DEFAULT_POSTMASKING_EXTRACT = "outputs/stage3/pipeline/stage3_postmasking_mask_state.json"
DEFAULT_POSTMASKING_COMPARISON = (
    "outputs/stage3/pipeline/stage3_premasking_vs_postmasking_mask_state_comparison.json"
)
DEFAULT_SPIKE_REPORT = "outputs/stage3/probes/stage3_mask_state_spike_report.json"
DEFAULT_POSTLOCAL_EXTRACT = (
    "outputs/stage3/pipeline/stage3_postlocal_adjustment_mask_state.json"
)
DEFAULT_POSTLOCAL_COMPARISON = (
    "outputs/stage3/pipeline/stage3_postmasking_vs_postlocal_adjustment_mask_state_comparison.json"
)
DEFAULT_POSTGLOBAL_POINT_COLOR_EXTRACT = (
    "outputs/stage3/probes/stage3_extracted_postglobal_point_color_mask_state.json"
)
DEFAULT_POSTGLOBAL_POINT_COLOR_COMPARISON = (
    "outputs/stage3/probes/stage3_mask_state_postglobal_point_color_comparison.json"
)
DEFAULT_OUTPUT = "outputs/stage3/stage3_manifest.json"


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for Stage 3 manifest generation."""
    parser = argparse.ArgumentParser(
        description="Build a compact Stage 3 manifest from generated artifacts."
    )
    parser.add_argument(
        "--presegmentation-extract",
        default=DEFAULT_PRESEGMENTATION_EXTRACT,
        help="Mask-state extract for the frozen formal pre-mask checkpoint.",
    )
    parser.add_argument(
        "--postmasking-extract",
        default=DEFAULT_POSTMASKING_EXTRACT,
        help=(
            "Mask-state extract for the frozen formal post-mask checkpoint."
        ),
    )
    parser.add_argument(
        "--postmasking-comparison",
        default=DEFAULT_POSTMASKING_COMPARISON,
        help="Core Stage 3 pre-mask vs post-mask comparison.",
    )
    parser.add_argument(
        "--spike-report",
        default=DEFAULT_SPIKE_REPORT,
        help="Optional proof-of-capability spike report.",
    )
    parser.add_argument(
        "--postlocal-extract",
        default=DEFAULT_POSTLOCAL_EXTRACT,
        help="Mask-state extract for the frozen formal post-local-adjustment checkpoint.",
    )
    parser.add_argument(
        "--postlocal-comparison",
        default=DEFAULT_POSTLOCAL_COMPARISON,
        help="Core Stage 3 post-mask vs post-local-adjustment comparison.",
    )
    parser.add_argument(
        "--postglobal-point-color-extract",
        default=DEFAULT_POSTGLOBAL_POINT_COLOR_EXTRACT,
        help="Optional global Point Color behavior-probe extract.",
    )
    parser.add_argument(
        "--postglobal-point-color-comparison",
        default=DEFAULT_POSTGLOBAL_POINT_COLOR_COMPARISON,
        help="Optional global Point Color behavior-probe comparison.",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help="Destination Stage 3 manifest JSON.",
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


def optional_artifact_ref(path: str | Path) -> dict[str, object] | None:
    """Return an artifact reference when an optional artifact exists."""
    artifact_path = Path(path)
    if not artifact_path.is_file():
        return None
    return artifact_ref(artifact_path)


def sequence_item(
    order: int,
    role: str,
    produced_by: str,
    artifact: dict[str, object] | None,
) -> dict[str, object]:
    """Return one compact artifact-sequence item."""
    return {
        "order": order,
        "role": role,
        "produced_by": produced_by,
        "artifact": artifact,
    }


def core_artifact_sequence(args: argparse.Namespace) -> list[dict[str, object]]:
    """Return formal Stage 3 pipeline artifacts in production order."""
    return [
        sequence_item(
            1,
            "premasking_mask_state_extract",
            "scripts/python/stage3/01_extract_mask_state.py",
            artifact_ref(args.presegmentation_extract),
        ),
        sequence_item(
            2,
            "postmasking_mask_state_extract",
            "scripts/python/stage3/01_extract_mask_state.py",
            artifact_ref(args.postmasking_extract),
        ),
        sequence_item(
            3,
            "premasking_vs_postmasking_comparison",
            "scripts/python/stage3/02_compare_mask_state.py",
            artifact_ref(args.postmasking_comparison),
        ),
        sequence_item(
            4,
            "postlocal_adjustment_mask_state_extract",
            "scripts/python/stage3/01_extract_mask_state.py",
            artifact_ref(args.postlocal_extract),
        ),
        sequence_item(
            5,
            "postmasking_vs_postlocal_adjustment_comparison",
            "scripts/python/stage3/02_compare_mask_state.py",
            artifact_ref(args.postlocal_comparison),
        ),
    ]


def probe_artifact_sequence(args: argparse.Namespace) -> list[dict[str, object]]:
    """Return optional Stage 3 exploratory behavior-probe artifacts."""
    candidates = [
        sequence_item(
            1,
            "proof_of_capability_mask_sidecar_parsing_spike",
            "scripts/python/stage3/01_extract_mask_state.py",
            optional_artifact_ref(args.spike_report),
        ),
        sequence_item(
            2,
            "postglobal_point_color_mask_state_extract",
            "scripts/python/stage3/01_extract_mask_state.py",
            optional_artifact_ref(args.postglobal_point_color_extract),
        ),
        sequence_item(
            3,
            "postlocal_adjustment_vs_postglobal_point_color_comparison",
            "scripts/python/stage3/02_compare_mask_state.py",
            optional_artifact_ref(args.postglobal_point_color_comparison),
        ),
    ]
    return [item for item in candidates if item["artifact"] is not None]


def comparison_summary(payload: dict[str, object]) -> dict[str, object]:
    """Return a comparison summary object when present."""
    summary = payload.get("summary", {})
    return summary if isinstance(summary, dict) else {}


def build_summary(
    mask_definition_comparison: dict[str, object],
    mask_edit_comparison: dict[str, object],
    probes: list[dict[str, object]],
) -> dict[str, object]:
    """Build a compact Stage 3 summary from core and probe artifacts."""
    definition_summary = comparison_summary(mask_definition_comparison)
    edit_summary = comparison_summary(mask_edit_comparison)
    return {
        "core_asset_count": definition_summary.get("asset_count"),
        "mask_definition_changed_asset_count": definition_summary.get(
            "changed_asset_count"
        ),
        "mask_edit_changed_asset_count": edit_summary.get("changed_asset_count"),
        "postmasking_mask_group_count": definition_summary.get(
            "after_state_mask_group_count"
        ),
        "postmasking_mask_entry_count": definition_summary.get(
            "after_state_mask_entry_count"
        ),
        "postlocal_adjustment_mask_group_count": edit_summary.get(
            "after_state_mask_group_count"
        ),
        "postlocal_adjustment_mask_entry_count": edit_summary.get(
            "after_state_mask_entry_count"
        ),
        "exploratory_probe_artifact_count": len(probes),
    }


def comparison_missing_count(payload: dict[str, object]) -> int:
    """Return the asset mismatch count for one comparison artifact."""
    summary = comparison_summary(payload)
    return int(summary.get("missing_before_state_asset_count") or 0) + int(
        summary.get("missing_after_state_asset_count") or 0
    )


def validation_status(
    mask_definition_comparison: dict[str, object],
    mask_edit_comparison: dict[str, object],
) -> dict[str, object]:
    """Return manifest validation status derived from core comparisons."""
    missing_count = comparison_missing_count(mask_definition_comparison)
    missing_count += comparison_missing_count(mask_edit_comparison)
    comparisons_complete = (
        mask_definition_comparison.get("status") == "complete"
        and mask_edit_comparison.get("status") == "complete"
    )
    status = "validated" if comparisons_complete and missing_count == 0 else "review_required"
    return {
        "status": status,
        "mask_definition_comparison_status": mask_definition_comparison.get("status"),
        "mask_edit_comparison_status": mask_edit_comparison.get("status"),
        "missing_core_compared_asset_count": missing_count,
    }


def build_manifest(args: argparse.Namespace) -> dict[str, object]:
    """Build the stable Stage 3 manifest payload."""
    mask_definition_comparison = read_json(args.postmasking_comparison)
    mask_edit_comparison = read_json(args.postlocal_comparison)
    core_sequence = core_artifact_sequence(args)
    probe_sequence = probe_artifact_sequence(args)
    validation = validation_status(mask_definition_comparison, mask_edit_comparison)
    return {
        "stage": "stage3_semantic_local_conditioning",
        "status": validation["status"],
        "pipeline_step": "05_build_stage3_manifest",
        "purpose": (
            "Compact index for Stage 3 generated evidence. This manifest "
            "separates the formal mask definition and mask-edit pipeline proof from "
            "exploratory Lightroom write-behavior probes."
        ),
        "core_pipeline_artifact_sequence": core_sequence,
        "exploratory_probe_artifact_sequence": probe_sequence,
        "validation": validation,
        "summary": build_summary(
            mask_definition_comparison,
            mask_edit_comparison,
            probe_sequence,
        ),
    }


def write_ordered_json(path: str | Path, payload: dict[str, object]) -> Path:
    """Write JSON while preserving semantic insertion order."""
    target = ensure_parent_dir(path)
    with target.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    return target


def main() -> None:
    """Generate the Stage 3 manifest artifact."""
    args = parse_args()
    manifest = build_manifest(args)
    write_ordered_json(args.output, manifest)
    print(
        f"Wrote {args.output} with "
        f"{len(manifest['core_pipeline_artifact_sequence'])} core artifacts "
        f"and {len(manifest['exploratory_probe_artifact_sequence'])} probes."
    )


if __name__ == "__main__":
    main()
