"""Stage 4 step 04: build an ML handoff contract."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from scripts.python.common import ensure_parent_dir, read_json


DEFAULT_FEATURE_INVENTORY = "outputs/stage4/features/stage4_feature_inventory.json"
DEFAULT_READINESS_REPORT = "outputs/stage4/handoff/stage4_dataset_readiness_report.json"
DEFAULT_OUTPUT = "outputs/stage4/handoff/stage4_ml_handoff_contract.json"


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for ML handoff contract generation."""
    parser = argparse.ArgumentParser(
        description="Build a Stage 4 handoff contract for a hypothetical ML team."
    )
    parser.add_argument("--feature-inventory", default=DEFAULT_FEATURE_INVENTORY)
    parser.add_argument("--readiness-report", default=DEFAULT_READINESS_REPORT)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    return parser.parse_args()


def build_contract(args: argparse.Namespace) -> dict[str, object]:
    """Build the Stage 4 ML handoff contract."""
    inventory = read_json(args.feature_inventory)
    readiness = read_json(args.readiness_report)
    inventory_summary = inventory.get("summary", {})
    readiness_summary = readiness.get("summary", {})
    if not isinstance(inventory_summary, dict):
        inventory_summary = {}
    if not isinstance(readiness_summary, dict):
        readiness_summary = {}

    return {
        "stage": "stage4_ml_readiness_handoff",
        "status": "contract_ready_for_review",
        "summary": {
            "asset_count": inventory_summary.get("asset_count"),
            "complete_handoff_feature_asset_count": inventory_summary.get(
                "complete_handoff_feature_asset_count"
            ),
            "feature_family_count": len(inventory.get("feature_families", [])),
            "model_training_readiness": readiness_summary.get(
                "model_training_readiness"
            ),
        },
        "pipeline_step": "04_build_ml_handoff_contract",
        "purpose": (
            "Define what this repository can hand to a future ML/data-science team "
            "without overstating current model-training readiness."
        ),
        "inputs": {
            "feature_inventory": args.feature_inventory,
            "dataset_readiness_report": args.readiness_report,
        },
        "producer": {
            "system": "digital_asset_processing_pipeline",
            "responsibility": (
                "Produce stage-bounded, hash-backed, inspectable artifacts from a "
                "Lightroom-centered creative workflow."
            ),
        },
        "consumer": {
            "team": "hypothetical_ml_team",
            "responsibility": (
                "Evaluate feature sufficiency, define targets, collect labels, and "
                "decide whether modeling is justified."
            ),
        },
        "stable_join_keys": [
            {
                "key": "asset_key",
                "meaning": "Native asset stem used to join RAW, XMP, ACR, manifests, and derived metrics.",
                "current_status": "implemented",
            }
        ],
        "handoff_artifacts": [
            {
                "artifact": "outputs/stage1/stage1_manifest.json",
                "role": "asset identity and metadata-state summary",
            },
            {
                "artifact": "outputs/stage2/stage2_manifest.json",
                "role": "global Develop transformation evidence index",
            },
            {
                "artifact": "outputs/stage3/stage3_manifest.json",
                "role": "semantic/local mask-state evidence index",
            },
            {
                "artifact": args.feature_inventory,
                "role": "cross-stage feature inventory",
            },
            {
                "artifact": args.readiness_report,
                "role": "modeling readiness and gap analysis",
            },
        ],
        "feature_families": inventory.get("feature_families", []),
        "dataset_scope": {
            "asset_count": inventory_summary.get("asset_count"),
            "complete_handoff_feature_asset_count": inventory_summary.get(
                "complete_handoff_feature_asset_count"
            ),
            "model_training_readiness": readiness_summary.get(
                "model_training_readiness"
            ),
        },
        "approved_claims": [
            "The repository can materialize a structured ML-readiness handoff package.",
            "The repository can identify which feature families exist per asset.",
            "The repository can distinguish source signal metrics from Lightroom parameter evidence.",
            "The repository can state current modeling gaps explicitly.",
        ],
        "non_claims": [
            "No trained model exists in the current repository.",
            "No model accuracy, cost reduction, or editing-style mimicry result is claimed.",
            "RAW metrics are not equivalent to final Lightroom-rendered visual state.",
            "Stage 3 mask state is evidence of Lightroom sidecar persistence, not proof of segmentation quality by itself.",
        ],
        "next_handoff_questions": [
            "Which business objective should define the target: editing-speed reduction, style suggestion, compute optimization, or QA?",
            "What label source will define accepted, rejected, or corrected transformations?",
            "Will modeling consume XMP/ACR parameter state, RAW signal summaries, Lightroom-rendered JPEG targets, or a joined multi-modal dataset?",
            "What minimum cross-shoot dataset size is required before a proof model is meaningful?",
        ],
    }


def write_ordered_json(path: str | Path, payload: dict[str, object]) -> Path:
    """Write JSON while preserving semantic insertion order."""
    target = ensure_parent_dir(path)
    with target.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    return target


def main() -> None:
    """Generate the Stage 4 ML handoff contract."""
    args = parse_args()
    contract = build_contract(args)
    write_ordered_json(args.output, contract)
    print(
        f"Wrote {args.output} with "
        f"{len(contract['feature_families'])} feature families."
    )


if __name__ == "__main__":
    main()
