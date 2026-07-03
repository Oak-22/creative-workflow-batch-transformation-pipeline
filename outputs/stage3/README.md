## Stage 3 Output Order

Stage 3 captures semantic/local Lightroom state across frozen sidecar
checkpoints. The JSON files are verbose because they preserve mask
groups, mask entries, local adjustment state, point-color state, hashes,
and comparison records.

There are two kinds of Stage 3 outputs:

- **Core pipeline proof:** the formal stage boundaries proving that
  Lightroom mask creation/copying and masked local edits persisted into
  sidecar state.
- **Exploratory behavior probes:** smaller investigations into how
  Lightroom writes local Point Color and global Point Color state.

The front-door artifact is:

```text
stage3_manifest.json
```

That manifest is intentionally compact. It references the core pipeline
proof artifacts and exploratory probe artifacts by path, size, SHA-256
hash, role, and producing script.

The optional proof-of-capability spike is:

```text
probes/stage3_mask_state_spike_report.json
```

That spike is exploratory evidence. The formal Stage 3 pipeline proof
starts with the pre-mask checkpoint.


## Core Pipeline Proof

Read or regenerate the core Stage 3 JSON artifacts in this order:

```text
1. pipeline/stage3_premasking_mask_state.json
   extracts mask state before Stage 3 mask creation

2. pipeline/stage3_postmasking_mask_state.json
   extracts state after mask creation/copying

3. pipeline/stage3_premasking_vs_postmasking_mask_state_comparison.json
   compares pre-mask vs post-mask state

4. pipeline/stage3_postlocal_adjustment_mask_state.json
   extracts state after masked local adjustment changes

5. pipeline/stage3_postmasking_vs_postlocal_adjustment_mask_state_comparison.json
   compares post-mask vs post-local-adjustment state
```

The core Stage 3 proof artifacts are:

```text
pipeline/stage3_premasking_vs_postmasking_mask_state_comparison.json
pipeline/stage3_postmasking_vs_postlocal_adjustment_mask_state_comparison.json
```

Those artifacts establish the formal Stage 3 handoff:

```text
no Lightroom mask state
  -> Lightroom mask state persisted in sidecars
  -> masked local adjustment state persisted in sidecars
```


## Exploratory Behavior Probes

The following artifacts are useful evidence, but they should be read as
behavior probes rather than as required pipeline outputs:

```text
6. probes/stage3_extracted_postglobal_point_color_mask_state.json
   extracts state after the asset-level global Point Color test

7. probes/stage3_mask_state_postglobal_point_color_comparison.json
   compares postlocal_adjustment vs postglobal_point_color
```

These outputs helped observe Lightroom-specific write behavior:

```text
local Point Color inside mask correction groups
asset-level global Point Color
```

Each comparison should still be read as an adjacent boundary check. It
should not be read as a comparison against every prior state.


## Folder Grouping

Stage 3 intentionally groups verbose JSON artifacts by review role:

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

The `pipeline/` folder is the formal Stage 3 proof path. The `probes/`
folder is intentionally exploratory: those artifacts explain Lightroom
write behavior that shaped later design, but they are not required to
understand the core stage handoff.


## Checkpoint Sequence

The output sequence maps to frozen sidecar checkpoint folders:

```text
data/stage3/reference_state/lightroom_sidecars_presegmentation/
  -> outputs/stage3/pipeline/stage3_premasking_mask_state.json

data/stage3/conditioned_state/lightroom_sidecars_postmasking_no_local_adjustment/
  -> outputs/stage3/pipeline/stage3_postmasking_mask_state.json
  -> outputs/stage3/pipeline/stage3_premasking_vs_postmasking_mask_state_comparison.json

data/stage3/conditioned_state/lightroom_sidecars_postlocal_adjustment/
  -> outputs/stage3/pipeline/stage3_postlocal_adjustment_mask_state.json
  -> outputs/stage3/pipeline/stage3_postmasking_vs_postlocal_adjustment_mask_state_comparison.json

data/stage3/conditioned_state/lightroom_sidecars_postglobal_point_color/
  -> outputs/stage3/probes/stage3_extracted_postglobal_point_color_mask_state.json
  -> outputs/stage3/probes/stage3_mask_state_postglobal_point_color_comparison.json
```

If the Stage 3 extractor schema changes, regenerate all Stage 3 extracts
before regenerating comparisons. Otherwise a comparison may report
schema drift as if it were Lightroom state change. Regenerate
`stage3_manifest.json` after the affected extracts and comparisons are
current.
