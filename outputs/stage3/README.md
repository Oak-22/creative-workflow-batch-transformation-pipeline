## Stage 3 Output Order

Stage 3 captures semantic/local Lightroom state across frozen sidecar
checkpoints. The JSON files are verbose because they preserve mask
groups, mask entries, local adjustment state, point-color state, hashes,
and comparison records.

There are two kinds of Stage 3 outputs:

- **Core pipeline proof:** the formal stage boundary proving that
  Lightroom mask creation/copying persisted into sidecar state.
- **Exploratory behavior probes:** smaller investigations into how
  Lightroom writes local masked adjustments, local Point Color, and
  global Point Color state.

The front-door artifact is:

```text
stage3_manifest.json
```

That manifest is intentionally compact. It references the core pipeline
proof artifacts and exploratory probe artifacts by path, size, SHA-256
hash, role, and producing script.

The optional proof-of-capability spike is:

```text
stage3_mask_state_spike_report.json
```

That spike is exploratory evidence. The main Stage 3 checkpoint ladder
starts with `presegmentation`.


## Core Pipeline Proof

Read or regenerate the core Stage 3 JSON artifacts in this order:

```text
1. stage3_extracted_presegmentation_mask_state.json
   extracts mask state before Stage 3 mask creation

2. stage3_extracted_postmasking_no_local_adjustment_mask_state.json
   extracts state after mask creation/copying, before intentional masked
   local Develop changes

3. stage3_mask_state_postmasking_no_local_adjustment_comparison.json
   compares presegmentation vs postmasking_no_local_adjustment
```

The core Stage 3 proof artifact is:

```text
stage3_mask_state_postmasking_no_local_adjustment_comparison.json
```

That artifact establishes the formal Stage 3 handoff:

```text
no Lightroom mask state
  -> Lightroom mask state persisted in sidecars
```


## Exploratory Behavior Probes

The following artifacts are useful evidence, but they should be read as
behavior probes rather than as required pipeline outputs:

```text
4. stage3_extracted_postlocal_adjustment_mask_state.json
   extracts state after masked local adjustment changes

5. stage3_mask_state_postlocal_adjustment_comparison.json
   compares postmasking_no_local_adjustment vs postlocal_adjustment

6. stage3_extracted_postglobal_point_color_mask_state.json
   extracts state after the asset-level global Point Color test

7. stage3_mask_state_postglobal_point_color_comparison.json
   compares postlocal_adjustment vs postglobal_point_color
```

These outputs helped observe Lightroom-specific write behavior:

```text
masked local Develop settings
local Point Color inside mask correction groups
asset-level global Point Color
```

Each comparison should still be read as an adjacent boundary check. It
should not be read as a comparison against every prior state.


## Future Folder Grouping

The current flat file layout is retained because script defaults and
existing references point to these paths. If Stage 3 output layout is
migrated later, prefer this visual grouping:

```text
outputs/stage3/
  pipeline/
    stage3_extracted_presegmentation_mask_state.json
    stage3_extracted_postmasking_no_local_adjustment_mask_state.json
    stage3_mask_state_postmasking_no_local_adjustment_comparison.json

  probes/
    stage3_mask_state_spike_report.json
    stage3_extracted_postlocal_adjustment_mask_state.json
    stage3_mask_state_postlocal_adjustment_comparison.json
    stage3_extracted_postglobal_point_color_mask_state.json
    stage3_mask_state_postglobal_point_color_comparison.json
```

Do that as an explicit path migration, not as an incidental cleanup,
because moving generated artifacts requires updating script defaults and
documentation links together.


## Checkpoint Sequence

The output sequence maps to frozen sidecar checkpoint folders:

```text
data/stage3/reference_state/lightroom_sidecars_presegmentation/
  -> outputs/stage3/stage3_extracted_presegmentation_mask_state.json

data/stage3/conditioned_state/lightroom_sidecars_postmasking_no_local_adjustment/
  -> outputs/stage3/stage3_extracted_postmasking_no_local_adjustment_mask_state.json
  -> outputs/stage3/stage3_mask_state_postmasking_no_local_adjustment_comparison.json

data/stage3/conditioned_state/lightroom_sidecars_postlocal_adjustment/
  -> outputs/stage3/stage3_extracted_postlocal_adjustment_mask_state.json
  -> outputs/stage3/stage3_mask_state_postlocal_adjustment_comparison.json

data/stage3/conditioned_state/lightroom_sidecars_postglobal_point_color/
  -> outputs/stage3/stage3_extracted_postglobal_point_color_mask_state.json
  -> outputs/stage3/stage3_mask_state_postglobal_point_color_comparison.json
```

If the Stage 3 extractor schema changes, regenerate all Stage 3 extracts
before regenerating comparisons. Otherwise a comparison may report
schema drift as if it were Lightroom state change. Regenerate
`stage3_manifest.json` after the affected extracts and comparisons are
current.
