## Stage 3 Layout

Stage 3 captures Lightroom semantic/local conditioning state after the
Stage 2 global Develop baseline. The core evidence question is how
Lightroom persists masks, local adjustment state, and point-color state
across increasingly narrow GUI-assisted edits.

Stage 3 currently uses this checkpoint ladder:

```text
presegmentation
  -> postmasking_no_local_adjustment
  -> postlocal_adjustment
  -> postglobal_point_color
```

Each checkpoint is a frozen sidecar state copied out of the mutable
Lightroom working set. The frozen checkpoint folders are the evidence
inputs for the Stage 3 extraction and comparison outputs.

Recommended artifact model:

- `reference_state/lightroom_sidecars_presegmentation/`: frozen sidecars
  before Stage 3 mask creation
- `conditioned_state/lightroom_sidecars_postmasking_no_local_adjustment/`:
  frozen sidecars after mask creation/copying, before intentional masked
  local Develop changes
- `conditioned_state/lightroom_sidecars_postlocal_adjustment/`: frozen
  sidecars after masked local adjustment changes
- `conditioned_state/lightroom_sidecars_postglobal_point_color/`: frozen
  sidecars after the asset-level global Point Color test
- `spikes/proof_of_capability_mask_sidecar_parsing/`: smaller exploratory
  evidence used to prove Lightroom mask state persistence before
  promoting the shape into the main Stage 3 checkpoint ladder

Derived analysis artifacts belong under `outputs/stage3/`. The manifest
stays at the stage root as the employer-facing review index, while the
verbose support artifacts are grouped by review role. The core pipeline
includes both mask-definition persistence and masked local-edit
persistence.

```text
outputs/stage3/
  stage3_manifest.json

  pipeline/
    stage3_premasking_mask_state.json
    stage3_postmasking_mask_state.json
    stage3_premasking_vs_postmasking_mask_state_comparison.json
    stage3_postlocal_adjustment_mask_state.json
    stage3_postmasking_vs_postlocal_adjustment_mask_state_comparison.json

  probes/
    stage3_mask_state_spike_report.json
    stage3_extracted_postglobal_point_color_mask_state.json
    stage3_mask_state_postglobal_point_color_comparison.json
```

That grouping keeps the workflow readable in file explorers while still
preserving the conceptual sequence:

```text
source checkpoint
  -> extracted state
  -> comparison report
```

Do not treat `data/live_workspace/` as the durable Stage 3 evidence
source. Lightroom may continue mutating it as the catalog updates. Use
the frozen Stage 3 sidecar folders for repeatable extraction,
comparison, and review.
